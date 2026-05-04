import pandas as pd

class EarningsAnalyzer:
    
    def __init__(self, raw_df):
        self.df = self._clean_data()
        
    