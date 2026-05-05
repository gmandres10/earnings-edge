import yfinance as yf
import pandas as pd

class Predictor:
    def __init__(self, ticker, analyzer):
        self.ticker = ticker
        self.analyzer = analyzer
        self._stock = yf.Ticker(ticker)
        
    