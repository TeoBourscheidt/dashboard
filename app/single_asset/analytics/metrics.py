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

