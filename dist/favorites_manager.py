"""JSON-backed favorites: ticker metadata plus a serialized earnings dataframe snapshot."""

import json
import os
from datetime import datetime

import pandas as pd


class FavoritesManager:
    """Load/save ``favorites.json`` with notes and cached analyzer-ready history.

    On ``save``, the analyzer dataframe is reset-indexed so ``Earnings Date`` becomes
    strings for JSON serialization. ``get_cached_df`` reverses that for in-memory use.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self._data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _write(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def save(self, ticker, company_name, beat_rate, avg_surprise, df, note=""):
        """Persist ticker metadata and a row-oriented copy of ``df``.

        ``df`` must be the cleaned dataframe from ``EarningsAnalyzer`` (DatetimeIndex).
        ``round`` guarantees JSON-friendly plain floats for summary fields.
        """
        df_copy = df.reset_index()
        df_copy["Earnings Date"] = df_copy["Earnings Date"].astype(str)
        self._data[ticker] = {
            "company_name": company_name,
            "beat_rate": round(beat_rate, 1),
            "avg_surprise": round(avg_surprise, 1),
            "note": note,
            "date_saved": datetime.now().strftime("%B %d, %Y"),
            "data": df_copy.to_dict(orient="records"),
        }
        self._write()

    def remove(self, ticker):
        """Delete a ticker from the store."""
        self._data.pop(ticker, None)
        self._write()

    def get_note(self, ticker):
        return self._data.get(ticker, {}).get("note", "")

    def get_all(self):
        """All favorite ticker symbols (dict keys)."""
        return list(self._data.keys())

    def get_info(self, ticker):
        """Full entry for sidebar display (includes serialized ``data`` list)."""
        return self._data.get(ticker, {})

    def get_cached_df(self, ticker):
        """Rebuild the indexed dataframe from JSON records, or ``None`` if missing/invalid."""
        info = self._data.get(ticker, {})
        records = info.get("data", None)
        if not records:
            return None
        try:
            df = pd.DataFrame(records)
            df["Earnings Date"] = pd.to_datetime(df["Earnings Date"])
            df = df.set_index("Earnings Date")
            return df
        except Exception:
            return None

    def is_favorite(self, ticker):
        return ticker in self._data
