import streamlit as st

# Configuración global de la página
st.set_page_config(
    page_title="Emisiones Difusas Chile",
    layout="wide"
)

st.title("Dashboard de Emisiones de Fuentes Difusas (2019-2024)")
st.markdown("---")

st.markdown("""
### Bienvenido a la plataforma de exploración de emisiones atmosféricas
Las emisiones generadas por fuentes difusas (combustión de leña, quemas agrícolas, incendios forestales) impactan directamente la calidad del aire a nivel comunal en la zona centro-sur de Chile.

**Por favor, selecciona una página en el menú lateral de la izquierda para comenzar:**
1. **Contexto y Datos:** Conoce la problemática, la pregunta de investigación y la base de datos.
2. **Análisis Exploratorio (EDA):** Filtra e interactúa con las distribuciones de los contaminantes.
3. **Análisis de la Pregunta:** Descubre los *hotspots* (comunas críticas) y la evolución temporal.
""")
