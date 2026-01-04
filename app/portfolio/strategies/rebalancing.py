import pandas as pd
import numpy as np

def rebalancing(data: pd.DataFrame, capital: float, freq: int, weights: list):
    """
    data : DataFrame des prix (index = dates, colonnes = actifs)
    capital : capital initial
    freq : fréquence de rebalancing (en nombre de jours)
    weights : liste des poids des actifs, somme = 1
    """
    
    selected_assets = data.columns
    n_assets = len(selected_assets)
    
    value = pd.Series(0.0, index=data.index)
    size = np.zeros(n_assets)  # nombre d’actions par actif
    cash = capital
    
    for i in range(len(data)):
        # Rebalancing si fréquence atteinte ou première date
        if i % freq == 0 or i == 0:
            for j in range(n_assets):
                # nombre d’actions = poids * capital / prix actuel
                size[j] = (cash * weights[j]) / data.iloc[i, j]
        
        # valeur totale du portefeuille
        portfolio_value = np.sum(size * data.iloc[i, :])
        value.iloc[i] = portfolio_value
        cash = portfolio_value  # mise à jour du capital pour le prochain rebalancing
        
    return value