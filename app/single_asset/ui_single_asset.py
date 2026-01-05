# single_asset/ui_single_asset.py
import streamlit as st    
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime as dt
import numpy as np

from single_asset.data.fetch_api import fetch_price, fetch_data
from single_asset.data.preprocess import clean_data
from single_asset.strategies.momentum import run_momentum
from single_asset.strategies.DCA import DCA
from single_asset.strategies.buy_and_hold import buy_and_hold
from single_asset.analytics.metrics import sharpe, max_drawdown, portfolio_return, CAGR, vol_annual,sortino_ratio,value_at_risk
from single_asset.analytics.forecast import auto_arima_forecast

def run_ui_single_asset():
    ###################"################"
    # Parameters generaux de la strategie

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
    st.text("Example of tickets : Bitcoin : BTC-USD , Apple : AAPL , S&P 500 : ^GSPC , OR : GC=F.")
    ########################"
    # On charge les data
    data = fetch_data(asset,start_date, end_date)
    price = clean_data(data)


    ################""
    # On ajoute la possibilite de la prediction sur l'asset
    forecast_df = None
    price_extended = price.copy() 
    c1, c2 = st.columns([1,4])

    with c1:
        show_forecast = st.checkbox("Show forecast")
    if show_forecast:
        with c2:
            horizon = st.number_input(
                "Forecast horizon (days)",
                min_value=1,
                max_value=90,
                value=30
            )
        with c1:
            with st.spinner("Calculating forecast..."):
                forecast_df = auto_arima_forecast(price, horizon)
                price_extended = pd.concat([price, forecast_df["forecast"]])


    ########################
    # Choix de la strategie et paramatre

    strategy = st.selectbox(
        "Select investment strategy",
        ["Buy & Hold", "Momentum","DCA – Dollar Cost Averaging"],
        index=0 
    )

    col11, col12,col13 = st.columns(3)
    with col11:
        capital = st.number_input(
            "Enter initial capital (€)",
            min_value=0.0,
            value=1000.0, 
            step=100.0
        )
    with col13:
        rf = st.number_input(
            "Enter risk free rate(%)",
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

    
    #########################
    # Strategy
    if strategy == "Buy & Hold": #premier strategie
        
        #on charge les valeurs du portefeuille
        result = buy_and_hold(price_extended,start_ts,capital)

        #on trace le graphe asset et portefeuille
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=result.index,
            y=result["Portefeuille"],
            mode="lines",
            name="Investement Strategy"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=data.index,
            y=price,
            mode="lines",
            name=asset
        ), secondary_y=True)
        if show_forecast: # on rajoute la prediction si elle est selectionner
            fig.add_trace(go.Scatter(
                x=forecast_df["forecast"].index,
                y=forecast_df["forecast"],
                mode="lines",
                name="Prediction"
            ), secondary_y=True)
        fig.update_yaxes(title_text="Portfolio Value", secondary_y=False)
        fig.update_yaxes(title_text=f"{asset} Price", secondary_y=True)
        fig.update_layout(
            title="Investement evolution",
            xaxis_title="Date",
            height=500  
        )
        st.plotly_chart(fig, use_container_width=True)

        ################
        #Metrics
        # calcul
        result=result[result["Portefeuille"]!=0]
        result=portfolio_return(result)
        result.dropna(inplace=True)
        max_drawdow=max_drawdown(result)
        cagr=CAGR(result)
        sharpe_ratio=sharpe(result,rf)
        sortino_val = sortino_ratio(result, rf=rf)
        vol = vol_annual(result) * 100  
        var_95 = value_at_risk(result, confidence=0.95) 

        #affichage
        c1,c2,c3,c4,c5,c6=st.columns(6)
        with c1:
            st.metric("CAGR (%)", f"{cagr:.2f}")
        with c2:
            st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
        with c3:
            st.metric("Sortino Ratio", f"{sortino_val:.2f}")  
        with c4:
            st.metric("Volatility (%)", f"{vol:.2f}")
        with c5:
            st.metric("Max Drawdown (%)", f"{max_drawdow:.2f}")
        with c6:
            st.metric("VaR 95% (%)", f"{var_95:.2f}")  


    elif strategy == "Momentum": # deuxieme strategie
        window = st.number_input(
            "Window ",
            min_value=0,
            max_value=len(price),
            value=20,
        )

        result = run_momentum(price_extended,start_ts,capital,window)

        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=result.index,
            y=result["Portefeuille"],
            mode="lines",
            name="Investement Strategy"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=data.index,
            y=price,
            mode="lines",
            name=asset,
        ), secondary_y=True)
        if show_forecast:
            fig.add_trace(go.Scatter(
                x=forecast_df["forecast"].index,
                y=forecast_df["forecast"],
                mode="lines",
                name="Prediction",
            ), secondary_y=True)
        fig.update_yaxes(title_text="Portfolio Value", secondary_y=False)
        fig.update_yaxes(title_text=f"{asset} Price", secondary_y=True)
        fig.update_layout(
            title="Investemment evolution",
            xaxis_title="Date",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        result=result[result["Portefeuille"]!=0]
        result=portfolio_return(result)
        result.dropna(inplace=True)
        max_drawdow=max_drawdown(result)
        cagr=CAGR(result)
        sharpe_ratio=sharpe(result,rf)
        sortino_val = sortino_ratio(result, rf=rf)
        vol = vol_annual(result) * 100
        var_95 = value_at_risk(result, confidence=0.95) 

        c1,c2,c3,c4,c5,c6=st.columns(6)
        with c1:
            st.metric("CAGR (%)", f"{cagr:.2f}")
        with c2:
            st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
        with c3:
            st.metric("Sortino Ratio", f"{sortino_val:.2f}") 
        with c4:
            st.metric("Volatility (%)", f"{vol:.2f}")
        with c5:
            st.metric("Max Drawdown (%)", f"{max_drawdow:.2f}")
        with c6:
            st.metric("VaR 95% (%)", f"{var_95:.2f}")


    elif strategy == "DCA – Dollar Cost Averaging": # troisieme strategie
        cc1,cc2=st.columns(2)
        with cc1:
            Amount = st.number_input(
                "Amount ReInvest ",
                min_value=0,
                max_value=int(capital),
                value=100
            )
        with cc2:
            freq = st.number_input(
                "Freq of ReInvest ",
                min_value=0,
                max_value=len(data),
                value=15
            )

        result, average_buy,size_invest = DCA(price_extended,start_date_invest,capital,freq,Amount)
        
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=result.index,
            y=result["Portefeuille"],
            mode="lines",
            name="Investement Strategy"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=data.index,
            y=price,
            mode="lines",
            name=asset
        ), secondary_y=True)
        if show_forecast:
            fig.add_trace(go.Scatter(
                x=forecast_df["forecast"].index,
                y=forecast_df["forecast"],
                mode="lines",
                name="Prediction"
            ), secondary_y=True)
        fig.update_yaxes(title_text="Portfolio Value", secondary_y=False)
        fig.update_yaxes(title_text=f"{asset} Price", secondary_y=True)
        fig.update_layout(
            title="Investement evolution",
            xaxis_title="Date",
            height=500  
        )
        st.plotly_chart(fig, use_container_width=True)
  
        result=result[result["Portefeuille"]!=0]
        result=portfolio_return(result)
        result.dropna(inplace=True)
        max_drawdow=max_drawdown(result)
        sortino_val = sortino_ratio(result, rf=rf) 
        V_f = result["Portefeuille"].iloc[-1]
        total_invested = size_invest
        total_return = (V_f - total_invested) / total_invested
        
        c1,c2,c3,c4,c5=st.columns(5)
        with c1:
            st.metric("Sortino Ratio", f"{sortino_val:.2f}") 
        with c2:
            st.metric("Max Drawdown (%)", f"{max_drawdow:.2f}")
        with c3:
            st.metric("Value Invest : ",size_invest)
        with c4:
            st.metric("Average buying (€): ",round(average_buy,2))
        with c5:
            st.metric("Total Return (%) : ",round(total_return*100,2))



