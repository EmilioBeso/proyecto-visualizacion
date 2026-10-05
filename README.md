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
X = tipo_fuente, contaminantes, region, provincia, comuna, Rural o Urbano, Lat, Lon.
Y = cantidad_toneladas
T = año

## fuente del dataset:
Registro de Emisiones y Transferencias de Contaminantes - ministerio del medioambiente
https://datos.gob.cl/dataset/emisiones-al-aire-de-fuentes-difusas

Los datos dentro del database muestran registros de que tipo de fuente han ocurrido en lugar y año especificos, tambien cuantificando la masa emitida en toneladas y su contaminante

## problema y pregunta:
En Chile al igual que en varios paises existen los gases causados por la quema de leña, queremos encontrar una forma en la cual podramos identificar como es que van evolucionando las emisiones de estos segun las zonas del pais de una forma que estos datos se puedan entender de forma visual, por lo cual añadiendole a nuestra pregunta; ¿Cómo se distribuyen y han evolucionado las emisiones atmosféricas por fuentes difusas en las comunas de Chile entre 2019 y 2024, y qué zonas concentran los mayores niveles de contaminación por leña y quemas agrícolas? 
tambien buscamos que se pueda visualizar con graficos

## descripcion del dataset:
El dataset utilizado representan las estimaciones oficiales del Ministerio del Medio Ambiente desde el año 2019 hasta el 2024 sobre la masa de contaminantes vertidos al aire por actividades no industriales ni vehiculares (leña, quemas, incendios, uso de solventes) en las reciones centro-sur de Chile, separandolo por tipo de fuente, contaminante, provincia y comuna. ​

## instrucciones para obtener los datos:
El dataset completo es una combinacion de archivos encontrados en datos.gob.cl en la seccion de Emisiones al aire de fuentes difusas, tomando los años del 2019 hasta el 2024, estos archivos fueron procesados en un notebook para agrupar los distintos años y resumirlos a la vez

## instrucciones para ejecutar la aplicacion:


## dependencias principales:
El sistema utiliza bibliotecas tales como pandas, streamlit, plotlit express o numpy

## breve descripcion de las paginas de la aplicacion:


## Estrucura del repositorio:

```text
├── data/
│   ├── raw/         
│   └── processed/  
├── notebooks/      
│   ├── 01_exploracion.ipynb
│   └── 02_eda.ipynb
├── src/             
├── figures/         
├── app/
│   ├──app.py
│   └── pages/
│       ├── 1_Contexto.py
│       ├── 2_EDA.py
│       └── 3_Analisis.py
│
├── .gitignore       
└── README.md
