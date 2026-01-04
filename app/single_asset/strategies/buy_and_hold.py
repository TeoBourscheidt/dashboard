import pandas as pd
from datetime import datetime, timedelta

def buy_and_hold(data : pd.DataFrame, start: str, capital : float=1000)  -> pd.DataFrame:
    evolve=pd.DataFrame()
    evolve.index=data.index
    while start not in data.index:
        start = start + timedelta(days=1)


    size_position=capital/data.loc[start]
    evolve["Portefeuille"]=data*size_position
    evolve.loc[:start,"Portefeuille"]=0
    return evolve
