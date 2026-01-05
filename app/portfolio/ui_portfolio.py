import streamlit as st
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

from portfolio.analytics.correlation import correlation_matrix
from portfolio.verifcation.weight_check import check_weights
from portfolio.strategies.rebalancing import rebalancing
from portfolio.strategies.allocation import allocation_hold
from portfolio.strategies.alloc_return import rebalancing_proportional_returns
from portfolio.data.fetch_api import fetch_data_bis
from portfolio.analytics.metrics import return_portfolio,vol_portfolio,sharpe_ratio,max_draw,VaR,total_return,annualized_return,cagr
def portfolio_page():
    

    ################################## 
    # Paramètres generaux de l'investissement
    today = dt.date.today()
    default_start = today - dt.timedelta(days=365)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start date",
            value=default_start,
            max_value=today
        )
        capital = st.number_input(
            "Enter initial capital (€)",
            min_value=0.0,
            value=1000.0,    
            step=100.0,       
        )
    with col2:
        end_date = st.date_input(
            "End date",
            value=today,
            min_value=start_date,
            max_value=today
        )
        rf = st.number_input(
            "Risk free rate (%)",
            min_value=0.0,
            value=0.08,   
            max_value=0.2,       
            format="%.2f"
        )   

    
    user_input = st.text_input(
        "Enter asset tickers (comma separated)",
        value="AAPL, MSFT, GOOGL"
    )
    st.text("Example of tickets : Bitcoin : BTC-USD , Apple : AAPL , S&P 500 : ^GSPC , OR : GC=F.")
    selected_assets = [
        t.strip().upper()
        for t in user_input.split(",")
        if t.strip() != ""
    ]

    ############""
    # Choix de la strategie
    strategy = st.selectbox(
        "Select investment strategy",
        ["Custom weights and hold", "Auto ballancing","Auto balancing proportional returns"],
        index=0  
    )


    ################################################
    #Charger les data :
    data = fetch_data_bis(selected_assets,start_date, end_date)


    ###################################################"
    # Selection en fonction de la strategie :

    if strategy=="Custom weights and hold": # Premiere strategie
        st.write("For this strategy, you must choose weights, then hold these assets until the end of the investment period.")
        
        ## Choix des poids.
        cols = st.columns(len(selected_assets))
        weights = []
        for i, asset in enumerate(selected_assets):
            w = cols[i].number_input(
                label=asset,
                min_value=0.0,
                max_value=1.0,
                value=1 / len(selected_assets),
                step=0.05,
                key=f"weight_{asset}"
            )
            weights.append(w)

        # check des poids
        weights=check_weights(weights)

        #tracer des valeurs des actifs du portefeuille
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for ticket in selected_assets:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data[ticket],
                mode="lines",
                name=ticket
            ), secondary_y=True)

        #charge les valeurs du portefeuille en fonction de la methode
        portfolio = allocation_hold(data, selected_assets,weights,capital)
     
        # on trace l'evolution du portefeuille
        fig.add_trace(go.Scatter(
            x=portfolio.index,
            y=portfolio,
            mode="lines",
            name="Portfolio"
        ), secondary_y=False)
        fig.update_yaxes(title_text="Portfolio Value", secondary_y=False)
        fig.update_yaxes(title_text="Asset Price", secondary_y=True)
        fig.update_layout(
            title="Portfolio evolution (Custom Weights)",
            xaxis_title="Date",
            height=500,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    if strategy=="Auto ballancing": # deuxieme strategie
        st.write("For this strategy, you must choose weights, then we readjust the weights every X amount of time (frequency) in the portfolio.")
    
        cols = st.columns(len(selected_assets))
        weights = []
        for i, asset in enumerate(selected_assets):
            w = cols[i].number_input(
                label=asset,
                min_value=0.0,
                max_value=1.0,
                value=1 / len(selected_assets),
                step=0.05,
                key=f"weight_{asset}"
            )
            weights.append(w)
        weights=check_weights(weights)

        freq = st.number_input(
            "Freq",
            min_value=0,
            value=30,   
            max_value=int(len(data)/2)
        ) 
        
        portfolio = rebalancing(data,capital,freq,weights)

        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for ticket in selected_assets:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data[ticket],
                mode="lines",
                name=ticket
            ), secondary_y=True)

        fig.add_trace(go.Scatter(
            x=portfolio.index,
            y=portfolio,
            mode="lines",
            name="Portfolio"
        ), secondary_y=False)
        fig.update_yaxes(title_text="Portfolio Value", secondary_y=False)
        fig.update_yaxes(title_text=f"Asset Price", secondary_y=True)
        fig.update_layout(
            title="Portfolio evolution (Auto Ballancing)",
            xaxis_title="Date",
            height=500,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

   
        
    if strategy == "Auto balancing proportional returns": # troisieme strategie
        st.write("Weights are automatically recalculated every X days based on past returns.")
        
        c1,c2=st.columns(2)
        with c1 :
            freq = st.number_input(
                "Rebalancing frequency (days)",
                min_value=1,
                value=30,
                max_value=len(data)
            )
        with c2:
            lookback = st.number_input(
                "Lookback period for returns calculation (days)",
                min_value=5,
                value=30,
                max_value=len(data)
            )
        
        portfolio = rebalancing_proportional_returns(data, capital, freq, lookback)
    
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for ticket in selected_assets:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data[ticket],
                mode="lines",
                name=ticket
            ), secondary_y=True)
        fig.add_trace(go.Scatter(
            x=portfolio.index,
            y=portfolio,
            mode="lines",
            name="Portfolio"
        ), secondary_y=False)
        fig.update_yaxes(title_text="Portfolio Value", secondary_y=False)
        fig.update_yaxes(title_text=f"Asset Price", secondary_y=True)
        fig.update_layout(
            title="Portfolio evolution (Dynamic Rebalancing)",
            xaxis_title="Date",
        )
        st.plotly_chart(fig, use_container_width=True)
        
      
    #################################
    # Metrics et matrice de corrélations:
    # Calcul
    returns = return_portfolio(portfolio)
    vol = vol_portfolio(returns)
    sharpe = sharpe_ratio(returns, rf=rf)
    max_drawdown = max_draw(returns)
    Var = VaR(returns)
    total_ret = total_return(portfolio) 
    annual_ret = annualized_return(portfolio)  

    # Affichage 
    matrix,metr=st.columns(2)
    with metr :
        st.markdown("**Metrics**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Return (%)", round(total_ret, 2))
        with col2:
            st.metric("Annual Return (%)", round(annual_ret, 2))
        with col3:
            st.metric("Sharpe Ratio", round(sharpe, 2))
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("Max Drawdown (%)", round(max_drawdown * 100, 2))
        with col5:
            st.metric("Volatility (%)", round(vol * 100, 2))
        with col6:
            st.metric("VaR 95% (%)", round(Var * 100, 2))
    with matrix :
        st.markdown("**Correlation Matrix**")
        corr_matrix=correlation_matrix(data)
        st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm').format("{:.2f}"))
            
    ################
    # Comapraison entre un actif et le portefeuille
    comp_asset = st.selectbox(
        "Select asset to compare with portfolio.",
        selected_assets,
        index=0  
    )
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[comp_asset],
        mode="lines",
        name=ticket
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=portfolio.index,
        y=portfolio,
        mode="lines",
        name="Portfolio"
    ), secondary_y=False)
    fig.update_yaxes(title_text="Portfolio Value", secondary_y=False)
    fig.update_yaxes(title_text="Asset Price", secondary_y=True)
    fig.update_layout(
        title="Comparaison between "+comp_asset+" and the portfolio.",
        xaxis_title="Date",
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)