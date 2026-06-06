# TODO: Aquí debes escribir tu código

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análisis dataset bancario", page_icon=":bank:", layout="wide")

df = pd.read_csv("/data/processed/transformed_and_clean_data.csv", sep=",")

# Variables numéricas
col_numericas = ["dias_hasta_registro", "Monto USD"]
for columna in col_numericas:
    if columna in df.columns:
        df[columna] = pd.to_numeric(df[columna], errors='coerce')

# Variables categóricas
col_categoricas = ["Sucursal", "Producto", "Vendedor", "Estado App", "estado_mora", "Mensual"]
for col in col_categoricas:
    df[col] = df[col].astype(str)

# Tituloo de la app
st.title("Análisis del dataset bancario")
st.markdown("Este dashboard presenta un análisis del dataset bancario, " \
"mostrando la distribución de los datos a través de varias sucursales de Uruguay.")

# Sidebar markdown y comentario de los filtros
st.sidebar.markdown("""
## Filtros
Puedes utilizar los siguientes filtros para analizar el dataset.
Los gráficos se actualizarán automáticamente según los filtros seleccionados.
                    """)

columna_filtro = st.sidebar.selectbox("Selecciona una columna para filtrar", options=df.columns)


df_filtrado = df.copy()
# Filtrado categórico
for col in col_numericas:
    min_val = float(df[col].min())
    max_val = float(df[col].max())

    rango = st.sidebar.slider(
        f"{col}",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val)
    )

    df_filtrado = df_filtrado[
        (df_filtrado[col] >= rango[0]) & 
        (df_filtrado[col] <= rango[1])
    ]

# Fitlrado numérico
for col in col_categoricas:
    opciones = df[col].unique()

    seleccion = st.sidebar.multiselect(
        f"{col}",
        opciones,
        default=opciones
    )

    df_filtrado = df_filtrado[df_filtrado[col].isin(seleccion)]
# Para ejecutar la app
# streamlit run app.py