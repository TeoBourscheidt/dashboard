import yfinance as yf

def fetch_prices(assets):
    df = yf.download(assets, period="6mo", interval="1h")["Close"]
    df = df.rename_axis("timestamp").reset_index()
    return df.set_index("timestamp")
