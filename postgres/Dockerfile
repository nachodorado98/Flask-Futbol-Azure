FROM postgres:16

COPY init.sql /docker-entrypoint-initdb.d/

COPY data/ligas.csv /docker-entrypoint-initdb.d/ligas.csv