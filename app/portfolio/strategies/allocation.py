import pandas as pd 


def allocation_hold(data : pd.DataFrame, selected_assets : list,weights:list,capital:float)->pd.DataFrame:
    portfolio = pd.Series(0, index=data.index)
    for i in range(len(selected_assets)):
        size_pos=capital*weights[i]/data[selected_assets[i]].iloc[0]
        portfolio+=size_pos*data[selected_assets[i]]
    return portfolio