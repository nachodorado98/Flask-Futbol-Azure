FROM postgres:13

ENV POSTGRES_USER airflow
ENV POSTGRES_PASSWORD airflow
ENV POSTGRES_DB airflow

COPY init.sql /docker-entrypoint-initdb.d/init.sql

COPY data/ligas.csv /docker-entrypoint-initdb.d/ligas.csv
COPY data/ciudades.csv /docker-entrypoint-initdb.d/ciudades.csv
COPY data/paises.csv /docker-entrypoint-initdb.d/paises.csv

CMD ["postgres"]