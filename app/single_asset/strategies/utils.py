import pandas as pd
import numpy as np

def moving_average(series: pd.Series, window: int) -> pd.Series:
    """
    Moyenne mobile simple.
    """
    return series.rolling(window).mean()


def position_sizing(capital: float, price: float, risk_pct: float = 0.01) -> int:
    """
    Détermine le nombre de positions que l'on peut acheter.
    risk_pct = 1% du capital par défaut
    """
    risk_amount = capital * risk_pct
    return int(risk_amount / price)


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise chaque colonne entre 0 et 1.
    """
    return (df - df.min()) / (df.max() - df.min())
