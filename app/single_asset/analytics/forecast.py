import numpy as np
import pandas as pd
from pmdarima import auto_arima


def auto_arima_forecast(
    price_series: pd.Series,
    horizon: int,
    freq: str = "D",
):

    series = price_series.copy()
    # --- Fréquence ---
    if freq is not None:
        series = series.asfreq(freq)
        series = series.interpolate()

    # --- Rendements log ---
    log_returns = np.log(series/series.shift(1)).dropna()

    # --- Auto-ARIMA ---
    model = auto_arima(log_returns )

    # --- Prévision ---
    forecast_returns = model.predict(n_periods=horizon)

    # --- Retour aux prix ---
    last_price = series.iloc[-1]
    forecast_prices = last_price * np.exp(np.cumsum(forecast_returns))

    # --- Index futur ---
    future_index = pd.date_range(
        start=series.index[-1],
        periods=horizon + 1,
        freq=series.index.freq or freq
    )[1:]

    forecast_prices = pd.Series(
        forecast_prices,
        index=future_index,
        name="forecast_price"
    )
    return forecast_prices
