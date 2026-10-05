import plotly.express as px
import streamlit as st

# Verificacion de carga de datos
if "datos" not in st.session_state:
    st.warning("Vaya a la página 'Contexto' para cargar los datos.")
    st.stop()

# Recuperamos los datos
df = st.session_state["datos"]

st.title("3. Análisis de la Pregunta")
st.markdown("¿Qué nos dicen realmente los datos sobre nuestra problemática?")

# Filtros interactivos
st.sidebar.header("Filtros del análisis")

contaminantes = sorted(df["contaminantes"].dropna().unique())
contaminante_sel = st.sidebar.selectbox(
    "Contaminante", contaminantes,
    index=contaminantes.index("MP2,5") if "MP2,5" in contaminantes else 0
    
)

anios = sorted(df["año"].dropna().unique())
anio_sel = st.sidebar.multiselect("Años a analizar", anios, default=anios)

regiones = sorted(df["region"].dropna().unique())
region_sel = st.sidebar.multiselect("Regiones", regiones, default=regiones)

fuentes = sorted(df["tipo_fuente"].dropna().unique())
fuente_sel = st.sidebar.multiselect("Tipos de fuente", fuentes, default=fuentes)

top_n = st.sidebar.slider("Comunas en el ranking", 5, 20, 10)


# Aplicar todos los filtros al dataframe
df_filtrado = df[
    (df["contaminantes"] == contaminante_sel) & 
    (df["año"].isin(anio_sel)) & 
    (df["region"].isin(region_sel)) & 
    (df["tipo_fuente"].isin(fuente_sel))
]

if df_filtrado.empty:
    st.warning("No hay datos para esta combinación de filtros.")
    st.stop()

st.markdown(f"**Pregunta del Proyecto:** ¿Cómo se distribuyen y han evolucionado las emisiones por fuentes difusas en la zona centro-sur, y qué comunas son las más críticas?")

col1, col2 = st.columns(2)

# Dimensión Espacial (Ranking)
with col1:
    st.subheader(f"Comunas más críticas (Top {top_n})")
    
    # Sumar toneladas totales por comuna para sacar el Top
    tot_comuna = df_filtrado.groupby(["region", "comuna"], as_index=False)["cantidad_toneladas"].sum()
    top_comunas = tot_comuna.nlargest(top_n, "cantidad_toneladas")
    lista_comunas_top = top_comunas["comuna"].tolist()
    
    # Filtrar solo las comunas del Top y agrupar por fuente para el gráfico apilado
    df_top = df_filtrado[df_filtrado["comuna"].isin(lista_comunas_top)]
    df_grafico_top = df_top.groupby(["comuna", "tipo_fuente"], as_index=False)["cantidad_toneladas"].sum()
    
    fig_top = px.bar(
        df_grafico_top, 
        x="comuna", 
        y="cantidad_toneladas", 
        color="tipo_fuente",
        category_orders={"comuna": lista_comunas_top},
        labels={"cantidad_toneladas": "Toneladas", "comuna": "Comuna", "tipo_fuente": "Fuente"},
        title=f"Composición de emisiones en el Top {top_n}"
    )
    fig_top.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_top, use_container_width=True)

    # Cálculos para la interpretación
    comuna_critica = top_comunas.iloc[0]['comuna']
    toneladas_critica = top_comunas.iloc[0]['cantidad_toneladas']
    porcentaje_top = (top_comunas["cantidad_toneladas"].sum() / tot_comuna["cantidad_toneladas"].sum()) * 100
    
    st.info(f"💡 **Interpretación:** La comuna con mayor urgencia es **{comuna_critica}** con {toneladas_critica:,.0f} toneladas acumuladas. "
            f"El Top {top_n} concentra el **{porcentaje_top:.1f}%** de las emisiones de toda la zona seleccionada. "
            f"Al estar en toneladas absolutas, este ranking tiende a destacar a las comunas más grandes o pobladas.")

