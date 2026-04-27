import yfinance as yf
import pandas as pd

class GetData:
    
    def __init__(self, ticker):
        self.ticker = str(ticker.upper().strip())
        self._stock = yf.Ticker(self.ticker)
        
    def get_earnings_result(self):
        df = self._stock.earnings