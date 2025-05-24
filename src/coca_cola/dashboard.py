import pandas as pd
from datetime import date

class KpiCalculator:
    def __init__(self, enriched_df: pd.DataFrame, output_path: str):
        self.df = enriched_df.copy()
        self.output_path = output_path

    def calcular_kpis(self):
        self.df["daily_return"] = self.df["Close"].pct_change()

        kpis = {
            "Tasa de variación diaria promedio (%)": self.df["daily_return"].mean() * 100,
            "Media móvil 5 días promedio": self.df["moving_avg_5"].mean(),
            "Volatilidad 20 días promedio": self.df["volatility_20"].mean(),
            "Retorno acumulado (%)": (self.df["Close"].iloc[-1] / self.df["Close"].iloc[0] - 1) * 100,
            "Desviación estándar del precio de cierre": self.df["Close"].std()
        }

        # Convertir a DataFrame y redondear a 2 decimales
        kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI", "Valor"])
        kpi_df["Valor"] = kpi_df["Valor"].round(2)
        kpi_df["Fecha"] = date.today()

        kpi_df.to_csv(self.output_path, index=False)
        return kpi_df
