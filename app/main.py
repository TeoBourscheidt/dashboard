import streamlit as st

st.set_page_config(page_title="Finance Dashboard", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a module :", ["Single Asset", "Portfolio"])

if page == "Single Asset":
    st.title("Single Asset Analysis")
    st.write("Module Single Asset - En développement")
else:
    st.title("Portfolio Analysis")
    st.write("Module Portfolio - En développement")
