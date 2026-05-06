import yfinance as yf
import pandas as pd

class Predictor:
    def __init__(self, ticker, analyzer):
        self.ticker = ticker
        self.analyzer = analyzer
        self._stock = yf.Ticker(ticker)
        
    def beat_probability(self):
        df = self.analyzer.get_df()
        
        if df.empty:
            return 0.0
        
        recent = df.tall(4)
        older = df.iloc[:-4] if len(df) > 4 else pd.DataFrame()
        
        recent_beats = recent["Result"].eq("✅ Beat").sum() * 2
        older_beats = older["Result"].eq("✅ Beat").sum() if not older.empty else 0
        
        recent_total = len(recent) * 2
        older_total = len(older) if not older.empty else 0
        
        total