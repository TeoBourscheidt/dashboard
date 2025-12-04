import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Finance Dashboard", layout="wide")

# Sidebar pour navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a module:", ["Single Asset", "Portfolio"])

# -----------------------------
# Single Asset
# -----------------------------
if page == "Single Asset":
    st.title("Single Asset Analysis")

    # Import et affichage du front-end Single Asset
    from single_asset.ui_single_asset import run_ui_single_asset
    run_ui_single_asset()

# -----------------------------
# Portfolio
# -----------------------------
else:
    st.title("Portfolio Analysis")
    st.write("Module Portfolio - En développement")
