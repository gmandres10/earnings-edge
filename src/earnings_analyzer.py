import pandas as pd

class EarningsAnalyzer:
    
    def __init__(self, raw_df, num_quarters = 4):
        self.num_quarters = num_quarters
        self.df = self._clean(raw_df)
        
    