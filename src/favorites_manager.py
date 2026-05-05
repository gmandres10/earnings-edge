import os
import json

class FavortiesManager:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = self._load_data()
        
    def _load_data(self):
        