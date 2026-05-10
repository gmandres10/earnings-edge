"""Heuristic beat outlook and shallow options-implied move from Yahoo Finance."""

import pandas as pd
import yfinance as yf


class Predictor:
    """Combines cached earnings history with live quote/options where requested.

    ``beat_probability`` and ``prediction_label`` use only ``analyzer``.
    ``implied_move`` and ``next_earnings_date`` call Yahoo (network-bound).
    """

    def __init__(self, ticker, analyzer):
        self.ticker = ticker
        self.analyzer = analyzer
        self._stock = yf.Ticker(ticker)

    def beat_probability(self):
        """Weighted beat rate: last 4 quarters count double vs older quarters."""
        df = self.analyzer.get_df()

        if df.empty:
            return 0.0

        recent = df.tail(4)
        older = df.iloc[:-4] if len(df) > 4 else pd.DataFrame()

        recent_beats = recent["Result"].eq("✅ Beat").sum() * 2
        older_beats = older["Result"].eq("✅ Beat").sum() if not older.empty else 0

        recent_total = len(recent) * 2
        older_total = len(older) if not older.empty else 0

        total_weight = recent_total + older_total
        total_beats = recent_beats + older_beats

        if total_weight == 0:
            return 0.0

        return (total_beats / total_weight) * 100

    def implied_move(self):
        """Rough straddle-implied pct move: ATM call+put ``lastPrice`` / spot."""
        try:
            current_price = self._stock.info.get("currentPrice") or self._stock.info.get(
                "regularMarketPrice"
            )

            if not current_price:
                return None

            expirations = self._stock.options
            if not expirations:
                return None

            expiry = expirations[0]
            chain = self._stock.option_chain(expiry)

            calls = chain.calls
            puts = chain.puts

            if calls.empty or puts.empty:
                return None

            calls["diff"] = (calls["strike"] - current_price).abs()
            atm_call = calls.loc[calls["diff"].idxmin()]

            puts["diff"] = (puts["strike"] - current_price).abs()
            atm_put = puts.loc[puts["diff"].idxmin()]

            straddle_price = atm_call["lastPrice"] + atm_put["lastPrice"]
            implied_move_pct = (straddle_price / current_price) * 100

            return round(implied_move_pct, 2)

        except Exception:
            return None

    def prediction_label(self):
        """Bucketed copy line for UI from ``beat_probability()``."""
        prob = self.beat_probability()
        if prob >= 70:
            return "🟢 High Probability of Beat"
        if prob >= 45:
            return "🟡 Coin Flip"
        return "🔴 Likely Miss"

    def next_earnings_date(self):
        """Earliest scheduled earnings strictly on/after *now* in the index TZ."""
        try:
            df = self._stock.earnings_dates
            if df is None or df.empty:
                return None

            today = pd.Timestamp.now(tz=df.index.tz)
            future_dates = df[df.index >= today]

            if future_dates.empty:
                return None

            return future_dates.index.min()
        except Exception:
            return None
