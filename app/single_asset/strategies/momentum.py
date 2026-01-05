import pandas as pd

def run_momentum(data: pd.DataFrame, start : str, capital :float = 1000, window: int = 20) -> pd.DataFrame:
    start = pd.Timestamp(start)
    evolve=pd.DataFrame()
    evolve.index=data.index

    buy=False
    start_buy=None
    size_position=0

    suivi_capital=[]
    cash=capital

    for i in range(len(data.index)):
        if data.index[i]>start and i>window:
            rendement=( data.loc[data.index[i]] - data.loc[data.index[i-window]] ) / data.loc[data.index[i-window]]
            if rendement>0:
                if not buy:
                    buy=True
                    start_buy=data.index[i]
                    size_position=cash/data.loc[start_buy]
                    print(size_position)
                    cash=0 
                suivi_capital.append(size_position*data.loc[data.index[i]])
                
                
            else :
                if buy:
                    buy=False
                    cash=size_position*data.loc[data.index[i]]
                    size_position=0
                suivi_capital.append(cash)
        else :
            suivi_capital.append(0)
    evolve["Portefeuille"]=suivi_capital
    return evolve