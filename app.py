# TODO: Aquí debes escribir tu código

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análisis dataset bancario", page_icon=":bank:", layout="wide")

df = pd.read_csv("../data/processed/cleaned_data.csv", sep=",")

col_numericas = [""]
# Para ejecutar la app
# streamlit run app.py