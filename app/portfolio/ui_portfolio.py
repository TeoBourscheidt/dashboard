import streamlit as st
import datetime as dt
import pandas as pd
import plotly.graph_objects as go

from portfolio.strategies.rebalancing import rebalancing
from portfolio.strategies.allocation import allocation_hold
from portfolio.strategies.alloc_return import rebalancing_proportional_returns
from portfolio.data.fetch_api import fetch_data_bis
from portfolio.analytics.metrics import return_portfolio,vol_portfolio,sharpe_ratio,max_draw,VaR,total_return,annualized_return,cagr
def portfolio_page():
    

    ################################## 
    # Paramètres 
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
                value=1000.0,   # 
                step=100.0,       #
                format="%.2f"
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
    selected_assets = [
    t.strip().upper()
    for t in user_input.split(",")
    if t.strip() != ""
    ]
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

    if strategy=="Custom weights and hold": # Premier strategy
        st.write("For this strategy, you must choose weights, then hold these assets until the end of the investment period.")
        st.write("Please note that the sum of the weights must be 1; there is no margin of safety.")
        
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

        col11, col22 = st.columns(2)
            
        with col11:
            
            fig = go.Figure()
            for ticket in selected_assets:
                fig.add_trace(go.Scatter(
                x=data.index,
                y=data[ticket],
                mode="lines",
                name=ticket
                ))

            fig.update_layout(
                    title="Asset price evolution",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    height=500,
                    margin=dict(l=40, r=40, t=40, b=40)
                    )
            st.plotly_chart(fig, use_container_width=True)
            
        with col22:
            portfolio = allocation_hold(data, selected_assets,weights,capital)
            fig = go.Figure()
        
            fig.add_trace(go.Scatter(
                    x=portfolio.index,
                    y=portfolio,
                    mode="lines",
                    name="Portfolio"
                    ))

            fig.update_layout(
                        title="Portfolio evolution",
                        xaxis_title="Date",
                        yaxis_title="Value",
                        height=500,
                        margin=dict(l=40, r=40, t=40, b=40)
                    )
            st.plotly_chart(fig, use_container_width=True)

        #################################
        # Metrics :

        #################################
        # Metrics :

        returns = return_portfolio(portfolio)
        vol = vol_portfolio(returns)
        sharpe = sharpe_ratio(returns, rf=rf)
        max_drawdown = max_draw(returns)
        Var = VaR(returns)
        total_ret = total_return(portfolio)  # ✅ Nouveau
        annual_ret = annualized_return(portfolio)  # ✅ Nouveau

        # Affichage avec 6 métriques
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.metric("Total Return (%)", round(total_ret, 2))
        with col2:
            st.metric("Annual Return (%)", round(annual_ret, 2))
        with col3:
            st.metric("Sharpe Ratio", round(sharpe, 2))
        with col4:
            st.metric("Max Drawdown (%)", round(max_drawdown * 100, 2))
        with col5:
            st.metric("Volatility (%)", round(vol * 100, 2))
        with col6:
            st.metric("VaR 95% (%)", round(Var * 100, 2))


    if strategy=="Auto ballancing":
        st.write("For this strategy, you must choose weights, then we readjust the weights every X amount of time (frequency) in the portfolio.")
        st.write("Please note that the sum of the weights must be 1; there is no margin of safety.")
        
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
        freq = st.number_input(
                "Freq",
                min_value=0,
                value=30,   
                max_value=len(data)
            ) 
        portfolio = rebalancing(data,capital,freq,weights)


        col11, col22 = st.columns(2)
            
        with col11:
            
            fig = go.Figure()
            for ticket in selected_assets:
                fig.add_trace(go.Scatter(
                x=data.index,
                y=data[ticket],
                mode="lines",
                name=ticket
                ))

            fig.update_layout(
                    title="Asset price evolution",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    height=500,
                    margin=dict(l=40, r=40, t=40, b=40)
                    )
            st.plotly_chart(fig, use_container_width=True)
            
        with col22:
            fig = go.Figure()
        
            fig.add_trace(go.Scatter(
                    x=portfolio.index,
                    y=portfolio,
                    mode="lines",
                    name="Portfolio"
                    ))

            fig.update_layout(
                        title="Portfolio evolution",
                        xaxis_title="Date",
                        yaxis_title="Value",
                        height=500,
                        margin=dict(l=40, r=40, t=40, b=40)
                    )
            st.plotly_chart(fig, use_container_width=True)

   
        #################################
        # Metrics :

        returns = return_portfolio(portfolio)
        vol = vol_portfolio(returns)
        sharpe = sharpe_ratio(returns, rf=rf)
        max_drawdown = max_draw(returns)
        Var = VaR(returns)
        total_ret = total_return(portfolio)  # ✅ Nouveau
        annual_ret = annualized_return(portfolio)  # ✅ Nouveau

        # Affichage avec 6 métriques
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.metric("Total Return (%)", round(total_ret, 2))
        with col2:
            st.metric("Annual Return (%)", round(annual_ret, 2))
        with col3:
            st.metric("Sharpe Ratio", round(sharpe, 2))
        with col4:
            st.metric("Max Drawdown (%)", round(max_drawdown * 100, 2))
        with col5:
            st.metric("Volatility (%)", round(vol * 100, 2))
        with col6:
            st.metric("VaR 95% (%)", round(Var * 100, 2))
        
        
    if strategy == "Auto balancing proportional returns":
        st.write("Weights are automatically recalculated every X days based on past returns.")
        
        freq = st.number_input(
            "Rebalancing frequency (days)",
            min_value=1,
            value=30,
            max_value=len(data)
        )
        
        lookback = st.number_input(
            "Lookback period for returns calculation (days)",
            min_value=5,
            value=30,
            max_value=len(data)
        )
        
        portfolio = rebalancing_proportional_returns(data, capital, freq, lookback)
        
        # Afficher graphiques et métriques...
        col11, col22 = st.columns(2)
        
        with col11:
            fig = go.Figure()
            for ticket in selected_assets:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[ticket],
                    mode="lines",
                    name=ticket
                ))
            fig.update_layout(
                title="Asset price evolution",
                xaxis_title="Date",
                yaxis_title="Price",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col22:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=portfolio.index,
                y=portfolio,
                mode="lines",
                name="Portfolio"
            ))
            fig.update_layout(
                title="Portfolio evolution (Dynamic Rebalancing)",
                xaxis_title="Date",
                yaxis_title="Value (€)",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Métriques
        returns = return_portfolio(portfolio)
        vol = vol_portfolio(returns)
        sharpe = sharpe_ratio(returns, rf=rf)
        max_drawdown = max_draw(returns)
        Var = VaR(returns)
        total_ret = total_return(portfolio)
        annual_ret = annualized_return(portfolio)

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Total Return (%)", round(total_ret, 2))
        col2.metric("Annualized Return (%)", round(annual_ret, 2))
        col3.metric("Sharpe Ratio", round(sharpe, 2))
        col4.metric("Volatility (%)", round(vol * 100, 2))
        col5.metric("Max Drawdown (%)", round(max_drawdown * 100, 2))
        col6.metric("VaR 95% (%)", round(Var * 100, 2))