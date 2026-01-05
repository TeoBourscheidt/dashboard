import streamlit as st
def check_weights(weights):
    total = sum(weights)
    if total > 1:
        st.warning("Weights normalized because sum > 1")
        return [w / total for w in weights]
    return weights