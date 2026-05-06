"""Data access wrapper around yfinance ticker endpoints."""

import pandas as pd
import yfinance as yf


class GetData:
    """Fetch company and earnings data for a ticker."""

    def __init__(self, ticker):
        """Create a yfinance ticker client from normalized input."""
        self.ticker = str(ticker.upper().strip())
        self._stock = yf.Ticker(self.ticker)

    def get_earnings_result(self):
        """Return the earnings dates table or a ValueError object."""
        df = self._stock.earnings_dates
        if df is None or df.empty:
            return ValueError(f"No earnings data found for ticker {self.ticker}.")
        return df

    def get_company_name(self):
        """Return the long company name or a ValueError object."""
        info = self._stock.info
        if "longName" not in info:
            return ValueError(f"Company name not found for ticker {self.ticker}.")
        return info["longName"]

    def get_current_stock_price(self):
        """Return the current stock price or a ValueError object."""
        info = self._stock.info
        if "currentPrice" not in info:
            return ValueError(
                f"Current stock price not found for ticker {self.ticker}."
            )
        return info["currentPrice"]
