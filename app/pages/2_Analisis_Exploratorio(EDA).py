import numpy as np
import plotly.express as px
import streamlit as st

ETIQUETAS = {
    "cantidad_toneladas": "Toneladas (t)", "tipo_fuente": "Tipo de fuente", "region": "Región",
    "comuna": "Comuna", "año": "Año",
}

if "datos" not in st.session_state:
    st.warning("Vaya a la página 'Contexto' para cargar los datos.")
    st.stop()

df = st.session_state["datos"]

st.title("2. Análisis Exploratorio de Datos (EDA)")
st.caption("¿Cómo se comportan nuestros datos?")

# Filtros de Exploración
st.sidebar.header("Filtros")

contaminantes = sorted(df["contaminantes"].dropna().unique())
contaminante_sel = st.sidebar.selectbox(
    "Contaminante", contaminantes,
    index=contaminantes.index("MP2,5") if "MP2,5" in contaminantes else 0
    )

regiones = sorted(df["region"].dropna().unique())
region_sel = st.sidebar.multiselect("Regiones", regiones, default=regiones)

# Filtrar el dataframe
df_filtrado = df[(df["region"].isin(region_sel)) & (df["contaminantes"] == contaminante_sel)]

if df_filtrado.empty:
    st.warning("No hay datos para esta combinación de filtros.")
    st.stop()

st.markdown(f"Contaminante: **{contaminante_sel}** · {len(region_sel)} región(es) · "
            f"{len(df_filtrado):,} registros (cada registro = comuna x fuente x año).")

# Estadísticas Descriptivas
st.header("1. Estadísticas Descriptivas")
y = df_filtrado["cantidad_toneladas"]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Media", f"{y.mean():,.1f} t")
col2.metric("Mediana", f"{y.median():,.1f} t")
col3.metric("Desviación Est.", f"{y.std():,.1f} t")
col4.metric("Asimetría", f"{y.skew():,.1f}")
col5.metric("Máximo", f"{y.max():,.0f} t")

tabla = (df_filtrado.groupby("tipo_fuente")["cantidad_toneladas"]
         .agg(registros="count", mediana="median", media="mean", maximo="max", total="sum")
         .sort_values("total", ascending=False).round(2))
st.dataframe(tabla, use_container_width=True)

razon = y.mean() / y.median() if y.median() > 0 else float("nan")
top10 = y[y >= y.quantile(0.9)].sum() / y.sum() * 100 if y.sum() > 0 else float("nan")
st.info(f"💡 **Interpretación:** la media ({y.mean():,.1f} t) es {razon:,.1f} veces la mediana ({y.median():,.1f} t) "
        f"y la asimetría es {y.skew():,.1f}: hay sesgo positivo. El 10% de registros más altos concentra el "
        f"{top10:.1f}% de las toneladas, es decir, pocos registros extremos elevan el promedio.")

#  Distribución (Histograma)
st.header("2. Distribución de las Toneladas")
df_grafico = df_filtrado[df_filtrado["cantidad_toneladas"] > 0].copy()   
excluidos = len(df_filtrado) - len(df_grafico)

# Calculamos el logaritmo matemáticamente para que las barras se distribuyan bien
df_grafico["log10_t"] = np.log10(df_grafico["cantidad_toneladas"])

fig_hist = px.histogram(
    df_grafico,
    x="log10_t",
    nbins=40,
    labels={"log10_t": "Toneladas de emisión"},
    title=f"Distribución de las toneladas de {contaminante_sel} por registro"
)

# Reemplazamos los números por las toneladas reales en el eje X
fig_hist.update_xaxes(
    tickvals=[-1, 0, 1, 2, 3, 4],
    ticktext=["0.1 t", "1 t", "10 t", "100 t", "1.000 t", "10.000 t"]
)

fig_hist.update_layout(yaxis_title="Número de registros", bargap=0.05)
st.plotly_chart(fig_hist, use_container_width=True)

p_bajo = (df_grafico["cantidad_toneladas"] < 10).mean() * 100
p_alto = (df_grafico["cantidad_toneladas"] >= 1000).mean() * 100

st.info(f"💡 **Interpretación:** el {p_bajo:.1f}% de los registros emite menos de 10 t y solo el {p_alto:.1f}% "
        f"supera las 1.000 t. Usamos una escala logarítmica en el eje X porque de lo contrario, "
        f"los registros extremos aplastarían la visualización de los datos normales."
        + (f" Se excluyeron {excluidos:,} re    gistros con 0 t o menos." if excluidos else ""))
