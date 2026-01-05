import pandas as pd
import numpy as np


def return_portfolio(data : pd.DataFrame)->pd.DataFrame:
    return data.pct_change().dropna()


def vol_portfolio(returns: pd.DataFrame | pd.Series, weights: list = None) -> float:
# Calcule la volatilité annuelle du portefeuille (écart-type annualisé).
    if isinstance(returns, pd.Series):
        port_vol = returns.std() * np.sqrt(252)
    else:
        if weights is None:
            raise ValueError("Weights must be provided when returns is a DataFrame")
        weights = np.array(weights)
        cov_matrix = returns.cov() * 252
        port_vol = np.sqrt(weights.T @ cov_matrix @ weights)
    
    return port_vol


def sharpe_ratio(returns: pd.DataFrame | pd.Series, weights: list = None, rf: float = 0.03, vol: float = None) -> float:
    #Mesure le rendement ajusté du risque. Plus le Sharpe est élevé, mieux le portefeuille compense le risque pris.
    if isinstance(returns, pd.Series):
        ret_annual = returns.mean() * 252
        if vol is None:
            vol = vol_portfolio(returns)
    else:
        if weights is None:
            raise ValueError("Weights must be provided when returns is a DataFrame")
        weights = np.array(weights)
        ret_mean_daily = returns.mean()
        ret_annual = (ret_mean_daily @ weights) * 252
        if vol is None:
            vol = vol_portfolio(returns, weights)
    
    sharpe = (ret_annual - rf) / vol
    return sharpe


def max_draw(returns: pd.DataFrame | pd.Series, weights: list = None) -> float:
    #Calcule la perte maximale depuis un sommet historique : Indique la plus grande baisse subie par le portefeuille.
    if isinstance(returns, pd.Series):
        portfolio_cum = (1 + returns).cumprod()
    else:
        if weights is None:
            raise ValueError("Weights must be provided when returns is a DataFrame")
        weights = np.array(weights)
        portfolio_cum = (1 + (returns @ weights)).cumprod()
    
    running_max = portfolio_cum.cummax()
    drawdown = (portfolio_cum - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return max_drawdown


def VaR(returns: pd.DataFrame | pd.Series, weights: list = None, confidence: float = 0.05) -> float:
    #Estime la perte potentielle maximale avec un certain niveau de confiance (par défaut 5% → 95% confidence).
    if isinstance(returns, pd.Series):
        var = returns.quantile(confidence)
    else:
        if weights is None:
            raise ValueError("Weights must be provided when returns is a DataFrame")
        weights = np.array(weights)
        var = (returns @ weights).quantile(confidence)
    
    return var

def total_return(portfolio: pd.Series) -> float:
    #Rendement total sur la période (en %)
    initial_value = portfolio.iloc[0]
    final_value = portfolio.iloc[-1]
    total_ret = ((final_value - initial_value) / initial_value) * 100
    return total_ret


def annualized_return(portfolio: pd.Series) -> float:
    #Rendement annualisé (%), tenant compte de la durée exacte de l’investissement.
    initial_value = portfolio.iloc[0]
    final_value = portfolio.iloc[-1]
    n_days = (portfolio.index[-1] - portfolio.index[0]).days
    n_years = n_days / 365.25
    if n_years > 0:
        annualized_ret = (((final_value / initial_value) ** (1 / n_years)) - 1) * 100
    else:
        annualized_ret = 0.0
    
    return annualized_ret


def cagr(portfolio: pd.Series) -> float:
   return annualized_return(portfolio)