# Dimensión Temporal
with col2:
    st.subheader("Evolución Anual (Serie de Tiempo)")
    
    agrupar_por = st.radio("Desglosar línea de tiempo por:", ["Tipo de fuente", "Región"], horizontal=True)
    col_agrupacion = "tipo_fuente" if agrupar_por == "Tipo de fuente" else "region"
    
    # Agrupar por año y la variable seleccionada
    df_evolucion = df_filtrado.groupby(["año", col_agrupacion], as_index=False)["cantidad_toneladas"].sum()
    
    fig_line = px.line(
        df_evolucion, 
        x="año", 
        y="cantidad_toneladas", 
        color=col_agrupacion, 
        markers=True,
        labels={"cantidad_toneladas": "Toneladas", "año": "Año"},
        title=f"Tendencia de {contaminante_sel} por {agrupar_por.lower()}"
    )
    fig_line.update_xaxes(dtick=1) # Hace que se vean de 1 en 1 (ej: 2019, 2020)
    
    
    st.plotly_chart(fig_line, use_container_width=True)

    # Calcular el año top
    tot_por_anio = df_filtrado.groupby("año")["cantidad_toneladas"].sum()
    if len(tot_por_anio) >= 3:
        anio_pico = tot_por_anio.idxmax()
        toneladas_pico = tot_por_anio.max()
        st.info(f"💡 **Interpretación:** El año con mayores emisiones fue **{anio_pico}** ({toneladas_pico:,.0f} t). "
                "En el gráfico se puede apreciar visualmente si los picos corresponden a eventos episódicos (como megaincendios) "
                "o si existe una carga constante a lo largo de los años (como la leña residencial).")
    else:
        st.info("💡 Seleccione al menos 3 años en los filtros para poder interpretar una evolución temporal.")

# Hallazgos y Conclusiones
st.markdown("---")
st.header("Hallazgos Principales y Refinamiento de la Pregunta")

# Cálculos para el texto final
total_toneladas = df_filtrado["cantidad_toneladas"].sum()
df_resumen_fuentes = df_filtrado.groupby("tipo_fuente")["cantidad_toneladas"].sum().reset_index()
df_resumen_fuentes["porcentaje"] = (df_resumen_fuentes["cantidad_toneladas"] / total_toneladas) * 100
df_resumen_fuentes = df_resumen_fuentes.sort_values("porcentaje", ascending=False)

fuente_principal = df_resumen_fuentes.iloc[0]["tipo_fuente"]
pct_principal = df_resumen_fuentes.iloc[0]["porcentaje"]

st.success(f"""
**1. Peso de las Fuentes:** Los datos revelan que la categoría predominante es **{fuente_principal}**, responsable del **{pct_principal:.1f}%** del total emitido bajo los filtros actuales.

**2. Asimetría Espacial:** Existen dos tipos de "hotspots" (zonas críticas). Por un lado, grandes ciudades donde predomina una contaminación estructural (ej. uso constante de leña). Por otro lado, comunas rurales que sufren picos episódicos severos (ej. incendios forestales).

**3. Anomalías Temporales:** La serie de tiempo demuestra que algunos años concentran la mayor parte del tonelaje debido a eventos extremos, lo que justifica la necesidad de separar el análisis de fuentes constantes vs. fuentes episódicas.
""")

st.subheader("Limitaciones del EDA actual y Siguientes Pasos (Hacia el Avance 3)")
st.markdown("""
*   **Sesgo poblacional/territorial:** Las toneladas están en valores absolutos. Una comuna grande lógicamente emitirá más que una pequeña.
*   **Próximo paso (Feature Engineering):** Para obtener una comparación justa y real del riesgo, es imperativo cruzar estos datos con la población (Censo/INE) o la superficie comunal, creando una métrica de **"tasa de emisión per cápita"** o **"densidad de emisiones"**.
*   **Mejora visual:** Incorporar un mapa coroplético que permita ver la distribución geográfica real de las comunas más afectadas.
""")