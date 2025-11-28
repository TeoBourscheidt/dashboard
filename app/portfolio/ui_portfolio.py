import streamlit as st
from portfolio.data.fetch_api import fetch_prices
from portfolio.analytics.portfolio_sim import simulate_portfolio
from portfolio.analytics.correlation import correlation_matrix

def portfolio_page():
    st.title("Portfolio Analysis")

    assets = st.multiselect("Choose assets", ["AAPL", "TSLA", "BTC-USD", "EURUSD=X"], default=["AAPL","TSLA","BTC-USD"])
    df = fetch_prices(assets)

    st.line_chart(df)

    weights = {asset: 1/len(assets) for asset in assets}

    portfolio = simulate_portfolio(df, weights)
    corr = correlation_matrix(df)

    st.subheader("Portfolio Value")
    st.line_chart(portfolio)

    st.subheader("Correlation Matrix")
    st.dataframe(corr)