# Carga Contaminante por Tipo de Fuente
st.header("3. Total acumulado por Fuente")

# Agrupacion
df_fuentes = df_filtrado.groupby("tipo_fuente", as_index=False)["cantidad_toneladas"].sum()
df_fuentes = df_fuentes.sort_values("cantidad_toneladas", ascending=True)
df_fuentes["pct"] = df_fuentes["cantidad_toneladas"] / df_fuentes["cantidad_toneladas"].sum() * 100

fig_bar = px.bar(
    df_fuentes,
    x="cantidad_toneladas",
    y="tipo_fuente",
    orientation="h",
    text=df_fuentes["pct"].map(lambda v: f"{v:.1f}%"),
    labels=ETIQUETAS,
    title=f"Toneladas totales de {contaminante_sel} por fuente, 2019–2024"
)
st.plotly_chart(fig_bar, use_container_width=True)

f_top = df_fuentes.iloc[-1]
lena = df_fuentes[df_fuentes["tipo_fuente"].str.contains("leña", case=False)]["pct"].sum()
st.info(f"💡 **Interpretación:** para {contaminante_sel}, **{f_top['tipo_fuente']}** aporta el {f_top['pct']:.1f}% "
        f"de las toneladas. Las fuentes de leña juntas suman el {lena:.1f}%. Cambia el contaminante en el panel "
        "lateral para ver si el orden de las fuentes se mantiene.")

# Dispersión por Grupos (Boxplot) 
st.header("4. Comparación de Dispersión (Boxplot)")

agrupar = st.radio("Agrupar el gráfico por:", ["Tipo de fuente", "Región"], horizontal=True)
columna_agrupar = "region" if agrupar == "Región" else "tipo_fuente"

fig_box = px.box(
    df_grafico,
    x=columna_agrupar,
    y="cantidad_toneladas",
    color=columna_agrupar,
    log_y=True,
    labels=ETIQUETAS,
    title=f"Distribución de {contaminante_sel} agrupado por {agrupar.lower()} (escala log)"
)
fig_box.update_layout(showlegend=False)
st.plotly_chart(fig_box, use_container_width=True)

g = df_grafico.groupby(columna_agrupar)["cantidad_toneladas"].agg(["median", "mean", "max"])
g["cola"] = g["mean"] / g["median"]
g_cola = g["cola"].idxmax()
st.info(f"💡 **Interpretación:** la mediana por registro es mayor en **{g['median'].idxmax()}** "
        f"({g['median'].max():,.1f} t) y menor en **{g['median'].idxmin()}** ({g['median'].min():,.1f} t). "
        f"La cola más pesada es la de **{g_cola}**: su media es {g.loc[g_cola, 'cola']:,.1f} veces su mediana "
        f"y su máximo llega a {g.loc[g_cola, 'max']:,.0f} t.")

# Visualización de los valores
with st.expander("Ver los 10 registros con mayores emisiones (Valores Atípicos)"):
    top_10 = df_filtrado.nlargest(10, "cantidad_toneladas")[["año", "region", "comuna", "tipo_fuente", "cantidad_toneladas"]]
    st.dataframe(top_10, use_container_width=True)

# grafico barras por Composición Regional
st.header("5. Composición de Emisiones por Región")

# Agrupación por región y fuente
df_region_fuente = df_filtrado.groupby(["region", "tipo_fuente"], as_index=False)["cantidad_toneladas"].sum()

fig_stack = px.bar(
    df_region_fuente,
    x="region",
    y="cantidad_toneladas",
    color="tipo_fuente",
    labels=ETIQUETAS,
    title=f"Toneladas de {contaminante_sel} por Región y Tipo de Fuente"
)
fig_stack.update_layout(legend_title_text="Fuente")
st.plotly_chart(fig_stack, use_container_width=True)

tot_reg = df_region_fuente.groupby("region")["cantidad_toneladas"].sum()
r_top = tot_reg.idxmax()
dom = df_region_fuente.loc[df_region_fuente.groupby("region")["cantidad_toneladas"].idxmax()].set_index("region")
d_top = dom.loc[r_top]
n_lena = int(dom["tipo_fuente"].str.contains("leña", case=False).sum())
st.info(f"💡 **Interpretación:** la región con más toneladas de {contaminante_sel} es **{r_top}** "
        f"({tot_reg[r_top]:,.0f} t, {tot_reg[r_top] / tot_reg.sum() * 100:.1f}% del total), donde predomina "
        f"**{d_top['tipo_fuente']}**. En {n_lena} de {len(dom)} regiones la fuente principal es la leña; "
        "en las demás predomina otra fuente.")