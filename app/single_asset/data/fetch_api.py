import yfinance as yf
from typing import Annotated
import pandas as pd

def fetch_data(ticket : str,start:Annotated[str, "YYYY-MM-DD"],end:Annotated[str, "YYYY-MM-DD"]) -> pd.DataFrame:
    try:
        data = yf.download(ticket, start, end)
        if data.empty:
            raise ValueError(f"Aucune donnée trouvée pour {ticket}.")
        return data

    except Exception as e:
        print(f"Erreur dans fetch_index_data : {e}")
        return pd.DataFrame()

def fetch_price(ticker: str, period: str = "1y") -> pd.DataFrame:
    try:
        data = yf.download(ticker, period=period, progress=False)
        if data.empty:
            raise ValueError(f"Aucune donnée trouvée pour {ticker}.")
        return data

    except Exception as e:
        print(f"Erreur dans fetch_index_data : {e}")
        return pd.DataFrame()