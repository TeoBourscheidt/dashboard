# single_asset/ui_single_asset.py

def run_ui_single_asset():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    import datetime as dt
    import numpy as np

    from single_asset.data.fetch_api import fetch_price, fetch_data
    from single_asset.data.preprocess import clean_data
    from single_asset.strategies.momentum import run_momentum
    from single_asset.strategies.buy_and_hold import buy_and_hold
    from single_asset.analytics.metrics import sharpe, max_drawdown, portfolio_return, CAGR, vol_annual
    from single_asset.analytics.forecast import auto_arima_forecast


        # --- Initialisation session_state ---
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False

    # --- Paramètres dates côte à côte ---
    #st.subheader("Analysis Period")
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

    # --- Paramètre actif ---
    asset = st.text_input(
        "Asset ticker",
        value="AAPL"
    ).strip().upper()

    # --- Bouton 1 : Download data ---
    col4, col5 = st.columns([1,4])
    with col4:
        run_download = st.button("Download data")
    with col5:
        show_forecast = st.checkbox("Show forecast")
    #data
    
    if run_download:
        # Ici tu mets ton fetch réel
        # Exemple temporaire avec données simulées
        data = fetch_data(asset,start_date, end_date)
        price=clean_data(data)

        st.session_state.data = data
        st.session_state.price = price
        st.session_state.data_loaded = True

        st.success("Data successfully downloaded.")

    

    # --- Affichage graphique SI données chargées ---
    if st.session_state.data_loaded:

        data = st.session_state.data
        price = st.session_state.price

        # Graphique prix réel

        # Si la checkbox est cochée, ajouter la prévision
        if show_forecast:
            horizon = st.number_input(
                "Forecast horizon (days)",
                min_value=1,
                max_value=365,
                value=30
            )
            # --- Générer les prédictions ---
            forecast = auto_arima_forecast(price, horizon)

            # --- Créer des séries “alignées” pour le graphique ---
            # La dernière valeur réelle sert de point de départ
            # On met NaN pour que la prédiction commence **après la dernière date réelle**
            forecast_aligned = pd.Series(
                [np.nan]*len(price) + list(forecast.values),
                index=list(price.index) + list(forecast.index)
            )

            price_aligned = pd.Series(
                list(price.values) + [np.nan]*len(forecast),
                index=list(price.index) + list(forecast.index)
            )

            # --- Tracer avec Plotly ---
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=price_aligned.index,
                y=price_aligned.values,
                mode='lines',
                name='Prix Réels'
            ))

            fig.add_trace(go.Scatter(
                x=forecast_aligned.index,
                y=forecast_aligned.values,
                mode='lines+markers',
                name='Prédiction',
                line=dict(color='red', dash='dash')
            ))

            fig.update_layout(
                title="Prix Réels et Prédiction",
                xaxis_title="Date",
                yaxis_title="Prix",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        else :
            fig = go.Figure()
            fig.add_trace(go.Scatter(
            x=data.index,
            y=price,
            mode="lines",
            name="Asset price"
            ))

            fig.update_layout(
                title="Asset price evolution",
                xaxis_title="Date",
                yaxis_title="Price",
                height=500,
                margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)

                #Methode:
        
        


        strategy = st.selectbox(
            "Select investment strategy",
            ["Buy & Hold", "Momentum"],
            index=0  # valeur par défaut = "Buy & Hold"
        )

        col11, col12 = st.columns(2)
        with col11:
            capital = st.number_input(
                "Enter initial capital (€)",
                min_value=0.0,
                value=1000.0,   # float
                step=100.0,       # int
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

        # --- Bouton 2 : Run analysis ---

        rf = st.number_input(
                "Enter risk free rate(0.04)",
                min_value=0.0,
                max_value=0.2,
                value=0.08,  # valeur par défaut
                format="%.2f"
            )
        
        if strategy == "Buy & Hold":
            
            run_analysis = st.button("Run analysis")
            if run_analysis:
                
                st.success("Running strategy analysis...")
                result = buy_and_hold(price,start_ts,capital)
                
                # --- Création des colonnes avec ratio 4:1 (≈80% / 20%) ---                
                col_left, col_right = st.columns([4, 1])

                    # --- Graphique à gauche ---
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
                        name="Asset price"
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
                    vol=vol_annual(result)

                    st.metric("Sharpe Ratio", round(sharpe_ratio, 2))
                    st.metric("Max Drawdown (%)", round(max_drawdow, 2))
                    st.metric("CAGR (%)", round(cagr, 2))
                    st.metric("Annual Vol (%)", round(vol, 2))



        elif strategy == "Momentum":
            window = st.number_input(
                    "Window ",
                    min_value=0,
                    max_value=len(price),
                    value=20,  # valeur par défaut
                
                )
            run_analysis = st.button("Run analysis")
            if run_analysis:
                st.success("Running strategy analysis...")
                
                result = run_momentum(price,start_ts,capital,window)
            
                # --- Création des colonnes avec ratio 4:1 (≈80% / 20%) ---
                col_left, col_right = st.columns([4, 1])

                # --- Graphique à gauche ---
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
                        name="Asset price"
                    ))
                    fig.update_layout(
                        title="Investemment evolution",
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
                    vol=vol_annual(result)

                    st.metric("Sharpe Ratio", round(sharpe_ratio, 2))
                    st.metric("Max Drawdown (%)", round(max_drawdow, 2))
                    st.metric("CAGR (%)", round(cagr, 2))
                    st.metric("Annual Vol (%)", round(vol, 2))






    # --- Message avant download ---
    if not st.session_state.data_loaded and not run_download:
        st.info("Please enter parameters and click 'Download data' to fetch the asset price.")