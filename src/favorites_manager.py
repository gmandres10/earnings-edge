import os
import json
import pandas as pd
from datetime import datetime

class FavoritesManager:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = self._load_data()
        
    def _load_data(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _write(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self._data, f, indent=2)
            
    def save(self, ticker, company_name, beat_rate, avg_surprise, df, note=""):
        df_copy = df.reset_index()
        df_copy["Earnings Date"] = df_copy["Earnings Date"].astype(str)
        self._data[ticker] = {
            "company_name": company_name,
            "beat_rate": round(beat_rate, 1),
            "avg_surprise": round(avg_surprise, 1),
            "note": note,
            "date_saved": datetime.now().strftime("%B %d, %Y"),
            "data": df_copy.to_dict(orient="records")
        }
        self._write()
        
    def remove (self, ticker):
        self._data.pop(ticker, None)
        self._write()
        
    def get_note(self, ticker):
        return self._data.get(ticker, {}).get("note", "")
    
    def get_all(self):
        return list(self._data.keys())
    
    def get_info(self,ticker):
        return self._data.get(ticker, {})
    
    def get_cached_df(self, ticker):
        info = self._data.get(ticker, {})
        records = info.get("data", None)
        if not records:
            return None
        try:
            df = pd.DataFrame(records)
            # Yahoo rows use mixed offset strings (-04/-05); vectorized parse requires a single tz.
            df["Earnings Date"] = pd.to_datetime(df["Earnings Date"], utc=True)
            df = df.set_index("Earnings Date")
            return df
        except Exception:
            return None
    def is_favorite(self, ticker):
        return ticker in self._data