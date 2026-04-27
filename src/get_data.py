import yfinance as yf
import pandas as pd

class GetData:
    
    def __init__(self, ticker):
        self.ticker = str(ticker.upper().strip())
        self._stock = yf.Ticker(self.ticker)
        
    def get_earnings_result(self):
        df = self._stock.earnings_dates
        if df is None or df.empty:
            return ValueError(f"No earnings data found for ticker {self.ticker}.")
        return df
    
    def get_company_name(self):
        info = self._stock.info
        if 'longName' not in info:
            return ValueError(f"Company name not found for ticker {self.ticker}.")
        return info['longName']        