import pandas as pd
import numpy as np

def rebalancing_proportional_returns(data: pd.DataFrame, capital: float, freq: int, lookback: int = 30) -> pd.Series:
    selected_assets = data.columns
    n_assets = len(selected_assets)
    
    value = pd.Series(0.0, index=data.index)
    size = np.zeros(n_assets)  # nombre d'actions par actif
    current_value = capital
    
    for i in range(len(data)):
        if i % freq == 0:
            # Calculer les poids en fonction des rendements passés
            if i < lookback:
                # Pas assez de données historiques -> poids égaux
                weights = np.ones(n_assets) / n_assets
            else:
                # Calculer les rendements moyens sur la période lookback
                returns_window = data.iloc[i-lookback:i].pct_change().dropna()
                mean_returns = returns_window.mean()
                
                # Si tous les rendements sont négatifs ou nuls, utiliser poids égaux
                if (mean_returns <= 0).all():
                    weights = np.ones(n_assets) / n_assets
                else:
                    # Mettre à 0 les rendements négatifs (on n'investit pas dans actifs en baisse)
                    mean_returns = mean_returns.clip(lower=0)
                    
                    # Calculer poids proportionnels
                    sum_returns = mean_returns.sum()
                    if sum_returns > 0:
                        weights = (mean_returns / sum_returns).values
                    else:
                        weights = np.ones(n_assets) / n_assets
            
            # Réallouer le portefeuille avec les nouveaux poids
            for j in range(n_assets):
                size[j] = (current_value * weights[j]) / data.iloc[i, j]
        
        # Calculer la valeur totale du portefeuille
        current_value = np.sum(size * data.iloc[i, :])
        value.iloc[i] = current_value
    
    return value