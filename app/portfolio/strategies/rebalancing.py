import pandas as pd
import numpy as np

def rebalancing(data: pd.DataFrame, capital: float, freq: int, weights: list):
    selected_assets = data.columns
    n_assets = len(selected_assets)
    
    value = pd.Series(0.0, index=data.index)
    size = np.zeros(n_assets) 
    cash = capital
    
    for i in range(len(data)):
        if i % freq == 0 or i == 0:
            for j in range(n_assets):
                size[j] = (cash * weights[j]) / data.iloc[i, j]
        portfolio_value = np.sum(size * data.iloc[i, :])
        value.iloc[i] = portfolio_value
        cash = portfolio_value 
        
    return value