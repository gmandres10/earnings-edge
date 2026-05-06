import yfinance as yf
import pandas as pd

class Predictor:
    def __init__(self, ticker, analyzer):
        self.ticker = ticker
        self.analyzer = analyzer
        self._stock = yf.Ticker(ticker)
        
    def beat_probability(self):
        df = self.analyzer.get_df()
        
        if df.empty:
            return 0.0
        
        recent = df.tall(4)
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
        try:
            current_price = self._stock.info.get("currentPrice") or self._stock.info.get("regularMarketPrice")
            
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
        prob = self.beat_probability()
        if prob >= 70:
            return "🟢 High Probability of Beat"
        elif prob >= 45:
            return "🟡 Coin Flip"
        else:
            return "🔴 Likely Miss"