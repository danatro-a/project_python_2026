# TODO: Aquí debes escribir tu código

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análisis dataset bancario", page_icon="✨", layout="wide")

df = pd.read_csv("data/processed/transformed_and_clean_data.csv")

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

st.subheader("Datos filtrados")
st.write(f'Cantidad de registros después del filtrado: {len(df_filtrado)}')
st.dataframe(df_filtrado)

col_num_filtradas =  df_filtrado[col_numericas]
resumen = pd.DataFrame({
    "Columna": col_num_filtradas.columns,
    "Media": col_num_filtradas.mean(),
    "Mediana": col_num_filtradas.median(),
    "Desviación Estándar": col_num_filtradas.std(),
    "Minimo": col_num_filtradas.min(),
    "Maximo": col_num_filtradas.max(),
    "Rango": col_num_filtradas.max() - col_num_filtradas.min(),
    "Cuartil 25%": col_num_filtradas.quantile(0.25),
    "Cuartil 75%": col_num_filtradas.quantile(0.75)
}).reset_index(drop=True)

st.subheader("Resumen estadístico de las variables numéricas")
st.dataframe(resumen)

columnas_scatter_x = ["dias_hasta_registro", "Monto USD", "Sucursal", "Vendedor", "Mensual"]


st.subheader("Gráficos de distribución")
if df_filtrado.empty:
    st.warning("No hay datos para mostrar. Ajusta los filtros para ver los gráficos.")
else:
    for col in col_numericas:
        fig = px.histogram(df_filtrado, x=col, nbins=20, title=f"Distribución de {col}")
        st.plotly_chart(fig, use_container_width=True)

    columna_x = st.selectbox("Selecciona la variable para el eje X del scatter plot", options=columnas_scatter_x)
    columna_y = st.selectbox("Selecciona la variable para el eje Y del scatter plot", options=col_numericas)
    fig_scatter = px.scatter(df_filtrado, x=columna_x, y=columna_y, title=f"Scatter plot: {columna_x} vs {columna_y}")
    st.plotly_chart(fig_scatter, use_container_width=True)

# Para ejecutar la app
# streamlit run app.py