import pandas as pd

class EarningsAnalyzer:
    
    def __init__(self, raw_df):
        self.df = self._clean_data(raw_df)
        
    def _clean_data(self, df):
        
        df = df.dropna(subset=["EPS Estimate", "Reported EPS"]).copy()
        
        df = df.sort_index(ascending=False)
        df["Surprise %"] = (
            (df["Reported EPS"] - df["EPS Estimate"]) / df["EPS Estimate"].abs()) * 100
        
        df["Beat"] = df["Surprise %"] > 0
        df["Result"] = df["Beat"].map({True: "✅ Beat", False: "❌ Miss"})
        
        df = df.drop(columns=["Surprise(%)"], errors="ignore")
        df = df.drop(columns=)
        
        return df
    
    def get_df(self):
        return self.df
    def beat_rate(self):
        return self.df["Beat"].mean() * 100
    def average_surprise(self):
        return self.df["Surprise %"].mean()
    def best_quarter(self):
        return self.df["Surprise %"].max()
    def worst_quarter(self):
        return self.df["Surprise %"].min()
    def quarters_analyzed(self):
        return len(self.df)
        
    