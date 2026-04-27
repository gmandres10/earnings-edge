import yfinance as yf
import pandas as pd

class GetData:
    
    def __init__(self, ticker):
        self.ticker = str(ticker.upper().strip())
        self._