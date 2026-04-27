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
    page_title="Earnings Analyzer",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)