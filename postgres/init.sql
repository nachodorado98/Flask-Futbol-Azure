CREATE DATABASE bbdd_futbol_data;

\c bbdd_futbol_data;

CREATE TABLE ligas (Id INTEGER PRIMARY KEY,
					Nombre VARCHAR(255));

\copy ligas (Id, Nombre) FROM '/docker-entrypoint-initdb.d/ligas.csv' WITH CSV HEADER;

CREATE TABLE equipos (Equipo_Id VARCHAR(255) PRIMARY KEY,
						Nombre_Completo VARCHAR(255) DEFAULT NULL,
						Nombre VARCHAR(255) DEFAULT NULL,
						Siglas CHAR(3) DEFAULT NULL,
						Escudo INTEGER DEFAULT NULL,
						Puntuacion INTEGER DEFAULT NULL,
						Pais VARCHAR(255) DEFAULT NULL,
						Codigo_Pais VARCHAR(5) DEFAULT NULL,
						Ciudad VARCHAR(255) DEFAULT NULL,
						Competicion VARCHAR(255) DEFAULT NULL,
						Codigo_Competicion VARCHAR(255) DEFAULT NULL,
						Temporadas INTEGER DEFAULT NULL,
						Estadio VARCHAR(255) DEFAULT NULL,
						Fundacion INTEGER DEFAULT NULL,
						Entrenador VARCHAR(255) DEFAULT NULL,
						Entrenador_URL VARCHAR(255) DEFAULT NULL,
						Codigo_Entrenador INTEGER DEFAULT NULL,
						Partidos INTEGER DEFAULT NULL,
						Presidente VARCHAR(255) DEFAULT NULL,
						Presidente_URL VARCHAR(255) DEFAULT NULL,
						Codigo_Presidente INTEGER DEFAULT NULL);