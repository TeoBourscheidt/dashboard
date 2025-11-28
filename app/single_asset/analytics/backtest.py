import pandas as pd

def run_backtest(price_series, strat_series):
    df = pd.DataFrame({
        "price": price_series,
        "strategy": strat_series
    })
    df["strategy_value"] = df["strategy"].cumprod()
    return df
