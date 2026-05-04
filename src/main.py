import os
import streamlit as st
import pandas as pd
import time 
import json
import matplotlib.pyplot as plt
import yfinance as yf


from get_data import GetData
from earnings_analyzer import EarningsAnalyzer


APP_PATH = os.path.dirname(os.path.abspath(__file__))


def get_data_path(filename: str) -> str:
    '''Returns the path to an asset file, given its filename.'''
    return os.path.join(APP_PATH, "data", filename)

st.set_page_config(
    page_title="Earnings Edge",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

ss = st.session_state

if "ticker" not in ss:
    ss.ticker = "AAPL"
    
if "df" not in ss:
    ss.df = None
    
if "company_name" not in ss:
    ss.company_name = ""

with st.sidebar:
    st.title("📈 Earnings Edge")
    ticker_input = st.text_input ("Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL): ", value=ss.ticker).upper().strip()
    analyze_button = st.button ("Analyze Earnings", use_container_width=True, type="primary")

if analyze_button and ticker_input:
    ss.ticker = ticker_input
    
    with st.spinner(f"Fetching data for {ticker_input}..."):
        try:
            stock = yf.Ticker(ss.ticker)
            ss.company_name = stock.info.get('longName', ss.ticker)
            df = stock.earnings_dates
            
            if df is None or df.empty:
                st.warning(f"No earnings data found for ticker {ss.ticker}")
                ss.df = None
            else:
                analyzer = EarningsAnalyzer(df)
                ss.df = analyzer.get_df()
                ss.analyzer = analyzer
        except Exception as e:
            st.error(f"Error : {e}")
            ss.df = None
            ss.analyzer = None
if ss.df is None:
    st.title("Earnings Edge")
    st.write("Enter a ticker in the sidebar and click Analyze to get started")
else:
    st.title(f"Earnings Analysis for {ss.company_name} ({ss.ticker})")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Beat Rate", f"{ss.analyzer.beat_rate():.0f}%")
    col2.metric("Average EPS Surprise", f"{ss.analyzer.average_surprise():+.1f}%")
    col3.metric("Best Quarter", f"{ss.analyzer.best_quarter():+.1f}%")
    col4.metric("Worst Quarter", f"{ss.analyzer.worst_quarter():+.1f}%")
    
    st.divider()
    
    st.write("### EPS Surprise % Per Quarter")
    
    fig, ax = plt.subplots(figsize=(12,5))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")
    
    colors = ["#2ecc71" if r == "✅ Beat" else "#e74c3c" for r in ss.df["Result"]]
    bars = ax.bar(ss.df.index.astype(str), ss.df["Surprise %"], color=colors, width = 0.6)
    
    ax.axhline(0)
    
    st.write("### Earnings History")
    st.dataframe(ss.df, use_container_width=True)
