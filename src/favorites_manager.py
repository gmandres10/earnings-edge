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