import pandas as pd

class EarningsAnalyzer:
    
    def __init__(self, raw_df):
        self.df = self._clean_data(raw_df)
        
    def _clean_data(self, df):
        
        df = df.dropna(subset=["EPS Estimate", "Reported EPS"]).copy()
        
    