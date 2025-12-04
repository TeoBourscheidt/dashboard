import pandas as pd

def run_momentum(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Stratégie Momentum : achète si prix > moyenne mobile, vend sinon.
    
    Args:
        df: DataFrame avec colonnes 'timestamp' et 'close'
        window: Fenêtre pour la moyenne mobile (défaut: 20 jours)
    
    Returns:
        DataFrame avec colonnes 'timestamp', 'position', 'strategy_value'
    """
    df_copy = df.copy()
    df_copy.columns = df_copy.columns.str.lower()
    
    # Vérifications
    if 'close' not in df_copy.columns:
        raise ValueError(f"Le DataFrame doit contenir une colonne 'close'. Colonnes : {df_copy.columns.tolist()}")
    
    if 'timestamp' not in df_copy.columns:
        raise ValueError(f"Le DataFrame doit contenir une colonne 'timestamp'. Colonnes : {df_copy.columns.tolist()}")
    
    # Calcul de la moyenne mobile
    df_copy['ma'] = df_copy['close'].rolling(window=window).mean()
    
    # Signal : 1 si prix > MA, 0 sinon
    df_copy['position'] = (df_copy['close'] > df_copy['ma']).astype(int)
    
    # Calculer les rendements quotidiens
    df_copy['returns'] = df_copy['close'].pct_change()
    
    # Rendements de la stratégie (position décalée d'un jour)
    df_copy['strategy_returns'] = df_copy['position'].shift(1) * df_copy['returns']
    
    # Valeur cumulée de la stratégie (commence à 100)
    df_copy['strategy_value'] = (1 + df_copy['strategy_returns'].fillna(0)).cumprod() * 100
    
    # Résultat final
    result = pd.DataFrame()
    result['timestamp'] = df_copy['timestamp'].values  # 🔥 Inclure timestamp
    result['position'] = df_copy['position'].values
    result['strategy_value'] = df_copy['strategy_value'].values
    
    return result