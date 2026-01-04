import numpy as np
import pandas as pd

def portfolio_return(data : pd.DataFrame) -> pd.DataFrame:
    #data["Return"]=( data["Portefeuille"]-data["Portefeuille"].shift(1) ) / data["Portefeuille"].shift(1)
    data["Return"]=data["Portefeuille"].pct_change()
    return data

def max_drawdown(data: pd.DataFrame) -> float:
    portfolio = data["Portefeuille"]

    # Supprimer les valeurs nulles initiales
    portfolio = portfolio[portfolio > 0]

    if portfolio.empty:
        return np.nan

    cum_max = portfolio.cummax()
    drawdown = (portfolio / cum_max) - 1

    return drawdown.min() * 100  # en % 

def CAGR(data: pd.DataFrame) -> float:
    portfolio = data["Portefeuille"].dropna()
    portfolio = portfolio[portfolio > 0]
    if portfolio.empty:
        return np.nan
    start_date = portfolio.index[0]
    end_date = portfolio.index[-1]

    T = (end_date - start_date).days / 365.25

    if T <= 0:
        return np.nan

    V_i = portfolio.iloc[0]
    V_f = portfolio.iloc[-1]

    if V_i <= 0:
        return np.nan

    return (V_f / V_i) ** (1 / T) - 1

def sharpe(data: pd.DataFrame, rf: float, periods: int = 252) -> float:
    returns=data["Return"]
    rf_period = rf / periods

    mean = returns.mean()-rf_period
    vol = returns.std()

    if vol == 0:
        return np.nan

    return (mean / vol) * np.sqrt(periods)


def vol_annual(data: pd.DataFrame, periods: int = 252) -> float:
    returns = data["Return"]
    return returns.std() * np.sqrt(periods)

# ✅ NOUVELLE MÉTRIQUE 1: Sortino Ratio
def sortino_ratio(data: pd.DataFrame, rf: float, periods: int = 252) -> float:
    """
    Calcule le ratio de Sortino (similaire au Sharpe mais pénalise uniquement la volatilité à la baisse).
    
    Args:
        data: DataFrame contenant la colonne "Return"
        rf: Taux sans risque annuel (ex: 0.03 pour 3%)
        periods: Nombre de périodes par an (252 pour jours de trading)
    
    Returns:
        float: Sortino ratio (plus élevé = meilleur)
    """
    returns = data["Return"].dropna()
    
    if returns.empty:
        return np.nan
    
    rf_period = rf / periods
    mean_return = returns.mean() - rf_period
    
    # Volatilité à la baisse (downside deviation)
    # On ne prend que les rendements négatifs
    downside_returns = returns[returns < 0]
    
    if len(downside_returns) == 0:
        # Pas de rendements négatifs = risque de baisse nul
        return np.inf if mean_return > 0 else np.nan
    
    downside_std = downside_returns.std()
    
    if downside_std == 0:
        return np.nan
    
    return (mean_return / downside_std) * np.sqrt(periods)




# ✅ BONUS: Value at Risk (VaR)
def value_at_risk(data: pd.DataFrame, confidence: float = 0.95) -> float:
    """
    Calcule la Value at Risk (VaR) - perte maximale attendue avec un certain niveau de confiance.
    
    Args:
        data: DataFrame contenant la colonne "Return"
        confidence: Niveau de confiance (0.95 = 95%)
    
    Returns:
        float: VaR en % (valeur positive représentant la perte potentielle)
    """
    returns = data["Return"].dropna()
    
    if returns.empty:
        return np.nan
    
    var = returns.quantile(1 - confidence)
    
    return abs(var) * 100  # En %