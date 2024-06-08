FROM postgres:13

ENV POSTGRES_USER airflow
ENV POSTGRES_PASSWORD airflow
ENV POSTGRES_DB airflow

COPY init.sql /docker-entrypoint-initdb.d/init.sql

COPY data/ligas.csv /docker-entrypoint-initdb.d/ligas.csv

CMD ["postgres"]