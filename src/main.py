import os
import streamlit as st
import pandas as pd
import time 
import json
import matplotlib.pyplot as plt

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
    ss.df = 

with st.sidebar:
    st.title("Earnings Edge")
    ticket_input = st.text_input ("Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL): ")
    analyze_button = st.button ("Analyze Earnings", use_container_width=True, type="primary")
    
st.title("Earnings Edge")
st.write("Enter a ticker and click Analyze to get started")
