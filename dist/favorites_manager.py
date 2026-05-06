"""Persistence helpers for favorite tickers and user notes."""

import json
import os


class FavoritesManager:
    """Store and manage favorite stock tickers in a JSON file."""

    def __init__(self, filepath):
        """Initialize manager and load favorites from disk."""
        self.filepath = filepath
        self._data = self._load_data()

    def _load_data(self):
        """Load saved favorites data, returning an empty dict on failure."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _write(self):
        """Persist in-memory favorites to disk."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self._data, f, indent=2)

    def save(self, ticker, note=""):
        """Save or update a ticker and its note."""
        self._data[ticker] = {"note": note}
        self._write()

    def remove(self, ticker):
        """Remove a ticker from favorites."""
        self._data.pop(ticker, None)
        self._write()

    def get_note(self, ticker):
        """Return the saved note for a ticker, if present."""
        return self._data.get(ticker, {}).get("note", "")

    def get_all(self):
        """Return all favorite ticker symbols."""
        return list(self._data.keys())

    def is_favorite(self, ticker):
        """Return whether the ticker is in favorites."""
        return ticker in self._data
