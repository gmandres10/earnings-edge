"""Utilities for cleaning and analyzing earnings results data."""

import pandas as pd


class EarningsAnalyzer:
    """Analyze historical earnings surprises for a given ticker."""

    def __init__(self, raw_df):
        """Build the analyzer from a raw earnings DataFrame."""
        self.df = self._clean_data(raw_df)

    def _clean_data(self, df):
        """Prepare earnings data and derive beat/miss and surprise metrics."""
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
        """Return the cleaned earnings DataFrame."""
        return self.df

    def beat_rate(self):
        """Return the percentage of quarters that beat estimates."""
        return self._beat_rate

    def average_surprise(self):
        """Return the average earnings surprise percentage."""
        return self.df["Surprise %"].mean()

    def best_quarter(self):
        """Return the strongest quarter by surprise percentage."""
        return self.df["Surprise %"].max()

    def worst_quarter(self):
        """Return the weakest quarter by surprise percentage."""
        return self.df["Surprise %"].min()

    def quarters_analyzed(self):
        """Return the total number of analyzed quarters."""
        return len(self.df)
