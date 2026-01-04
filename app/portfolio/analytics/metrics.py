import pandas as pd
import numpy as np


def return_portfolio(data : pd.DataFrame)->pd.DataFrame:
    return data.pct_change().dropna()


def vol_portfolio(returns: pd.DataFrame | pd.Series, weights: list = None) -> float:

    if isinstance(returns, pd.Series):
        # Cas 1: returns de portefeuille directement
        port_vol = returns.std() * np.sqrt(252)
    else:
        # Cas 2: returns par actif + weights
        if weights is None:
            raise ValueError("Weights must be provided when returns is a DataFrame")
        weights = np.array(weights)
        cov_matrix = returns.cov() * 252
        port_vol = np.sqrt(weights.T @ cov_matrix @ weights)
    
    return port_vol


def sharpe_ratio(returns: pd.DataFrame | pd.Series, weights: list = None, rf: float = 0.03, vol: float = None) -> float:
    """
    Calcule le ratio de Sharpe du portefeuille.
    
    Args:
        returns: DataFrame (returns par actif) ou Series (returns du portefeuille)
        weights: list des poids (requis si returns est un DataFrame)
        rf: float, taux sans risque annuel
        vol: float, volatilité pré-calculée (optionnelle)
    
    Returns:
        float: Ratio de Sharpe
    """
    if isinstance(returns, pd.Series):
        # Cas 1: returns de portefeuille directement
        ret_annual = returns.mean() * 252
        if vol is None:
            vol = vol_portfolio(returns)
    else:
        # Cas 2: returns par actif + weights
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
    """
    Calcule le drawdown maximum du portefeuille.
    
    Args:
        returns: DataFrame (returns par actif) ou Series (returns du portefeuille)
        weights: list des poids (requis si returns est un DataFrame)
    
    Returns:
        float: Maximum drawdown (valeur négative)
    """
    if isinstance(returns, pd.Series):
        # Cas 1: returns de portefeuille directement
        portfolio_cum = (1 + returns).cumprod()
    else:
        # Cas 2: returns par actif + weights
        if weights is None:
            raise ValueError("Weights must be provided when returns is a DataFrame")
        weights = np.array(weights)
        portfolio_cum = (1 + (returns @ weights)).cumprod()
    
    running_max = portfolio_cum.cummax()
    drawdown = (portfolio_cum - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return max_drawdown


def VaR(returns: pd.DataFrame | pd.Series, weights: list = None, confidence: float = 0.05) -> float:
    """
    Calcule la Value at Risk (VaR) du portefeuille.
    
    Args:
        returns: DataFrame (returns par actif) ou Series (returns du portefeuille)
        weights: list des poids (requis si returns est un DataFrame)
        confidence: float, niveau de confiance (0.05 = 95%)
    
    Returns:
        float: VaR au niveau de confiance spécifié
    """
    if isinstance(returns, pd.Series):
        # Cas 1: returns de portefeuille directement
        var = returns.quantile(confidence)
    else:
        # Cas 2: returns par actif + weights
        if weights is None:
            raise ValueError("Weights must be provided when returns is a DataFrame")
        weights = np.array(weights)
        var = (returns @ weights).quantile(confidence)
    
    return var

def total_return(portfolio: pd.Series) -> float:
    """
    Calcule le rendement total du portefeuille sur la période.
    
    Args:
        portfolio: Series représentant la valeur du portefeuille dans le temps
    
    Returns:
        float: Rendement total en pourcentage
    """
    initial_value = portfolio.iloc[0]
    final_value = portfolio.iloc[-1]
    total_ret = ((final_value - initial_value) / initial_value) * 100
    return total_ret


def annualized_return(portfolio: pd.Series) -> float:
    """
    Calcule le rendement annualisé du portefeuille.
    
    Args:
        portfolio: Series représentant la valeur du portefeuille dans le temps
    
    Returns:
        float: Rendement annualisé en pourcentage
    """
    initial_value = portfolio.iloc[0]
    final_value = portfolio.iloc[-1]
    
    # Nombre de jours dans la période
    n_days = (portfolio.index[-1] - portfolio.index[0]).days
    n_years = n_days / 365.25
    
    # Rendement annualisé
    if n_years > 0:
        annualized_ret = (((final_value / initial_value) ** (1 / n_years)) - 1) * 100
    else:
        annualized_ret = 0.0
    
    return annualized_ret


def cagr(portfolio: pd.Series) -> float:
    """
    Calcule le CAGR (Compound Annual Growth Rate) du portefeuille.
    Identique à annualized_return, mais nom plus explicite en finance.
    
    Args:
        portfolio: Series représentant la valeur du portefeuille dans le temps
    
    Returns:
        float: CAGR en pourcentage
    """
    return annualized_return(portfolio)