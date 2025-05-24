import yfinance as yf
import os
from logger import Logger
from enricher import DataEnricher
from modeller import Modeller
from dashboard import KpiCalculator
import pandas as pd
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


def main():
    collector = Collector("COCA34.SA")
    log.info(f"Nombre largo: {collector.info['longName']}")
    log.info(f"Sector: {collector.info['sector']}")
    log.info(f"Cierre anterior: {collector.info['previousClose']}")

    historical_data = collector.get_data()
    historical_data = historical_data.reset_index()
    total_datos = len(historical_data)

    log.info(f"Total de datos obtenidos: {total_datos}")
    try:
        enricher = DataEnricher(historical_data)
        enriched_data = enricher.enrich()
        log.info("Datos enriquecidos correctamente.")
        log.info(f"Total de datos enriquecidos: {len(enriched_data)}")
    except Exception as e:
        log.error(f"Error al enriquecer los datos: {e}")
        enriched_data = None 

    if historical_data is not None:
        log.info("Guardando datos en archivo CSV...")
        
        csv_path = f"{collector.ruta_static}/data/historical.csv"
        historical_data.to_csv(csv_path)
        log.info(f"Datos guardados en archivo CSV: {csv_path}")
        
        csv_path = f"{collector.ruta_static}/data/enriched.csv"
        enriched_data.to_csv(csv_path)
        log.info(f"Datos enriquecidos guardados en: {csv_path}")
    else:
        log.error("No se guardaron datos porque no se recuperó información histórica.")

    log.info("Obtener datos para entrenar el modelo")
    try:
        modeller = Modeller("src/coca_cola/static/data/enriched.csv")
        modeller.entrenar()
        log.info("Modelo entrenado correctamente.")
        log.info(f"Modelo guardado en: {modeller.model_path}")
    except Exception as e:
        log.error(f"Error al entrenar el modelo: {e}")
        modeller = None

    log.info("Obtener datos para predecir")
    if modeller is None:
        log.error("No se pudo entrenar el modelo. No se puede predecir.")
        exit(1)
    try:     
        predicciones = modeller.predecir(enriched_data)
        log.info(predicciones[:5])
        log.info("Predicciones realizadas correctamente.")
        log.info(f"Predicciones guardadas en: {modeller.model_path}")
        # pred_df = pd.DataFrame(predicciones, columns=["predicted_close"])
        pred_path = f"{collector.ruta_static}/data/predicciones.csv"
        # pred_df.to_csv(pred_path, index=False)
        enriched_data["predicted_close"] = predicciones
        enriched_data.to_csv(f"{collector.ruta_static}/data/predicciones.csv", index=False)
        log.info(f"Predicciones guardadas en archivo CSV: {pred_path}")
        
    except Exception as e:
        log.error(f"Error al predecir: {e}")
        predicciones = None
        
    try:
        kpi_path = f"{collector.ruta_static}/data/kpis.csv"
        kpi_calculator = KpiCalculator(enriched_data, kpi_path)
        kpi_df = kpi_calculator.calcular_kpis()
        log.info("KPIs calculados y guardados correctamente.")
        log.info(f"Archivo de KPIs generado en: {kpi_path}")
        log.info(f"\n{kpi_df}")
    except Exception as e:
        log.error(f"Error al calcular los KPIs: {e}")    

if __name__ == "__main__":
    main()
