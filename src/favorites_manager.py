import os
import json

class FavortiesManager:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = self._load_data()
        
    def _load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return {}
    
    def _write(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self._data, f, indent=2)
            
    def save(self, ticker, note=""):
        self._data[ticker] = {"note": note}
        self._write()
        
    def remove (self, ticker):
        self._data.pop(ticker, None)
        self._write()
        
    def get_note(self, ticker):
        return self._data.get(ticker, {}).get("note", "")
    
    def get_all(self):
        return 