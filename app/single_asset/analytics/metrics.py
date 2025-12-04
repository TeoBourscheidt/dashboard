import numpy as np

def max_drawdown(series: np.ndarray) -> float:
    """
    Maximum drawdown d'une série de valeur cumulée.
    """
    cum_max = np.maximum.accumulate(series)
    drawdown = (series - cum_max) / cum_max
    return drawdown.min()

def cumulative_return(series: np.ndarray) -> float:
    """
    Rendement cumulatif total.
    """
    return series[-1] / series[0] - 1

def volatility(returns: np.ndarray, freq: int = 252) -> float:
    """
    Volatilité annualisée des rendements.
    
    freq : nombre de périodes par an (252 pour daily, 12 pour monthly)
    """
    return np.std(returns) * np.sqrt(freq)

def sharpe_ratio(returns: np.ndarray, freq: int = 252, risk_free_rate: float = 0.0) -> float:
    """
    Sharpe ratio annualisé.
    
    risk_free_rate : taux sans risque annualisé (0 par défaut)
    """
    excess_returns = returns - risk_free_rate / freq
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(freq)
