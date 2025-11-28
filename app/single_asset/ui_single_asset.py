# app/single_asset/ui_single_asset.py
import streamlit as st
from single_asset.data.fetch_api import fetch_price
from single_asset.analytics.backtest import run_backtest
from single_asset.analytics.metrics import compute_metrics
from single_asset.strategies.buy_and_hold import buy_and_hold

def single_asset_page():
    st.title("Single Asset Analysis")

    asset = st.selectbox("Choose asset", ["AAPL", "BTC-USD", "EURUSD=X"])
    
    df = fetch_price(asset)

    if df is None:
        st.error("Data unavailable.")
        return

    st.line_chart(df["close"])

    st.subheader("Strategy")
    strategy = st.selectbox("Strategy:", ["Buy & Hold"])

    if strategy == "Buy & Hold":
        strat_series = buy_and_hold(df["close"])

    results = run_backtest(df["close"], strat_series)
    metrics = compute_metrics(strat_series)

    st.line_chart(results)
    st.json(metrics)
