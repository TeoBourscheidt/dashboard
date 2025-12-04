import yfinance as yf
from typing import Annotated
import pandas as pd

def fetch_data(ticket : str,start:Annotated[str, "YYYY-MM-DD"],end:Annotated[str, "YYYY-MM-DD"]) -> pd.DataFrame:
    try:
        data = yf.download(ticket, start, end)
        if data.empty:
            raise ValueError(f"Aucune donnée trouvée pour {ticket}.")
        data = data.droplevel("Ticker", axis=1)
        return data

    except Exception as e:
        print(f"Erreur dans fetch_index_data : {e}")
        return pd.DataFrame()

def fetch_price(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Télécharge les données de prix d'un ticker via yfinance.
    """
    df = yf.download(ticker, period=period, progress=False)
    
    # Aplatir les colonnes si MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Réinitialiser l'index
    df = df.reset_index()
    
    # 🔥 NOUVEAU : Mettre toutes les colonnes en minuscules
    df.columns = df.columns.str.lower()
    
    # Renommer 'date' en 'timestamp' si nécessaire
    if 'date' in df.columns:
        df.rename(columns={'date': 'timestamp'}, inplace=True)
    
    return df