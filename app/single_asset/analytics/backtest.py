import pandas as pd

def backtest_price_and_strategy(price_df: pd.DataFrame, strategy_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fusionne les données de prix et de stratégie pour le backtesting.
    
    Args:
        price_df: DataFrame avec colonnes 'timestamp', 'close', etc.
        strategy_df: DataFrame avec colonnes 'timestamp', 'position', 'strategy_value'
    
    Returns:
        DataFrame fusionné avec 'timestamp', 'close', 'strategy_value', 'strategy_returns'
    """
    # 🔥 Merge sur 'timestamp' en évitant les doublons
    backtest_df = pd.merge(
        price_df[['timestamp', 'close']],  # Sélectionner uniquement les colonnes nécessaires
        strategy_df[['timestamp', 'strategy_value']],  # Éviter de dupliquer 'timestamp'
        on='timestamp',
        how='inner'
    )
    
    # Calculer les rendements de la stratégie
    backtest_df['strategy_returns'] = backtest_df['strategy_value'].pct_change()
    
    return backtest_df