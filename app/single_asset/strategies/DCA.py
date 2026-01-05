import pandas as pd
from datetime import datetime, timedelta


def DCA(data : pd.Series,start:str,capital:float, freq: float,amount:float)->tuple:
    start = pd.Timestamp(start)
    while start not in data.index:
        start = start + timedelta(days=1)

    evolve=pd.Series(0,index=data.index)

    total_invest=capital
    size=capital/data.loc[start]
    moyenne_achat=size*data.iloc[0]
    for i in range(len(data)):
        if data.index[i]>start:
            if (data.index[i] - start).days % freq == 0:
                new_buy_size=amount/data.iloc[i]
                size+= new_buy_size
                moyenne_achat+=new_buy_size*data.iloc[i]
                total_invest+=amount
            evolve.iloc[i]=size*data.iloc[i]
    rendue=pd.DataFrame()
    rendue["Portefeuille"]=evolve
    return rendue,moyenne_achat/size,total_invest

    