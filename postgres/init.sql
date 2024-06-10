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

CREATE TABLE estadios (Estadio_Id VARCHAR(255) PRIMARY KEY,
						Codigo_Estadio INTEGER,
						Nombre VARCHAR(255),
						Direccion VARCHAR(255),
						Latitud DOUBLE PRECISION,
						Longitud DOUBLE PRECISION,
						Ciudad VARCHAR(255),
						Capacidad INTEGER,
						Fecha INTEGER,
						Largo INTEGER,
						Ancho INTEGER,
						Telefono VARCHAR(255),
						Cesped VARCHAR(255));

CREATE TABLE equipo_estadio (Equipo_Id VARCHAR(255),
							Estadio_Id VARCHAR(255),
							PRIMARY KEY (Equipo_Id, Estadio_Id),
							FOREIGN KEY (Equipo_Id) REFERENCES equipos (Equipo_Id) ON DELETE CASCADE,
							FOREIGN KEY (Estadio_Id) REFERENCES estadios (Estadio_Id) ON DELETE CASCADE);