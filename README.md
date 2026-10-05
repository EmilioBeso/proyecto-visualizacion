## Integrantes; 
Emilio Besoain, Rony huenuñanco

## Descripcion:
Las emisiones atmosféricas generadas por fuentes difusas (combustión de leña residencial, quemas agrícolas e incendios forestales) tienen menor visibilidad pública que la gran industria, pero afectan directamente la calidad del aire a nivel comunal en Chile.

## Motivacion:
En la zona centro sur del país, la combustión de leña representa la principal causa de emisión de gases. Analizar estos datos permite identificar qué comunas absorben la mayor carga contaminante para orientar la toma de decisiones en salud pública y medio ambiente.

## Pregunta:
¿Cómo se distribuyen y han evolucionado las emisiones atmosféricas por fuentes difusas en las comunas de Chile entre 2019 y 2024, y qué zonas concentran los mayores niveles de contaminación por leña y quemas agrícolas?

## Alcance:
Se investigan las comunas de Chile, pero con un enfoque en la zona centro sur. con un periodo investigado del año 2019 hasta el 2024.
los limites es que no veremos la produccion de gases de industrias, vehiculos, etc

## Estructura X, Y, T:
X = tipo_fuente, contaminantes, region, provincia, comuna, Rural o Urbano, Lat, Lon.
Y = cantidad_toneladas
T = año

## Fuente del Dataset:
Registro de Emisiones y Transferencias de Contaminantes - ministerio del medioambiente
https://datos.gob.cl/dataset/emisiones-al-aire-de-fuentes-difusas

Los datos dentro del database muestran registros de que tipo de fuente han ocurrido en lugar y año especificos, tambien cuantificando la masa emitida en toneladas y su contaminante

## Problema y Pregunta:
En Chile al igual que en varios paises existen los gases causados por la quema de leña, queremos encontrar una forma en la cual podramos identificar como es que van evolucionando las emisiones de estos segun las zonas del pais de una forma que estos datos se puedan entender de forma visual, por lo cual añadiendole a nuestra pregunta; ¿Cómo se distribuyen y han evolucionado las emisiones atmosféricas por fuentes difusas en las comunas de Chile entre 2019 y 2024, y qué zonas concentran los mayores niveles de contaminación por leña y quemas agrícolas? 
tambien buscamos que se pueda visualizar con graficos

## Descripcion del Dataset:
El dataset utilizado representan las estimaciones oficiales del Ministerio del Medio Ambiente desde el año 2019 hasta el 2024 sobre la masa de contaminantes vertidos al aire por actividades no industriales ni vehiculares (leña, quemas, incendios, uso de solventes) en las reciones centro-sur de Chile, separandolo por tipo de fuente, contaminante, provincia y comuna. ​

## Instrucciones para Obtener los Datos:
El dataset completo es una combinacion de archivos encontrados en datos.gob.cl en la seccion de Emisiones al aire de fuentes difusas, tomando los años del 2019 hasta el 2024, estos archivos fueron procesados en un notebook para agrupar los distintos años y resumirlos a la vez

## Instrucciones para Ejecutar la Aplicacion:
Descargar el archivo mediante github

Abrir el archivo en VS Code

En el terminal descargar las librerias con este comando; pip install -r requirements.txt

En el terminal escribir; cd app

Una vez dentro de la carpeta app escribir en el terminal; streamlit run app.py

Si no se abre la pagina con la aplicacion entrar manualmente al localhost

## Aependencias Principales:
El sistema utiliza bibliotecas tales como pandas, streamlit, plotlit express o numpy

## Breve descripcion de las paginas de la aplicacion:
En la pagina app se encuentra una introduccion donde se explica brevemente el contexto del proyecto, y tambien que para acceder a la informacion visual se debe de acceder en el menu lateral.

En la pagina 1 se define el problema, la pregunta de investigación y el alcance del estudio (variables, objetivo y temporalidad). Aparte muestra los datos despues de la limpieza.

En la pagina 2 se encuentra la página interactiva principal donde el usuario puede filtrar la información por tipo de contaminante y región mostrando los datos en varios graficos.

En la pagina 3 se fija el análisis específicamente en el material particulado MP2,5 por ser el más crítico para la salud, aparte que tiene la seccion para ver los hotspots y da una conclusion dado con los datos obtenidos.

## Estrucura del repositorio:

```text
├── data/
│   ├── raw/        
│   └── processed/
│       └──emisiones_centro_sur_2019_2024.csv
├── notebooks/      
│   ├── 01_exploracion.ipynb
│   └── 02_eda.ipynb
├── src/             
├── figures/         
├── app/
│   ├──app.py
│   └── pages/
│       ├── 1_Contexto_y_Datos.py
│       ├── 2_Analisis_Exploratorio(EDA).py
│       └── 3_Analisis_de_la_Pregunta.py
│
├── .gitignore       
└── README.md
