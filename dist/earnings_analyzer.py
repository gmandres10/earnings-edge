"""Transform raw Yahoo Finance earnings tables into labeled surprise metrics."""

import pandas as pd


class EarningsAnalyzer:
    """Compute beat/miss labels and summary stats from quarterly earnings rows.

    Expects the same columns as ``yfinance.Ticker.earnings_dates`` after ingestion:
    datetime index ``Earnings Date``, ``EPS Estimate``, ``Reported EPS``, optional
    ``Surprise(%)`` from Yahoo (dropped here in favor of a derived column).
    """

    def __init__(self, raw_df):
        """Normalize *raw_df* into ``self.df`` (sorted newest-first by earnings date)."""
        self.df = self._clean_data(raw_df)

    def _clean_data(self, df):
        """Drop incomplete rows, compute surprise % and human-readable beat/miss."""
        df = df.dropna(subset=["EPS Estimate", "Reported EPS"]).copy()

        df = df.sort_index(ascending=False)
        df["Surprise %"] = (
            (df["Reported EPS"] - df["EPS Estimate"]) / df["EPS Estimate"].abs()
        ) * 100

        df["Beat"] = df["Surprise %"] > 0
        df["Result"] = df["Beat"].map({True: "✅ Beat", False: "❌ Miss"})

        self._beat_rate = df["Beat"].mean() * 100

        df = df.drop(columns=["Surprise(%)"], errors="ignore")
        df = df.drop(columns=["Beat"], errors="ignore")

        return df

    def get_df(self):
        """Return the cleaned dataframe (DatetimeIndex preserved)."""
        return self.df

    def beat_rate(self):
        """Percentage of quarters with positive EPS surprise."""
        return self._beat_rate

    def average_surprise(self):
        """Mean of ``Surprise %`` across retained quarters."""
        return self.df["Surprise %"].mean()

    def best_quarter(self):
        """Largest ``Surprise %``."""
        return self.df["Surprise %"].max()

    def worst_quarter(self):
        """Smallest ``Surprise %``."""
        return self.df["Surprise %"].min()

    def quarters_analyzed(self):
        """Row count after cleaning."""
        return len(self.df)
