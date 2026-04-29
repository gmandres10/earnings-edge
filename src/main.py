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
                ss.df = df    
        except Exception as e:
            st.error(f"Error : {e}")
            ss.df = None
            
if ss.df is None:
    st.title("Earnings Edge")
    st.write("Enter a ticker in the sidebar and click Analyze to get started")
else:
    st.title(f"Earnings Analysis for {ss.company_name} ({ss.ticker})")
    st.write     

st.title("Earnings Edge")
st.write("Enter a ticker and click Analyze to get started")
