# single_asset/ui_single_asset.py
import streamlit as st    
import pandas as pd
import plotly.graph_objects as go
import datetime as dt
import numpy as np

from single_asset.data.fetch_api import fetch_price, fetch_data
from single_asset.data.preprocess import clean_data
from single_asset.strategies.momentum import run_momentum
from single_asset.strategies.buy_and_hold import buy_and_hold
from single_asset.analytics.metrics import sharpe, max_drawdown, portfolio_return, CAGR, vol_annual,sortino_ratio,value_at_risk
from single_asset.analytics.forecast import auto_arima_forecast

def run_ui_single_asset():
    ###################"################"
    # Parameters

    today = dt.date.today()
    default_start = today - dt.timedelta(days=365)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start date",
            value=default_start,
            max_value=today
        )
    with col2:
        end_date = st.date_input(
            "End date",
            value=today,
            min_value=start_date,
            max_value=today
        )

    asset = st.text_input(
        "Asset ticker",
        value="AAPL"
    ).strip().upper()

    strategy = st.selectbox(
            "Select investment strategy",
            ["Buy & Hold", "Momentum"],
            index=0  # valeur par défaut = "Buy & Hold"
        )

    col11, col12,col13 = st.columns(3)
    with col11:
        capital = st.number_input(
                "Enter initial capital (€)",
                min_value=0.0,
                value=1000.0,   # float
                step=100.0,       # int
                format="%.2f"
            )
    with col13:
        rf = st.number_input(
                "Enter risk free rate(0.04)",
                min_value=0.0,
                max_value=0.2,
                value=0.08,  # valeur par défaut
                format="%.2f"
            )
    with col12:
        start_date_invest = st.date_input(
                "Start Invest",
                value=start_date,
                min_value=start_date,
                max_value=today
            )
        start_ts = pd.Timestamp(start_date_invest)



    show_forecast = st.checkbox("Show forecast")

    ########################"
    # Data
    data = fetch_data(asset,start_date, end_date)
    price = clean_data(data)

    forecast_df = None
    price_extended = price.copy() 
    if show_forecast:
        horizon = st.number_input(
                "Forecast horizon (days)",
                min_value=1,
                max_value=90,
                value=30
            )
        
        with st.spinner("Calculating forecast..."):
            forecast_df = auto_arima_forecast(price, horizon)
            
            price_extended = pd.concat([price, forecast_df["forecast"]])

    if strategy == "Buy & Hold":
            
        result = buy_and_hold(price,start_ts,capital)
        col_left, col_right = st.columns([4, 1])
        with col_left:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                    x=result.index,
                    y=result["Portefeuille"],
                    mode="lines",
                    name="Investement Strategy"
                ))
            fig.add_trace(go.Scatter(
                x=data.index,
                y=price,
                mode="lines",
                name=asset
            ))
            fig.update_layout(
                    title="Investement evolution",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    height=500
                )
            st.plotly_chart(fig, use_container_width=True)

                    # --- Metrics à droite ---
        with col_right:
                    
            result=result[result["Portefeuille"]!=0]
            result=portfolio_return(result)
            result.dropna(inplace=True)

            max_drawdow=max_drawdown(result)
            cagr=CAGR(result)
            sharpe_ratio=sharpe(result,rf)
            sortino_val = sortino_ratio(result, rf=rf)  # ✅ Nouveau
            
            vol = vol_annual(result) * 100  # En %
            
            var_95 = value_at_risk(result, confidence=0.95) 

            
            st.metric("CAGR (%)", f"{cagr:.2f}")
            st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
            st.metric("Sortino Ratio", f"{sortino_val:.2f}")  # ✅ Nouveau
            st.metric("Volatility (%)", f"{vol:.2f}")
            st.metric("Max Drawdown (%)", f"{max_drawdow:.2f}")
            st.metric("VaR 95% (%)", f"{var_95:.2f}")  # Bonus


    elif strategy == "Momentum":
        window = st.number_input(
                    "Window ",
                    min_value=0,
                    max_value=len(price),
                    value=20,  # valeur par défaut
                
                )
        result = run_momentum(price,start_ts,capital,window)
        col_left, col_right = st.columns([4, 1])
        with col_left:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=result.index,
                y=result["Portefeuille"],
                mode="lines",
                name="Investement Strategy"
            ))
            fig.add_trace(go.Scatter(
                x=data.index,
                y=price,
                mode="lines",
                name=asset
            ))
            fig.update_layout(
                title="Investemment evolution",
                xaxis_title="Date",
                yaxis_title="Price",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

            with col_right:
                result=result[result["Portefeuille"]!=0]
                result=portfolio_return(result)
                result.dropna(inplace=True)

                max_drawdow=max_drawdown(result)
                cagr=CAGR(result)
                sharpe_ratio=sharpe(result,rf)
                sortino_val = sortino_ratio(result, rf=rf)  # ✅ Nouveau
                
                vol = vol_annual(result) * 100  # En %
               
                var_95 = value_at_risk(result, confidence=0.95) 

                st.metric("CAGR (%)", f"{cagr:.2f}")
                st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
                st.metric("Sortino Ratio", f"{sortino_val:.2f}")  # ✅ Nouveau
                
                st.metric("Volatility (%)", f"{vol:.2f}")
                st.metric("Max Drawdown (%)", f"{max_drawdow:.2f}")
                
                st.metric("VaR 95% (%)", f"{var_95:.2f}")  # Bonus


