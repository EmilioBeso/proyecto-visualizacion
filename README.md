## integrantes; 
Emilio Besoain, Rony huenuñanco

## desc:
Las emisiones atmosféricas generadas por fuentes difusas (combustión de leña residencial, quemas agrícolas e incendios forestales) tienen menor visibilidad pública que la gran industria, pero afectan directamente la calidad del aire a nivel comunal en Chile.

## motivacion:
En la zona centro sur del país, la combustión de leña representa la principal causa de emisión de gases. Analizar estos datos permite identificar qué comunas absorben la mayor carga contaminante para orientar la toma de decisiones en salud pública y medio ambiente.

## pregunta:
¿Cómo se distribuyen y han evolucionado las emisiones atmosféricas por fuentes difusas en las comunas de Chile entre 2019 y 2024, y qué zonas concentran los mayores niveles de contaminación por leña y quemas agrícolas?

## alcance:
Se investigan las comunas de Chile, pero con un enfoque en la zona centro sur. con un periodo investigado del año 2019 hasta el 2024.
los limites es que no veremos la produccion de gases de industrias, vehiculos, etc

## estructura x, y, t:
X = tipo_fuente, contaminant, region, provincia, comuna, Rural o Urbano, Lat, Lon.
Y = cantidad_ton
T = año

## fuente del dataset:
Registro de Emisiones y Transferencias de Contaminantes - ministerio del medioambiente
https://datos.gob.cl/dataset/emisiones-al-aire-de-fuentes-difusas

Los datos dentro del database muestran registros de que tipo de fuente han ocurrido en lugar y año especificos, tambien cuantificando la masa emitida en toneladas y su contaminante

## Estrucura del repositorio

```text
├── data/
│   ├── raw/         # Datos originales descargados (excluidos en .gitignore)
│   └── processed/   # Dataset unificado 2019-2024
├── notebooks/       # Notebooks de exploración y análisis (EDA)
│   └── 01_exploracion.ipynb
├── src/             # Scripts de Python para carga y limpieza
├── figures/         # Gráficos y recursos visuales exportados
├── app/             # Aplicación interactiva (Streamlit / Plotly)
├── .gitignore       # Archivos excluidos del control de versiones
└── README.md        # Documentación principal del proyecto