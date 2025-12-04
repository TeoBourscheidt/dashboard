import pandas as pd

def simulate_portfolio(df, weights):
    weighted = pd.DataFrame()

    for asset, w in weights.items():
        weighted[asset] = w * (df[asset] / df[asset].iloc[0])

    return weighted.sum(axis=1)
