"""Streamlit UI for analyzing earnings performance and predictions."""

import json
import os

import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

from earnings_analyzer import EarningsAnalyzer
from favorites_manager import FavoritesManager
from predictor import Predictor

APP_PATH = os.path.dirname(os.path.abspath(__file__))


def get_data_path(filename: str) -> str:
    """Return the absolute path for an app data file."""
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

if "analyzer" not in ss:
    ss.analyzer = None

if "auto_analyze" not in ss:
    ss.auto_analyze = False

if "predictor" not in ss:
    ss.predictor = None

favorites = FavoritesManager(get_data_path("favorites.json"))

with st.sidebar:
    st.title("📈 Earnings Edge")
    ticker_input = st.text_input(
        "Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL): ",
        value=ss.ticker,
    ).upper().strip()
    analyze_button = st.button("Analyze Earnings", use_container_width=True, type="primary")
    st.divider()
    st.subheader("⭐ Favorites")
    favorites_list = favorites.get_all()
    if favorites_list:
        for fav in favorites_list:
            col_a, col_b = st.columns([4, 1])
            with col_a:
                if st.button(fav, use_container_width=True, key=f"fav_{fav}"):
                    ss.ticker = fav
                    ss.df = None
                    ss.analyzer = None
                    ss.auto_analyze = True
                    st.rerun()
            with col_b:
                if st.button("❌", key=f"del_{fav}"):
                    favorites.remove(fav)
                    st.rerun()
    else:
        st.caption(
            "No favorites yet. Analyze a stock and click the ⭐ button to add it here."
        )

if (analyze_button and ticker_input) or ss.auto_analyze:
    ss.auto_analyze = False
    if analyze_button:
        ss.ticker = ticker_input

    with st.spinner(f"Fetching data for {ticker_input}..."):
        try:
            stock = yf.Ticker(ss.ticker)
            ss.company_name = stock.info.get("longName", ss.ticker)
            df = stock.earnings_dates

            if df is None or df.empty:
                st.warning(f"No earnings data found for ticker {ss.ticker}")
                ss.df = None
            else:
                analyzer = EarningsAnalyzer(df)
                ss.df = analyzer.get_df()
                ss.analyzer = analyzer
                ss.predictor = Predictor(ss.ticker, analyzer)
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

    tab1, tab2, tab3 = st.tabs(
        ["EPS Surprise % Per Quarter", "Earnings History", "Prediction"]
    )

    with tab1:
        st.write("### EPS Surprise % Per Quarter")

        plot_df = ss.df.sort_index(ascending=True).tail(12)

        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")

        colors = ["#2ecc71" if r == "✅ Beat" else "#e74c3c" for r in plot_df["Result"]]
        bars = ax.bar(plot_df.index.astype(str), plot_df["Surprise %"], color=colors, width=0.6)

        ax.axhline(0, color="white", linewidth=0.8, linestyle="--", alpha=0.5)

        for bar, val in zip(bars, plot_df["Surprise %"]):
            y_pos = bar.get_height() + 0.3 if val >= 0 else bar.get_height() - 1.5
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                y_pos,
                f"{val:+.1f}%",
                ha="center",
                color="white",
                fontsize=8,
            )

        ax.set_xlabel("Earnings Date", color="white")
        ax.set_ylabel("Surprise %", color="white")
        ax.tick_params(colors="white", axis="both")
        ax.tick_params(axis="x", rotation=45)
        ax.spines[["top", "right", "left", "bottom"]].set_color("#333")
        fig.tight_layout()

        st.pyplot(fig)

        col_1, col_r = st.columns(2)
        col_1.success("✅ Beat Quarters - Reported EPS above estimate")
        col_r.error("❌ Miss Quarters - Reported EPS below estimate")

    with tab2:
        st.write("### Earnings History")
        st.dataframe(ss.df, use_container_width=True)

    with tab3:
        st.write("### Earnings Beat Prediction")

        pred = ss.predictor
        prob = pred.beat_probability()
        label = pred.prediction_label()
        move = pred.implied_move()
        date = pred.next_earnings_date()

        if date:
            st.info(f"Next Earnings Date: {date.strftime('%B %d, %Y')}")
        else:
            st.info("Next Earnings Date: Not Available")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Predicted Beat Probability", f"{prob:.0f}%")
            st.write(f"Verdict: {label}")
            st.caption(
                "Prediction based on historical earnings performance with more weight on recent quarters"
            )

        with col2:
            if move:
                st.metric("Implied Move (Next Earnings)", f"±{move:.1f}%")
                st.caption("Estimated stock price move based on current option prices")
            else:
                st.warning("Implied Move: Not Available")
        st.divider()

        st.write("### Beat Probability Explanation")
        df_display = ss.analyzer.get_df()
        recent = df_display.tail(4)
        older = df_display.iloc[:-4] if len(df_display) > 4 else None

        col_a, col_b = st.columns(2)
        with col_a:
            recent_rate = recent["Result"].eq("✅ Beat").mean() * 100
            st.metric("Recent 4 Quarters Beat Rate", f"{recent_rate:.0f}%")
        with col_b:
            if older is not None and not older.empty:
                older_rate = older["Result"].eq("✅ Beat").mean() * 100
                st.metric("Older Quarters Beat Rate", f"{older_rate:.0f}%")

    st.divider()
    st.subheader("Notes & Favorites")
    note = st.text_area("Personal Note for this Stock", value=favorites.get_note(ss.ticker))
    if st.button("⭐ Add to Favorites"):
        favorites.save(ss.ticker, note)
        st.success(f"{ss.ticker} added to favorites!")
