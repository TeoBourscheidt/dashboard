import numpy as np
import pandas as pd
from pmdarima import auto_arima

def auto_arima_forecast(price_series: pd.Series,horizon: int,freq: str = "D",alpha: float = 0.05)->pd.DataFrame:

    series = price_series.copy()

    if freq is not None:
        series = series.asfreq(freq)
        series = series.interpolate()

    # ARIMA sur les prix avec auto-différenciation
    model = auto_arima(
        series,
        start_p=1, start_q=1,
        max_p=3, max_q=3,
        d=None,  # Trouve auto l'ordre de différenciation
        seasonal=False,
        suppress_warnings=True,
        stepwise=True
    )

    # Prévision
    forecast_price, conf_int = model.predict(
        n_periods=horizon,
        return_conf_int=True,
        alpha=alpha
    )

    #Ajout d'une tendance simple pour éviter les prédictions plates
    recent_trend = (series.iloc[-1] - series.iloc[-min(20, len(series))]) / min(20, len(series))
    trend_adjustment = np.array([recent_trend * (i + 1) * 0.3 for i in range(horizon)])
    forecast_price = forecast_price + trend_adjustment

    future_index = pd.date_range(
        start=series.index[-1],
        periods=horizon + 1,
        freq=series.index.freq or freq
    )[1:]

    return pd.DataFrame(
        {
            "forecast": forecast_price,
            "lower": conf_int[:, 0] + trend_adjustment,
            "upper": conf_int[:, 1] + trend_adjustment,
        },
        index=future_index
    )