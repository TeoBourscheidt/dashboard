import pandas as pd

def clean_data(df : pd.DataFrame)->pd.DataFrame: 
    data=df.copy()
    if isinstance(data.index, pd.DatetimeIndex):
        data.index=pd.to_datetime(data.index) 
    data = data.dropna(how="any")
    data = data[~data.index.duplicated(keep="first")]
    return data

def resample_data(df: pd.DataFrame, freq: str) -> pd.DataFrame:
    # Normalisation des noms de colonnes
    cols = {c.lower(): c for c in df.columns}
    
    # Détection OHLC
    required = ["open", "high", "low", "close"]
    has_ohlc = all(col in cols for col in required)
    
    if has_ohlc:
        # Construction dynamique du dictionnaire OHLC
        ohlc_dict = {
            cols["open"]: "first",
            cols["high"]: "max",
            cols["low"]: "min",
            cols["close"]: "last"
        }
        return df.resample(freq).agg(ohlc_dict).dropna()
    
    # Si pas OHLC → fallback : moyenne
    return df.resample(freq).mean().dropna()
