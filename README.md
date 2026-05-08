📈 Earnings Edge
A Streamlit dashboard that pulls live earnings history for any stock ticker and analyzes how the company has historically performed around earnings events. Search any ticker and instantly see whether the company consistently beats or misses analyst estimates, how large the surprises have been, and what the options market is implying for the next report.

🚀 How to Run
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run dist/main.py

✨ Features

🔍 Live Ticker Search — search any publicly traded stock (AAPL, TSLA, NVDA, etc.)
📊 EPS Surprise Chart — color-coded bar chart showing beat (green) vs miss (red) per quarter
📈 KPI Metrics — beat rate, average EPS surprise, best and worst quarter at a glance
🔮 Earnings Prediction — weighted beat probability with recent quarters counting double
📉 Implied Move — expected price move pulled live from the options market
⭐ Favorites — save tickers with personal notes, persisted between sessions
📋 Raw Data Table — full earnings history with EPS estimate, reported EPS, surprise %, and result
💾 Persistent Storage — favorites and notes saved to disk as JSON, survive app restarts


🖥️ App Preview
SectionDescriptionSidebarTicker search, Analyze button, saved favorites listKPI RowBeat rate, avg surprise, best/worst quarterEPS Surprises TabInteractive bar chart of last 12 quartersPrediction TabBeat probability, verdict, implied move from optionsEarnings History TabFull raw data tableNotes SectionPersonal notes saved per ticker

📁 File Structure
earnings-edge/
│
├── README.md                   ← You are here
├── demo.mp4                    ← App demo video
│
├── src/                        ← Development zone
│   ├── main.py                 ← Streamlit app entry point
│   ├── earnings_analyzer.py    ← Data cleaning & EPS calculations
│   ├── favorites_manager.py    ← Read/write favorites to disk
│   ├── predictor.py            ← Beat probability & implied move
│   └── data/
│       └── favorites.json      ← Saved tickers and notes (auto-generated)
│
└── dist/                       ← Production zone (graded version)
    ├── main.py                 ← Stable copy of src/main.py
    ├── earnings_analyzer.py    ← Stable copy
    ├── favorites_manager.py    ← Stable copy
    ├── predictor.py            ← Stable copy
    └── data/
        └── favorites.json      ← Stable copy of saved data

🗂️ What Each File Does
FilePurposemain.pyStreamlit UI — sidebar, charts, tabs, session stateearnings_analyzer.pyCleans raw yfinance data, computes surprise %, beat/missfavorites_manager.pySaves and loads favorites + notes from favorites.jsonpredictor.pyCalculates weighted beat probability and options implied movedata/favorites.jsonAuto-generated JSON file storing saved tickers and notes

🛠️ Tech Stack
ToolPurposePython 3.xCore languageStreamlitWeb app frameworkyfinanceLive stock & options data from Yahoo FinancePandasData cleaning and manipulationMatplotlibEPS surprise bar chartJSONPersistent storage for favorites and notes

📦 Dependencies
streamlit
yfinance
pandas
matplotlib
lxml
Install all at once:
bashpip install streamlit yfinance pandas matplotlib lxml

💡 User Guide

Search a ticker — type a stock symbol in the sidebar (e.g. AAPL) and click Analyze Earnings
Read the KPIs — check beat rate and average surprise at the top
Explore the chart — green bars = beat, red bars = miss, labels show exact surprise %
Check the prediction — click the Prediction tab for beat probability and implied move
Save a favorite — scroll down, write a note, and click ⭐ Add to Favorites
Load a favorite — click any saved ticker in the sidebar to instantly reload its analysis


🔮 Next Steps

 Slider to control how many quarters appear on the chart
 Price reaction chart — show how the stock moved the day after earnings
 @st.cache_data to avoid re-fetching the same ticker on every rerun
 Comparison mode — analyze two tickers side by side
 Export to CSV button for the earnings history table
