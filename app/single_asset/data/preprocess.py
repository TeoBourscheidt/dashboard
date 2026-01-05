import pandas as pd

def clean_data(data : pd.DataFrame)->pd.DataFrame:
    data = data.droplevel("Ticker", axis=1)
    return data["Close"]
