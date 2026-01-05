import streamlit as st
import time
import datetime as dt
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Finance Dashboard", layout="wide")
# Auto-refresh toutes les 5 minutes (300 secondes)
st_autorefresh = st.empty()
with st_autorefresh:
    st.markdown(
        """
        <script>
        setTimeout(function(){
            window.location.reload();
        }, 300000);
        </script>
        """,
        unsafe_allow_html=True
    )

from single_asset.ui_single_asset import run_ui_single_asset
from portfolio.ui_portfolio import portfolio_page
from portfolio.data.fetch_api import fetch_data_bis

# Sidebar pour navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Home", "Strategy"])

# Afficher l'heure de dernière mise à jour
st.sidebar.info(f"Last update: {time.strftime('%Y-%m-%d %H:%M:%S')}")

####################"
#Home page
if page == "Home":
    st.markdown("<h1 style='text-align: center;'>Home</h1>", unsafe_allow_html=True)
    st.text("As part of our academic program, we have developed a platform designed to support portfolio managers by providing " \
    "them with quantitative management tools. Our goal is to create a dashboard capable of retrieving, analyzing, and visualizing " \
    "financial and economic data in real time, while simulating investment strategies and providing key metrics for decision-making"
    ". Our project consists of two pages: a Home page for presentation and a Strategy page presenting different types of investment" \
    " strategies for a single asset or an investment portfolio.")

    ##############
    # Acceuil affiache d'un actif ou plusieurs actifs :
    ###################"################"
    # Parameters

    today = dt.date.today()
    default_start = today - dt.timedelta(days=365)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start date",
            value=default_start,
            max_value=today
        )
    with col2:
        end_date = st.date_input(
            "End date",
            value=today,
            min_value=start_date,
            max_value=today
        )

    user_input = st.text_input(
        "Enter asset tickers (comma separated)",
        value="AAPL, MSFT, GOOGL"
    )
    st.text("Example of tickets : Bitcoin : BTC-USD , Apple : AAPL , S&P 500 : ^GSPC , OR : GC=F.")
    selected_assets = [
    t.strip().upper()
    for t in user_input.split(",")
    if t.strip() != ""
    ]

    #On charge les data 
    data = fetch_data_bis(selected_assets,start_date, end_date)

    #Affichage du prix actuel:
    cols = st.columns(len(selected_assets))  
    for i, ticket in enumerate(selected_assets):
        last_price = data[ticket].iloc[-1]  # dernier prix
        prev_price = data[ticket].iloc[-2] if len(data[ticket]) > 1 else last_price
        delta = last_price - prev_price  # variation
        delta_pct = (delta / prev_price) * 100 if prev_price != 0 else 0

        # couleur verte si hausse, rouge si baisse
        color = "normal"  # st.metric gère automatiquement vert/rouge pour delta
        cols[i].metric(label=ticket, value=f"${last_price:.2f}", delta=f"{delta_pct:.2f}%")

    #On affiche les asset
    fig = go.Figure()
    for ticket in selected_assets:
        fig.add_trace(go.Scatter(
        x=data.index,
        y=data[ticket],
        mode="lines",
        name=ticket
    ))
    fig.update_layout(
        title="Asset price evolution",
        xaxis_title="Date",
        yaxis_title="Price",
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
   

##############"
# Strategy page
else:
    st.markdown("<h1 style='text-align: center;'>Strategy</h1>", unsafe_allow_html=True)
    st.text("The project is based on a modular architecture, developed in pairs:\n Module Quant A (Single asset): analysis of a single asset," \
    " with backtesting of strategies such as buy-and-hold or momentum, performance display (Sharpe ratio, max drawdown) and " \
    "interactive visualization of the cumulative value of the strategy.\nQuant Module B (Portfolio): multivariate analysis and portfolio " \
    "simulation with multiple assets, weight management and rebalancing, display of portfolio metrics (correlation, volatility," \
    " return) and comparison with individual assets")

    strategy = st.selectbox(
        "Select module",
        ["Quant A (Single asset)", "Quant B (Portfolio)"],
        index=0 
    )
    if strategy=="Quant A (Single asset)":
        run_ui_single_asset()
    else:
        portfolio_page()

####################
# Pour faire les rapports mais ca ne marche pas 
#from ..reports.report_code import enrgistrement_prices
#enrgistrement_prices(selected_assets,start_date,end_date)

    
    