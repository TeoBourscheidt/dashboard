import pandas as pd
import numpy as np
from datetime import datetime
import os
import yfinance as yf

def enrgistrement_prices(tickers :list,start :str,end:str):
    data = yf.download(tickers, start, end)["Close"]
    data_file = r"C:\Users\bours\Documents\Esilv\A4\Python, Git and Linux\project_root\report\prices.csv"
    data.to_csv(data_file)

# Fichier des données (exemple)
data_file = r"C:\Users\bours\Documents\Esilv\A4\Python, Git and Linux\project_root\report\prices.csv"

# Lecture des données
df = pd.read_csv(data_file, parse_dates=['Date'], index_col='Date')

for asset in df.columns:
    # Calculs quotidiens
    volatility = df[asset].pct_change().std()  # volatilité
    close_price = df[asset].iloc[-1]
    max_drawdown = ((df[asset].cummax() - df[asset]) / df[asset].cummax()).max()

    # Créer dossier report si nécessaire
    report_dir = r"C:\Users\bours\Documents\Esilv\A4\Python, Git and Linux\project_root\reports"
    os.makedirs(report_dir, exist_ok=True)

    # Nom du fichier report
    now = datetime.now().strftime("%Y-%m-%d")
    report_file = os.path.join(report_dir, f"daily_report_{now}.txt")

    # Écriture du report
    with open(report_file, 'w') as f:
        f.write(f"Daily Report: {now}\n")
        f.write(f"Close Price: {close_price}\n")
        f.write(f"Volatility: {volatility:.4f}\n")
        f.write(f"Max Drawdown: {max_drawdown:.4f}\n")

    print(f"Report saved to {report_file}")
