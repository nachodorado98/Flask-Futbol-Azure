CREATE DATABASE bbdd_futbol_data;

\c bbdd_futbol_data;

CREATE TABLE ligas_scrapear (Id INTEGER PRIMARY KEY,
					Nombre VARCHAR(255));

\copy ligas_scrapear (Id, Nombre) FROM '/docker-entrypoint-initdb.d/ligas.csv' WITH CSV HEADER;

CREATE TABLE paises (Pais VARCHAR(50) PRIMARY KEY,
					PaisIngles VARCHAR(50));

\copy paises (Pais, PaisIngles) FROM '/docker-entrypoint-initdb.d/paises.csv' WITH CSV HEADER;

CREATE TABLE ciudades (CodCiudad SERIAL PRIMARY KEY,
						Ciudad VARCHAR(50),
						Latitud VARCHAR(50),
						Longitud VARCHAR(50),
						Pais VARCHAR(50),
						Siglas CHAR(3),
						Tipo VARCHAR(50),
						Poblacion INT,
						FOREIGN KEY (Pais) REFERENCES paises (Pais));

\copy ciudades (Ciudad, Latitud, Longitud, Pais, Siglas, Tipo, Poblacion) FROM '/docker-entrypoint-initdb.d/ciudades.csv' WITH CSV HEADER;

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
						Cesped VARCHAR(255),
						Pais VARCHAR(255) DEFAULT NULL,
						Codigo_Pais VARCHAR(5) DEFAULT NULL);

CREATE TABLE equipo_estadio (Equipo_Id VARCHAR(255),
							Estadio_Id VARCHAR(255),
							PRIMARY KEY (Equipo_Id, Estadio_Id),
							FOREIGN KEY (Equipo_Id) REFERENCES equipos (Equipo_Id) ON DELETE CASCADE,
							FOREIGN KEY (Estadio_Id) REFERENCES estadios (Estadio_Id) ON DELETE CASCADE);

CREATE TABLE partidos (Partido_Id VARCHAR(255) PRIMARY KEY,
						Equipo_Id_Local VARCHAR(255),
						Equipo_Id_Visitante VARCHAR(255),
						Fecha DATE,
						Hora CHAR(5),
						Competicion VARCHAR(255),
						Marcador VARCHAR(255),
						Resultado VARCHAR(255),
						FOREIGN KEY (Equipo_Id_Local) REFERENCES equipos (Equipo_Id) ON DELETE CASCADE,
						FOREIGN KEY (Equipo_Id_Visitante) REFERENCES equipos (Equipo_Id) ON DELETE CASCADE);

CREATE TABLE proximos_partidos (Partido_Id VARCHAR(255) PRIMARY KEY,
								Equipo_Id_Local VARCHAR(255),
								Equipo_Id_Visitante VARCHAR(255),
								Fecha DATE,
								Hora CHAR(5),
								Competicion VARCHAR(255),
								FOREIGN KEY (Equipo_Id_Local) REFERENCES equipos (Equipo_Id) ON DELETE CASCADE,
								FOREIGN KEY (Equipo_Id_Visitante) REFERENCES equipos (Equipo_Id) ON DELETE CASCADE);

CREATE TABLE partido_estadio (Partido_Id VARCHAR(255),
							Estadio_Id VARCHAR(255),
							PRIMARY KEY (Partido_Id, Estadio_Id),
							FOREIGN KEY (Partido_Id) REFERENCES partidos (Partido_Id) ON DELETE CASCADE,
							FOREIGN KEY (Estadio_Id) REFERENCES estadios (Estadio_Id) ON DELETE CASCADE);

CREATE TABLE competiciones (Competicion_Id VARCHAR(255) PRIMARY KEY,
							Nombre VARCHAR(255) DEFAULT NULL,
							Codigo_Logo VARCHAR(255) DEFAULT NULL,
							Codigo_Pais VARCHAR(5) DEFAULT NULL);

CREATE TABLE competiciones_campeones (Competicion_Id VARCHAR(255),
										Temporada INTEGER,
										Equipo_Id VARCHAR(255),
										PRIMARY KEY (Competicion_Id, Temporada, Equipo_Id),
										FOREIGN KEY (Competicion_Id) REFERENCES competiciones (Competicion_Id) ON DELETE CASCADE);

CREATE TABLE partido_competicion (Partido_Id VARCHAR(255),
									Competicion_Id VARCHAR(255),
									PRIMARY KEY (Partido_Id, Competicion_Id),
									FOREIGN KEY (Partido_Id) REFERENCES partidos (Partido_Id) ON DELETE CASCADE,
									FOREIGN KEY (Competicion_Id) REFERENCES competiciones (Competicion_Id) ON DELETE CASCADE);

