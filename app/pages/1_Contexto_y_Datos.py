import streamlit as st
import pandas as pd

st.title("1. Contexto y Datos")

# Carga de datos y almacenamiento en sesión

if "datos" not in st.session_state:
    try:
        
        df = pd.read_csv("../data/processed/emisiones_centro_sur_2019_2024.csv")
        df["tipo_fuente"] = df["tipo_fuente"].replace({
        "Combustión de Leña Residencial Urbana": "Leña residencial urbana",
        "Combustión de leña Rural Urbana": "Leña residencial rural",
        })
        st.session_state["datos"] = df
    except FileNotFoundError:
        st.error("No se encontró el archivo de datos. Verifica que ejecutaste el notebook de limpieza.")
        st.stop()

df = st.session_state["datos"]

st.header("Problema, pregunta y alcance")
st.markdown(
    "Las fuentes difusas (leña residencial, quemas agrícolas, incendios forestales) "
    "emiten contaminantes al aire sin una chimenea o punto único identificable. "
    "En la zona centro-sur de Chile pueden afectar la calidad del aire de las comunas."
)
st.info("¿Cómo se distribuyen y han evolucionado las emisiones atmosféricas por fuentes "
        "difusas en las comunas de la zona centro-sur de Chile entre 2019 y 2024?")
 
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Variable (X)**")
    st.markdown("Región y comuna, tipo de fuente, contaminante y zona rural/urbana.")
with col2:
    st.markdown("**Objetivo (Y)**")
    st.markdown("Emisiones estimadas, en toneladas (`cantidad_toneladas`).")
with col3:
    st.markdown("**Temporalidad (T)**")
    st.markdown("Año, de 2019 a 2024 (6 años).")
st.markdown("**Alcance:** zona centro-sur, de Maule a Los Lagos. "
            "Excluye fuentes fijas industriales, parque vehicular y mediciones de monitoreo.")

# Descripción y Calidad de Datos 
st.header("Auditoría y Calidad de los Datos")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Registros", f"{len(df):,}")
m2.metric("Variables", df.shape[1])
m3.metric("Regiones", df["region"].nunique())
m4.metric("Comunas", df["comuna"].nunique())
m5.metric("Periodo", f"{df['año'].min()}–{df['año'].max()}")


st.markdown("**Tratamiento de Datos y Decisiones (Data Cleaning)**")
st.markdown("""
| Hallazgo / Inconsistencia | Acción correctiva tomada en pre-procesamiento |
|---|---|
| Múltiples archivos anuales pesados | Consolidación y agrupación por año, comuna y fuente para optimizar rendimiento de la app. |
| Tipos de datos numéricos mal formateados | Conversión de comas a puntos y casteo a `float` en la columna de toneladas. |
| Variable `Rural o Urbano` vacía al 93% | Se conservó por trazabilidad, pero la segmentación principal se hace a través de `tipo_fuente`. |
""")

st.dataframe(df.head(5), use_container_width=True)