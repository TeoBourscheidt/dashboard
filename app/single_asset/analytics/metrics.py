import numpy as np

def compute_metrics(strategy_series):
    returns = strategy_series.pct_change().dropna()

    sharpe = np.sqrt(252) * returns.mean() / returns.std()
    max_drawdown = ((strategy_series / strategy_series.cummax()) - 1).min()

    return {
        "Sharpe Ratio": float(sharpe),
        "Max Drawdown": float(max_drawdown)
    }
