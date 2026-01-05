import numpy as np
import pandas as pd

def portfolio_return(data : pd.DataFrame) -> pd.DataFrame:
    #data["Return"]=( data["Portefeuille"]-data["Portefeuille"].shift(1) ) / data["Portefeuille"].shift(1)
    data["Return"]=data["Portefeuille"].pct_change()
    return data

def max_drawdown(data: pd.DataFrame) -> float:
    #Le Max Drawdown mesure la perte maximale subie par ton portefeuille depuis un sommet historique jusqu’à un creux.
    portfolio = data["Portefeuille"]
    portfolio = portfolio[portfolio > 0]

    if portfolio.empty:
        return np.nan

    cum_max = portfolio.cummax()
    drawdown = (portfolio / cum_max) - 1
    return drawdown.min() * 100  # en % 

def CAGR(data: pd.DataFrame) -> float:
    #Le CAGR indique le taux de croissance annuel moyen d’un investissement sur toute la période.
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
    #Le Sharpe Ratio mesure le rendement excédentaire du portefeuille par rapport au risque total (volatilité).
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


def sortino_ratio(data: pd.DataFrame, rf: float, periods: int = 252) -> float:
    #Le Sortino Ratio est un indicateur de performance ajustée au risque, qui pénalise uniquement les rendements négatifs.
    returns = data["Return"].dropna() 

    if returns.empty:
        return np.nan
    rf_period = rf / periods
    mean_return = returns.mean() - rf_period
    downside_returns = returns[returns < 0]

    if len(downside_returns) == 0:
        return np.inf if mean_return > 0 else np.nan
    downside_std = downside_returns.std()

    if downside_std == 0:
        return np.nan
    return (mean_return / downside_std) * np.sqrt(periods)


def value_at_risk(data: pd.DataFrame, confidence: float = 0.95) -> float:
    #La Value at Risk (VaR) mesure la perte maximale attendue sur un portefeuille avec un certain niveau de confiance.
    returns = data["Return"].dropna()
    
    if returns.empty:
        return np.nan
    
    var = returns.quantile(1 - confidence)
    
    return abs(var) * 100  