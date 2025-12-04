import pandas as pd

def run_buy_and_hold(df: pd.DataFrame) -> pd.DataFrame:
    """
    Stratégie Buy & Hold : achète au début et garde jusqu'à la fin.
    
    Args:
        df: DataFrame avec colonnes 'timestamp' et 'close'
    
    Returns:
        DataFrame avec colonnes 'timestamp', 'position', 'strategy_value'
    """
    df_copy = df.copy()
    df_copy.columns = df_copy.columns.str.lower()
    
    # Vérifier que 'close' existe
    if 'close' not in df_copy.columns:
        raise ValueError(f"Le DataFrame doit contenir une colonne 'close'. Colonnes disponibles : {df_copy.columns.tolist()}")
    
    # 🔥 Vérifier que 'timestamp' existe
    if 'timestamp' not in df_copy.columns:
        raise ValueError(f"Le DataFrame doit contenir une colonne 'timestamp'. Colonnes disponibles : {df_copy.columns.tolist()}")
    
    # Créer le DataFrame de résultat
    result = pd.DataFrame()
    result['timestamp'] = df_copy['timestamp'].values  # 🔥 Inclure timestamp
    result['position'] = 1  # Toujours investi
    
    # Calculer la valeur de la stratégie normalisée à 100
    initial_price = df_copy['close'].iloc[0]
    result['strategy_value'] = (df_copy['close'].values / initial_price) * 100
    
    return result