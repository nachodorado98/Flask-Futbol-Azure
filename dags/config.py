# Comandos BASH para crear las carpetas
BASH_LOGS="cd ../../opt/airflow/dags && mkdir -p entorno/logs"
BASH_ESCUDOS="cd ../../opt/airflow/dags && mkdir -p entorno/imagenes/escudos"
BASH_ENTRENADORES="cd ../../opt/airflow/dags && mkdir -p entorno/imagenes/entrenadores"
BASH_PRESIDENTES="cd ../../opt/airflow/dags && mkdir -p entorno/imagenes/presidentes"
BASH_ESTADIOS="cd ../../opt/airflow/dags && mkdir -p entorno/imagenes/estadios"
BASH_COMPETICIONES="cd ../../opt/airflow/dags && mkdir -p entorno/imagenes/competiciones"
BASH_PAISES="cd ../../opt/airflow/dags && mkdir -p entorno/imagenes/paises"

# URL para descargar las imagenes
URL_ESCUDO="https://cdn.resfu.com/img_data/equipos/"
URL_ESCUDO_ALTERNATIVA="https://cdn.resfu.com/img_data/escudos/medium/"
URL_ENTRENADOR="https://cdn.resfu.com/img_data/people/original/"
URL_PRESIDENTE="https://cdn.resfu.com/img_data/people/original/"
URL_ESTADIO="https://cdn.resfu.com/img_data/estadios/original_new/"
URL_COMPETICION="https://cdn.resfu.com/media/img/league_logos/"
URL_PAIS="https://cdn.resfu.com/media/img/flags/round/"

# Contenedor y carpetas para el datalake
CONTENEDOR="contenedorequipos"
ESCUDOS="escudos"
ENTRENADORES="entrenadores"
PRESIDENTES="presidentes"
ESTADIOS="estadios"
COMPETICIONES="competiciones"
PAISES="paises"

# Carpetas para las tablas en el datalake
TABLA_EQUIPOS="tablas/equipos"
TABLA_ESTADIOS="tablas/estadios"
TABLA_EQUIPO_ESTADIO="tablas/equipo_estadio"
TABLA_PARTIDOS="tablas/partidos"
TABLA_PARTIDO_ESTADIO="tablas/partido_estadio"
TABLA_COMPETICIONES="tablas/competiciones"

EQUIPO_ID=369 # Atletico de Madrid. Numero del escudo realmente, no el equipo_id. La web crea asi la URL
TEMPORADA_INICIO=2024 # Año de inicio minimo: 1921. Año de inicio maximo: Año actual
MES_FIN_TEMPORADA=6 # Mes para indicar un cambio de temporada. El mes 6, Junio, sera el ultimo mes de la temporada actual.