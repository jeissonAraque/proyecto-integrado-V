import pandas as pd
import numpy as np

class DataEnricher:
    def __init__(self, df):
        self.df = df.copy()
    
    def enrich(self):
        df = self.df
        df['daily_return'] = df['Close'].pct_change()
        df['cumulative_return'] = (1 + df['daily_return']).cumprod()
        df['moving_avg_5'] = df['Close'].rolling(window=5).mean()
        df['moving_avg_20'] = df['Close'].rolling(window=20).mean()
        df['volatility_20'] = df['daily_return'].rolling(window=20).std()
        df['price_change'] = df['Close'].diff()
        df["Day"] = df["Date"].dt.day
        df["Month"] = df["Date"].dt.month
        df["Year"] = df["Date"].dt.year
        df["Weekday"] = df["Date"].dt.day_name()
        df = df.dropna()  # eliminar filas con valores faltantes generados por rolling
        return df