CREATE TABLE jugadores (Jugador_Id VARCHAR(255) PRIMARY KEY,
						Nombre VARCHAR(255) DEFAULT NULL,
						Equipo_Id VARCHAR(255) DEFAULT NULL,
						Codigo_Pais VARCHAR(5) DEFAULT NULL,
						Codigo_Jugador VARCHAR(15) DEFAULT NULL,
						Puntuacion INTEGER DEFAULT NULL,
						Valor DOUBLE PRECISION DEFAULT NULL,
						Dorsal INTEGER DEFAULT NULL,
						Posicion VARCHAR(5) DEFAULT NULL);

CREATE TABLE jugadores_equipo (Jugador_Id VARCHAR(255),
								Equipo_Id VARCHAR(255),
								Temporadas INTEGER,
								Goles INTEGER,
								Partidos INTEGER,
								PRIMARY KEY (Jugador_Id, Equipo_Id),
								FOREIGN KEY (Jugador_Id) REFERENCES jugadores (Jugador_Id) ON DELETE CASCADE,
								FOREIGN KEY (Equipo_Id) REFERENCES equipos (Equipo_Id) ON DELETE CASCADE);

CREATE TABLE jugadores_seleccion (Jugador_Id VARCHAR(255) PRIMARY KEY,
									Codigo_Seleccion INTEGER,
									Convocatorias INTEGER,
									Goles INTEGER,
									Asistencias INTEGER,
									FOREIGN KEY (Jugador_Id) REFERENCES jugadores (Jugador_Id) ON DELETE CASCADE);

CREATE TABLE partido_goleador (Partido_Id VARCHAR(255),
								Jugador_Id VARCHAR(255),
								Minuto INTEGER,
								Anadido INTEGER,
								Local BOOL,
								PRIMARY KEY (Partido_Id, Jugador_Id, Minuto, Anadido),
								FOREIGN KEY (Partido_Id) REFERENCES partidos (Partido_Id) ON DELETE CASCADE,
								FOREIGN KEY (Jugador_Id) REFERENCES jugadores (Jugador_Id) ON DELETE CASCADE);

CREATE TABLE entrenadores (Entrenador_Id VARCHAR(255) PRIMARY KEY,
							Nombre VARCHAR(255) DEFAULT NULL,
							Equipo_Id VARCHAR(255) DEFAULT NULL,
							Codigo_Pais VARCHAR(5) DEFAULT NULL,
							Codigo_Entrenador VARCHAR(15) DEFAULT NULL,
							Puntuacion INTEGER DEFAULT NULL);

CREATE TABLE temporada_jugadores (Temporada INTEGER);

CREATE TABLE variables (Nombre VARCHAR(255) PRIMARY KEY,
						Valor VARCHAR(255));

INSERT INTO variables (Nombre, Valor)
VALUES ('DAG_EQUIPOS_EJECUTADO', 'False'),
		('DAG_PARTIDOS_EJECUTADO', 'False'),
		('DAG_COMPETICIONES_EJECUTADO', 'False'),
		('DAG_JUGADORES_EJECUTADO', 'False'),
		('DAG_ESTADIOS_EJECUTADO', 'False'),
		('DAG_ENTRENADORES_EJECUTADO', 'False');

CREATE TABLE usuarios (Usuario VARCHAR(255) PRIMARY KEY,
						Correo VARCHAR(255),
						Contrasena VARCHAR(255),
						Nombre VARCHAR(255),
						Apellido VARCHAR(255),
						Fecha_Nacimiento DATE,
						CodCiudad INT,
						Equipo_Id VARCHAR(255),
						FOREIGN KEY (Equipo_Id) REFERENCES equipos (Equipo_Id) ON DELETE CASCADE,
						FOREIGN KEY (CodCiudad) REFERENCES ciudades (CodCiudad));

CREATE TABLE partidos_asistidos (Asistido_Id VARCHAR(255) PRIMARY KEY,
								Partido_Id VARCHAR(255),
								Usuario VARCHAR(255),
								Comentario VARCHAR(255) DEFAULT NULL,
								Imagen VARCHAR(255) DEFAULT NULL,
								On_Tour BOOL DEFAULT False,
								Fecha_Ida DATE DEFAULT NULL,
								Fecha_Vuelta DATE DEFAULT NULL,
								Teletrabajo BOOL DEFAULT NULL,
								FOREIGN KEY (Partido_Id) REFERENCES partidos (Partido_Id) ON DELETE CASCADE,
								FOREIGN KEY (Usuario) REFERENCES usuarios (Usuario) ON DELETE CASCADE,
								CONSTRAINT check_fechas CHECK (Fecha_Ida <= Fecha_Vuelta));

CREATE TABLE partido_asistido_favorito (Partido_Id VARCHAR(255),
										Usuario VARCHAR(255),
										PRIMARY KEY (Partido_Id, Usuario),
										FOREIGN KEY (Partido_Id) REFERENCES partidos (Partido_Id) ON DELETE CASCADE,
										FOREIGN KEY (Usuario) REFERENCES usuarios (Usuario) ON DELETE CASCADE);