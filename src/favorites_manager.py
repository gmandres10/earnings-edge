import os
import json

class FavortiesManager:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self._data