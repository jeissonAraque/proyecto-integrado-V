import requests
import numpy as np
import json
import time
import pandas as pd
import yfinance as yf
import sqlite3
import os
from logger import Logger
import warnings
warnings.filterwarnings("ignore")

log = Logger(name="CollectorLogger", log_file="logs/collector.log").get_logger()

class Collector:
    def __init__(self, ticker_symbol):
        self.ticker = yf.Ticker(ticker_symbol) 
        self.info = self.ticker.info
        self.ruta_static = "src/coca_cola/static"
        self.db_path = os.path.join(self.ruta_static, "data", "historical.db")  
        self.create_table()
        log.info(f"Collector inicializado para el ticker {ticker_symbol}")
        
    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Crear la tabla si no existe
        c.execute('''
        CREATE TABLE IF NOT EXISTS historical_data (
            Date TEXT,
            Open REAL,
            High REAL,
            Low REAL,
            Close REAL,
            Volume INTEGER
        )
        ''')
        conn.commit()
        conn.close()  
        log.info("Tabla historical_data creada/verificada en la base de datos SQLite.")  
        
    def get_data(self, start_date=None, end_date=None):
        if start_date and end_date:
            log.info(f"Datos obtenidos para el período {start_date} a {end_date}.")
            return self.ticker.history(start=start_date, end=end_date, interval="1d")
        else:
            log.warning("No se proporcionaron fechas válidas para obtener datos.")
            return None 
        
    def save_to_sqlite(self, data):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Insertar datos históricos en la tabla
        for index, row in data.iterrows():
            c.execute('''
            INSERT INTO historical_data (Date, Open, High, Low, Close, Volume)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))
        
        conn.commit()
        conn.close()
        log.info("Datos guardados en la base de datos SQLite.")
        print("Datos guardados en SQLite correctamente.")   
       


collector = Collector("KO")
print(collector.info["longName"])
print(collector.info["sector"]) 
print(collector.info["previousClose"])
log.info(f"Nombre largo: {collector.info['longName']}")
log.info(f"Sector: {collector.info['sector']}")
log.info(f"Cierre anterior: {collector.info['previousClose']}")

historical_data = collector.get_data("2023-01-01", "2023-10-01")
 
if historical_data is not None:
    csv_path = os.path.join(collector.ruta_static, "data", "historical.csv")
    historical_data.to_csv(csv_path)
    log.info(f"Datos guardados en archivo CSV: {csv_path}")
    print(f"Datos guardados en archivo CSV: {csv_path}")

    collector.save_to_sqlite(historical_data)
    log.info("Guardado en la base de datos exitosamente.")
    print("Guardado en la base de datos exitosamente.")
else:
    log.error("No se guardaron datos porque no se recuperó información histórica.")
    print("No se guardaron datos porque no se recuperó información histórica.")

