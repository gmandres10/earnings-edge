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
        
        recent = 