# single_asset/ui_single_asset.py

def run_ui_single_asset():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go

    from single_asset.data.fetch_api import fetch_price
    from single_asset.data.preprocess import clean_data
    from single_asset.strategies.momentum import run_momentum
    from single_asset.strategies.buy_and_hold import run_buy_and_hold
    from single_asset.analytics.backtest import backtest_price_and_strategy
    from single_asset.analytics.metrics import sharpe_ratio, max_drawdown, volatility, cumulative_return

    # -----------------------------
    # Titre et description
    # -----------------------------
    st.markdown("Visualisez le prix réel, les performances des stratégies et les métriques financières.")

    # -----------------------------
    # A. Choix de l'asset
    # -----------------------------
    assets = ["AAPL", "MSFT", "GOOG", "SPY", "BTC-USD", "ETH-USD"]
    asset = st.selectbox("Select an Asset:", assets)

    # -----------------------------
    # B. Télécharger les données
    # -----------------------------
    with st.spinner("Fetching data..."):
        df = fetch_price(asset)
        df = clean_data(df)

    if df.empty:
        st.error(f"Impossible de charger les données pour {asset}")
        return

    st.success(f"Data for {asset} loaded: {len(df)} rows")
    st.dataframe(df.head(10))

    # -----------------------------
    # C. Choix de la stratégie
    # -----------------------------
    strategy_name = st.selectbox("Select Strategy:", ["Buy & Hold", "Momentum"])
    window = st.slider("Momentum Lookback Window:", 5, 100, value=20)

    if strategy_name == "Buy & Hold":
        strategy_df = run_buy_and_hold(df)
    else:
        strategy_df = run_momentum(df, window=window)

    # -----------------------------
    # D. Graphique principal (plotly)
    # -----------------------------
    backtest_df = backtest_price_and_strategy(df, strategy_df)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=backtest_df["timestamp"],
        y=backtest_df["close"],
        mode="lines",
        name="Close",
        line=dict(color="blue")
    ))
    fig.add_trace(go.Scatter(
        x=backtest_df["timestamp"],
        y=backtest_df["strategy_value"],
        mode="lines",
        name="Strategy Value",
        line=dict(color="green")
    ))
    fig.update_layout(title=f"{asset} Price vs Strategy Performance",
                      xaxis_title="Date", yaxis_title="Value", hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # E. Affichage des métriques
    # -----------------------------
    rets = backtest_df["strategy_returns"].dropna().values

    if len(rets) > 1:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sharpe Ratio", f"{sharpe_ratio(rets):.2f}")
        col2.metric("Max Drawdown", f"{max_drawdown(backtest_df['strategy_value'].values):.2%}")
        col3.metric("Volatility", f"{volatility(rets):.2%}")
        col4.metric("Cumulative Return", f"{cumulative_return(backtest_df['strategy_value'].values):.2%}")
    else:
        st.warning("Pas assez de données pour calculer les métriques")

    # -----------------------------
    # F. Prévisions (bonus)
    # -----------------------------
    st.markdown("---")  # Séparateur visuel
    st.subheader("📈 Forecast Future Prices")

    # 🔥 Les widgets AVANT le bouton
    forecast_horizon = st.number_input("Forecast Horizon (days):", min_value=1, max_value=60, value=10, key="forecast_horizon")
    forecast_method = st.selectbox("Forecast Method:", ["linear"], key="forecast_method")

    # Bouton pour lancer la prévision
    if st.button("Generate Forecast"):
        from single_asset.analytics.forecast import predict_next_days
        
        with st.spinner("Generating forecast..."):
            try:
                # Générer les prévisions
                forecast_series = predict_next_days(df, horizon=forecast_horizon, method=forecast_method)

                # Créer les dates futures
                last_date = pd.to_datetime(df['timestamp'].iloc[-1])
                future_dates = pd.date_range(
                    start=last_date + pd.Timedelta(days=1),
                    periods=forecast_horizon,
                    freq='D'
                )

                # Créer le graphique
                fig_forecast = go.Figure()
                
                # Historique
                fig_forecast.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['close'],
                    mode="lines",
                    name="Historical Close",
                    line=dict(color="blue", width=2)
                ))
                
                # Prévisions
                fig_forecast.add_trace(go.Scatter(
                    x=future_dates,
                    y=forecast_series,
                    mode="lines",
                    name="Forecast",
                    line=dict(color="red", dash="dash", width=2)
                ))
                
                # Mise en forme
                fig_forecast.update_layout(
                    title=f"{asset} - {forecast_method.capitalize()} Forecast ({forecast_horizon} days)",
                    xaxis_title="Date",
                    yaxis_title="Close Price ($)",
                    hovermode="x unified",
                    showlegend=True,
                    height=500
                )
                
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                # Afficher les valeurs prédites
                with st.expander("📊 View Forecast Values"):
                    forecast_df = pd.DataFrame({
                        'Date': future_dates,
                        'Predicted Price': forecast_series
                    })
                    st.dataframe(forecast_df)
                
            except Exception as e:
                st.error(f"❌ Error generating forecast: {str(e)}")
                st.exception(e)  # Pour le debug
