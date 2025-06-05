import pandas as pd
from datetime import date

class KpiCalculator:
    def __init__(self, enriched_df: pd.DataFrame, output_path: str):
        self.df = enriched_df.copy()
        self.output_path = output_path

#     def calcular_kpis(self):
#         self.df["daily_return"] = self.df["Close"].pct_change()

#         kpis = {
#             "Tasa de variación diaria promedio (%)": self.df["daily_return"].mean() * 100,
#             "Media móvil 5 días promedio": self.df["moving_avg_5"].mean(),
#             "Volatilidad 20 días promedio": self.df["volatility_20"].mean(),
#             "Retorno acumulado (%)": (self.df["Close"].iloc[-1] / self.df["Close"].iloc[0] - 1) * 100,
#             "Desviación estándar del precio de cierre": self.df["Close"].std()
#         }

#         # Convertir a DataFrame y redondear a 2 decimales
#         kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI", "Valor"])
#         kpi_df["Valor"] = kpi_df["Valor"].round(2)
#         kpi_df["Fecha"] = date.today()

#         kpi_df.to_csv(self.output_path, index=False)
#         return kpi_df

    def calcular_kpis(self):
        self.df["daily_return"] = self.df["Close"].pct_change()
        self.df["Year"] = self.df["Date"].dt.year  # Asegúrate de que "Date" esté en formato datetime

        kpi_df = self.df.groupby("Year").agg({
            "daily_return": lambda x: x.mean() * 100,
            "moving_avg_5": "mean",
            "volatility_20": "mean",
            "Close": ["first", "last", "std"]
        }).reset_index()

        # Renombrar columnas
        kpi_df.columns = ["Year", 
                        "Tasa de variación diaria promedio (%)", 
                        "Media móvil 5 días promedio", 
                        "Volatilidad 20 días promedio", 
                        "Primer cierre", 
                        "Último cierre", 
                        "Desviación estándar del precio de cierre"]

        # Calcular retorno acumulado
        kpi_df["Retorno acumulado (%)"] = ((kpi_df["Último cierre"] / kpi_df["Primer cierre"]) - 1) * 100

        # Eliminar columnas auxiliares si no las necesitas
        kpi_df.drop(columns=["Primer cierre", "Último cierre"], inplace=True)

        # Redondear
        kpi_df = kpi_df.round(2)

        # Guardar
        kpi_df.to_csv(self.output_path, index=False)
        return kpi_df
