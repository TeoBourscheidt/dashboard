import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_next_days(df: pd.DataFrame, horizon: int = 10, method: str = "linear") -> np.ndarray:
    """
    Prévoit les prix futurs en utilisant une régression linéaire simple.
    
    Args:
        df: DataFrame avec colonnes 'timestamp' et 'close'
        horizon: Nombre de jours à prévoir
        method: Méthode de prévision ('linear' pour l'instant)
    
    Returns:
        Array numpy avec les prévisions
    """
    # 🔥 Standardiser les colonnes en minuscules
    df_copy = df.copy()
    df_copy.columns = df_copy.columns.str.lower()
    
    # Vérifier que 'close' existe
    if 'close' not in df_copy.columns:
        raise ValueError(f"Le DataFrame doit contenir une colonne 'close'. Colonnes disponibles : {df_copy.columns.tolist()}")
    
    if method == "linear":
        # Préparer les données
        X = np.arange(len(df_copy)).reshape(-1, 1)  # Indices comme feature
        y = df_copy["close"].values  # 🔥 'close' en minuscule
        
        # Entraîner le modèle
        model = LinearRegression()
        model.fit(X, y)
        
        # Prédire les valeurs futures
        future_X = np.arange(len(df_copy), len(df_copy) + horizon).reshape(-1, 1)
        forecast = model.predict(future_X)
        
        return forecast
    
    else:
        raise NotImplementedError(f"Méthode '{method}' non implémentée. Utilisez 'linear'.")