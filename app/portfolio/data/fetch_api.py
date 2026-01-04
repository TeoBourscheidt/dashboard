import yfinance as yf
from typing import Annotated
import pandas as pd

def clean_data(data : pd.DataFrame)->pd.DataFrame:
    data = data.droplevel("Ticker", axis=1)
    return data["Close"]

def fetch_data_bis(list_ticket : list,start:Annotated[str, "YYYY-MM-DD"],end:Annotated[str, "YYYY-MM-DD"]) -> pd.DataFrame:
    save=pd.DataFrame()
    for ticket in list_ticket:
        data = yf.download(ticket, start, end)
        if data.empty:
            raise ValueError(f"Aucune donnée trouvée pour {ticket}.")
        save[ticket]=clean_data(data)
    return save

