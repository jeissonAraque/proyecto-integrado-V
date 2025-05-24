import pandas as pd
import numpy as np
import os
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from logger import Logger
import warnings
warnings.filterwarnings("ignore")

log = Logger(name="ModellerLogger", log_file="logs/modeller.log").get_logger()

class Modeller:
    def __init__(self, data_path, model_path="src/coca_cola/static/models/model.pkl"):
        self.data_path = data_path
        self.model_path = model_path
        self.model = LinearRegression()
    
    def entrenar(self):
        # Cargar datos
        df = pd.read_csv(self.data_path)
        df = df.dropna()

        # Variables predictoras y objetivo
        X = df[['moving_avg_5', 'moving_avg_20', 'volatility_20']]
        y = df['Close']

        # División en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar modelo
        self.model.fit(X_train, y_train)

        # Predicciones
        y_pred = self.model.predict(X_test)

        # Evaluación
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = self.model.score(X_test, y_test)

        log.info("Modelo entrenado.")
        log.info(f"RMSE: {rmse:.4f}")
        log.info(f"MAE: {mae:.4f}")
        log.info(f"R²: {r2:.4f}")

        # Guardar modelo
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        log.info(f"Modelo guardado en: {self.model_path}")
    
    def predecir(self, nuevo_df):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError("El modelo no ha sido entrenado. No se encontró model.pkl")
        
        model = joblib.load(self.model_path)
        predicciones = model.predict(nuevo_df[['moving_avg_5', 'moving_avg_20', 'volatility_20']])
        return predicciones
