import yfinance as yf
import pandas as pd

def fetch_price(asset):
    try:
        df = yf.download(asset, period="6mo", interval="1h")
        df = df.rename(columns={"Close": "close"})
        return df
    except Exception as e:
        print("API Error:", e)
        return None
