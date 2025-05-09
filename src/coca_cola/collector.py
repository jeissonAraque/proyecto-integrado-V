import yfinance as yf
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
        log.info(f"Collector inicializado para el ticker {ticker_symbol}")
        
    def get_data(self):
        log.info(f"Datos obtenidos desde el 2011 a 2025.")
        return self.ticker.history(period="max", interval="1d")
  
         
collector = Collector("COCA34.SA")
log.info(f"Nombre largo: {collector.info['longName']}")
log.info(f"Sector: {collector.info['sector']}")
log.info(f"Cierre anterior: {collector.info['previousClose']}")

historical_data = collector.get_data()
total_datos = len(historical_data)
log.info(f"Total de datos obtenidos: {total_datos}")
 
if historical_data is not None:
    log.info("Guardando datos en archivo CSV...")
    
    csv_path = f"{collector.ruta_static}/data/historical.csv"
    historical_data.to_csv(csv_path)
    log.info(f"Datos guardados en archivo CSV: {csv_path}")

else:
    log.error("No se guardaron datos porque no se recuperó información histórica.")

