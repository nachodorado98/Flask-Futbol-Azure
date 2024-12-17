import pytest
import pandas as pd
from unittest.mock import patch

from src.etls import ETL_Equipos_Liga, ETL_Detalle_Equipo, ETL_Escudo_Equipo, ETL_Entrenador_Equipo
from src.etls import ETL_Estadio_Equipo, ETL_Partidos_Equipo, ETL_Partido_Estadio, ETL_Competicion
from src.etls import ETL_Campeones_Competicion, ETL_Partido_Competicion, ETL_Jugadores_Equipo
from src.etls import ETL_Jugador, ETL_Partido_Goleadores, ETL_Estadio, ETL_Proximos_Partidos_Equipo

from src.scrapers.excepciones_scrapers import EquiposLigaError, EquipoError, EquipoEscudoError
from src.scrapers.excepciones_scrapers import EquipoEntrenadorError, EquipoEstadioError, PartidosEquipoError
from src.scrapers.excepciones_scrapers import PartidoEstadioError, CompeticionError, CompeticionCampeonesError
from src.scrapers.excepciones_scrapers import PartidoCompeticionError, JugadoresEquipoError, JugadorError
from src.scrapers.excepciones_scrapers import PartidoGoleadoresError, EstadioError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa-liga",)]
)
def test_etl_equipos_liga_error(endpoint):

	with pytest.raises(EquiposLigaError):

		ETL_Equipos_Liga(endpoint)

@pytest.mark.parametrize(["endpoint"],
	[("primera/2024",),("segunda/2024",),("/primera/2019",), ("bundesliga/2024",),
	("premier/2024",),("/primera/1996",),("/segunda/1990",)]
)
def test_etl_equipos_liga(conexion, endpoint):

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["endpoint"],
	[("primera/2024",),("segunda/2024",),("/primera/2019",), ("bundesliga/2024",),("premier/2024",),
	("/primera/1996",),("/segunda/1990",)]
)
def test_etl_equipos_liga_equipos_existentes(conexion, endpoint):

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros==numero_registros_nuevos

@pytest.mark.parametrize(["endpoint", "nuevos_equipos"],
	[
		("primera/2024",12),
		("segunda/2024",4),
		("/primera/2019",2),
		("bundesliga/2024",5),
		("premier/2024",3),
		("/primera/1996",7),
		("/segunda/1990",1)
	]
)
def test_etl_equipos_liga_equipos_nuevos_equipos(conexion, endpoint, nuevos_equipos):

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute(f"""DELETE FROM equipos
							WHERE Equipo_Id IN (SELECT Equipo_Id
												FROM equipos
												ORDER BY RANDOM()
												LIMIT {nuevos_equipos})""")

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros+nuevos_equipos==numero_registros_nuevos

@pytest.mark.parametrize(["temporada1", "temporada2"],
	[
		("primera/2019","primera/2020"),
		("primera/2024","primera/2023"),
		("premier/2014","premier/2015")
	]
)
def test_etl_equipos_liga_equipos_nueva_temporada(conexion, temporada1, temporada2):

	ETL_Equipos_Liga(temporada1)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	ETL_Equipos_Liga(temporada2)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros+3==numero_registros_nuevos

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_detalle_equipo_error(endpoint):

	with pytest.raises(EquipoError):

		ETL_Detalle_Equipo(endpoint)

def test_etl_detalle_equipo_no_existe_error():

	with pytest.raises(Exception):

		ETL_Detalle_Equipo("atletico-madrid")

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("villarreal",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_detalle_equipo_datos_correctos(conexion, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Detalle_Equipo(nombre_equipo)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre_completo"] is not None
	assert datos_actualizados["nombre"] is not None
	assert datos_actualizados["siglas"] is not None
	assert datos_actualizados["pais"] is not None
	assert datos_actualizados["codigo_pais"] is not None
	assert datos_actualizados["ciudad"] is not None
	assert datos_actualizados["competicion"] is not None
	assert datos_actualizados["codigo_competicion"] is not None
	assert datos_actualizados["temporadas"] is not None
	assert datos_actualizados["estadio"] is not None
	assert datos_actualizados["fundacion"] is not None
	assert datos_actualizados["presidente"] is not None
	assert datos_actualizados["presidente_url"] is not None
	assert datos_actualizados["codigo_presidente"] is not None

@pytest.mark.parametrize(["nombre_equipo"],
	[("sporting-gijon",)]
)
def test_etl_detalle_equipo_dato_faltante(conexion, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Detalle_Equipo(nombre_equipo)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre_completo"] is not None
	assert datos_actualizados["nombre"] is not None
	assert datos_actualizados["siglas"] is not None
	assert datos_actualizados["pais"] is not None
	assert datos_actualizados["codigo_pais"] is not None
	#assert datos_actualizados["ciudad"] is None # Antes tenia un dato faltante pero ahora han añadido el dato en la web
	assert datos_actualizados["competicion"] is not None
	assert datos_actualizados["codigo_competicion"] is not None
	assert datos_actualizados["temporadas"] is not None
	assert datos_actualizados["estadio"] is not None
	assert datos_actualizados["fundacion"] is not None
	assert datos_actualizados["presidente"] is not None
	assert datos_actualizados["presidente_url"] is not None
	assert datos_actualizados["codigo_presidente"] is not None

@pytest.mark.parametrize(["nombre_equipo"],
	[("seleccion-santa-amalia",),("kakamega-homeboyz",),("cd-valdehornillo-a-senior",),("malaga",)]
)
def test_etl_detalle_equipo_sin_presidente(conexion, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Detalle_Equipo(nombre_equipo)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["presidente"] is None
	assert datos_actualizados["presidente_url"] is None
	assert datos_actualizados["codigo_presidente"] is None

@pytest.mark.parametrize(["nombre_equipo"],
	[("sheffield-united",),("afc-bournemouth",)]
)
def test_etl_detalle_equipo_sin_codigo_presidente(conexion, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Detalle_Equipo(nombre_equipo)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["presidente"] is not None
	assert datos_actualizados["presidente_url"] is not None
	assert datos_actualizados["codigo_presidente"] is None

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_escudo_equipo_error(endpoint):

	with pytest.raises(EquipoEscudoError):

		ETL_Escudo_Equipo(endpoint)

def test_etl_escudo_equipo_no_existe_error(conexion):

	with pytest.raises(Exception):

		ETL_Escudo_Equipo("atletico-madrid")

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_escudo_equipo_datos_correctos(conexion, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Escudo_Equipo(nombre_equipo)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["escudo"] is not None
	assert datos_actualizados["puntuacion"] is not None

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_entrenador_equipo_error(endpoint):

	with pytest.raises(EquipoEntrenadorError):

		ETL_Entrenador_Equipo(endpoint)

def test_etl_entrenador_equipo_no_existe_error():

	with pytest.raises(Exception):

		ETL_Entrenador_Equipo("atletico-madrid")

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_entrenador_equipo_datos_correctos(conexion, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Entrenador_Equipo(nombre_equipo)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["entrenador"] is not None
	assert datos_actualizados["entrenador_url"] is not None
	assert datos_actualizados["codigo_entrenador"] is not None
	assert datos_actualizados["partidos"] is not None

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_estadio_equipo_error(endpoint):

	with pytest.raises(EquipoEstadioError):

		ETL_Estadio_Equipo(endpoint)

def test_etl_estadio_equipo_no_existe_error():

	with pytest.raises(Exception):

		ETL_Estadio_Equipo("atletico-madrid")

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_estadio_equipo_datos_correctos(conexion, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Estadio_Equipo(nombre_equipo)

	conexion.c.execute("SELECT * FROM estadios")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM equipo_estadio")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_estadio_equipo_estadio_existente(conexion, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Estadio_Equipo(nombre_equipo)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio=len(conexion.c.fetchall())

	ETL_Estadio_Equipo(nombre_equipo)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio_nuevos=len(conexion.c.fetchall())

	assert numero_registros_estadio==numero_registros_estadio_nuevos
	assert numero_registros_equipo_estadio==numero_registros_equipo_estadio_nuevos

def test_etl_estadio_equipo_estadio_nuevo(conexion):

	conexion.insertarEquipo("atletico-madrid")

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarEquipoEstadio(("atletico-madrid", "vicente-calderon"))

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio=len(conexion.c.fetchall())

	ETL_Estadio_Equipo("atletico-madrid")

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevo=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio_nuevo=len(conexion.c.fetchall())

	assert numero_registros_estadio_nuevo==numero_registros_estadio+1
	assert numero_registros_equipo_estadio_nuevo==numero_registros_equipo_estadio+1

@pytest.mark.parametrize(["equipo1", "equipo2"],
	[
		("flamengo-rio-janeiro", "fluminense-rio-janeiro"),
		("milan", "internazionale"),
		("roma", "lazio")
	]
)
def test_etl_estadio_equipo_estadio_compartido(conexion, equipo1, equipo2):

	conexion.insertarEquipo(equipo1)

	ETL_Estadio_Equipo(equipo1)

	conexion.insertarEquipo(equipo2)

	ETL_Estadio_Equipo(equipo2)

	conexion.c.execute("SELECT * FROM estadios")

	assert len(conexion.c.fetchall())==1

	conexion.c.execute("SELECT * FROM equipo_estadio")

	assert len(conexion.c.fetchall())==2

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_etl_partidos_equipo_error(equipo_id, temporada):

	with pytest.raises(PartidosEquipoError):

		ETL_Partidos_Equipo(equipo_id, temporada)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_partidos_equipo(conexion, equipo_id, temporada):

	ETL_Partidos_Equipo(equipo_id, temporada)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_partidos_equipo_todo_existente(conexion, equipo_id, temporada):

	ETL_Partidos_Equipo(equipo_id, temporada)

	conexion.c.execute("SELECT * FROM equipos")

	equipos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	partidos=conexion.c.fetchall()

	ETL_Partidos_Equipo(equipo_id, temporada)

	conexion.c.execute("SELECT * FROM equipos")

	equipos_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	partidos_nuevos=conexion.c.fetchall()

	assert len(equipos)==len(equipos_nuevos)
	assert len(partidos)==len(partidos_nuevos)

@pytest.mark.parametrize(["equipo_id", "temporada", "nuevos_partidos"],
	[
		(369, 2021, 1),
		(369, 2014, 4),
		(4, 2020, 3),
		(449, 2017, 20),
		(429, 1990, 11),
		(369, 2000, 2),
		(369, 1940, 1),
		(449, 1971, 7),
		(2115, 2024, 22)
	]
)
def test_etl_partidos_equipo_partidos_nuevos(conexion, equipo_id, temporada, nuevos_partidos):

	ETL_Partidos_Equipo(equipo_id, temporada)

	conexion.c.execute(f"""DELETE FROM partidos
							WHERE Partido_Id IN (SELECT Partido_Id
												FROM partidos
												ORDER BY RANDOM()
												LIMIT {nuevos_partidos})""")

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM partidos")

	partidos=conexion.c.fetchall()

	ETL_Partidos_Equipo(equipo_id, temporada)

	equipos_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	partidos_nuevos=conexion.c.fetchall()

	assert len(partidos_nuevos)==len(partidos)+nuevos_partidos

def test_etl_partido_estadio_error():

	with pytest.raises(PartidoEstadioError):

		ETL_Partido_Estadio("equipo1", "equipo2", "partido_id")

def test_etl_partido_estadio_no_existe_error():

	with pytest.raises(PartidoEstadioError):

		ETL_Partido_Estadio("numancia", "atletico-madrid", "2024489479")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_etl_partido_estadio_datos_correctos(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Estadio(local, visitante, partido_id)

	conexion.c.execute("SELECT * FROM estadios")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_estadio")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_etl_partido_estadio_estadio_existente(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Estadio(local, visitante, partido_id)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_estadio")

	numero_registros_partido_estadio=conexion.c.fetchall()

	ETL_Partido_Estadio(local, visitante, partido_id)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_estadio")

	numero_registros_partido_estadio_nuevos=conexion.c.fetchall()

	assert numero_registros_estadio==numero_registros_estadio_nuevos
	assert numero_registros_partido_estadio==numero_registros_partido_estadio_nuevos

@pytest.mark.parametrize(["local", "visitante", "partido_id_ida", "partido_id_vuelta"],
	[
		("milan", "internazionale", "2024103419", "202524914"),
		("roma", "lazio", "2024103401", "2024662727")
	]
)
def test_etl_partido_estadio_estadio_compartido(conexion, local, visitante, partido_id_ida, partido_id_vuelta):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id_ida, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Estadio(local, visitante, partido_id_ida)

	partido=[partido_id_vuelta, visitante, local, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Estadio(visitante, local, partido_id_vuelta)

	conexion.c.execute("SELECT * FROM estadios")

	assert len(conexion.c.fetchall())==1

	conexion.c.execute("SELECT * FROM partido_estadio")

	assert len(conexion.c.fetchall())==2

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_competicion_error(endpoint):

	with pytest.raises(CompeticionError):

		ETL_Competicion(endpoint)

def test_etl_competicion_no_existe_error():

	with pytest.raises(Exception):

		ETL_Competicion("primera")

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",)]
)
def test_etl_competicion_datos_correctos(conexion, competicion):

	conexion.insertarCompeticion(competicion)

	ETL_Competicion(competicion)

	conexion.c.execute(f"SELECT * FROM competiciones WHERE Competicion_Id='{competicion}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert datos_actualizados["codigo_logo"] is not None
	assert datos_actualizados["codigo_pais"] is not None

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_competicion_campeones_error(endpoint):

	with pytest.raises(CompeticionCampeonesError):

		ETL_Campeones_Competicion(endpoint)

def test_etl_competicion_campeones_no_existe_error():

	with pytest.raises(Exception):

		ETL_Campeones_Competicion("primera")

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_etl_competicion_campeones_datos_correctos(conexion, competicion):

	conexion.insertarCompeticion(competicion)

	ETL_Campeones_Competicion(competicion)

	conexion.c.execute(f"SELECT * FROM competiciones_campeones")

	assert conexion.c.fetchone()

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_etl_competicion_campeones_existentes(conexion, competicion):

	conexion.insertarCompeticion(competicion)

	ETL_Campeones_Competicion(competicion)

	conexion.c.execute(f"SELECT * FROM competiciones_campeones")

	numero_registros=len(conexion.c.fetchone())

	ETL_Campeones_Competicion(competicion)

	conexion.c.execute(f"SELECT * FROM competiciones_campeones")

	numero_registros_nuevos=len(conexion.c.fetchone())

	assert numero_registros==numero_registros_nuevos

def test_etl_partido_competicion_error():

	with pytest.raises(PartidoCompeticionError):

		ETL_Partido_Competicion("equipo1", "equipo2", "partido_id")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_etl_partido_competicion_datos_correctos(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Competicion(local, visitante, partido_id)

	conexion.c.execute("SELECT * FROM competiciones")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_competicion")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_etl_partido_competicion_existente(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Competicion(local, visitante, partido_id)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_competicion")

	numero_registros_partido_competicion=len(conexion.c.fetchall())

	ETL_Partido_Competicion(local, visitante, partido_id)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_competicion")

	numero_registros_partido_competicion_nuevos=len(conexion.c.fetchall())

	assert numero_registros_competiciones==numero_registros_competiciones_nuevos
	assert numero_registros_partido_competicion==numero_registros_partido_competicion_nuevos

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_etl_jugadores_equipo_error(equipo_id, temporada):

	with pytest.raises(JugadoresEquipoError):

		ETL_Jugadores_Equipo(equipo_id, temporada)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_jugadores_equipo(conexion, equipo_id, temporada):

	ETL_Jugadores_Equipo(equipo_id, temporada)

	conexion.c.execute("SELECT * FROM jugadores")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_jugadores_equipo_existentes(conexion, equipo_id, temporada):

	ETL_Jugadores_Equipo(equipo_id, temporada)

	conexion.c.execute("SELECT * FROM jugadores")

	jugadores=conexion.c.fetchall()

	ETL_Jugadores_Equipo(equipo_id, temporada)

	conexion.c.execute("SELECT * FROM jugadores")

	jugadores_nuevos=conexion.c.fetchall()

	assert len(jugadores)==len(jugadores_nuevos)

@pytest.mark.parametrize(["equipo_id", "temporada", "nuevos_jugadores"],
	[
		(369, 2021, 1),
		(369, 2014, 4),
		(4, 2020, 3),
		(449, 2017, 20),
		(429, 1990, 11),
		(369, 2000, 2),
		(369, 1940, 1),
		(449, 1971, 7),
		(2115, 2024, 22)
	]
)
def test_etl_jugadores_equipo_jugadores_nuevos(conexion, equipo_id, temporada, nuevos_jugadores):

	ETL_Jugadores_Equipo(equipo_id, temporada)

	conexion.c.execute(f"""DELETE FROM jugadores
							WHERE Jugador_Id IN (SELECT Jugador_Id
												FROM jugadores
												ORDER BY RANDOM()
												LIMIT {nuevos_jugadores})""")

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM jugadores")

	jugadores=conexion.c.fetchall()

	ETL_Jugadores_Equipo(equipo_id, temporada)

	conexion.c.execute("SELECT * FROM jugadores")

	jugadores_nuevos=conexion.c.fetchall()

	assert len(jugadores_nuevos)==len(jugadores)+nuevos_jugadores

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_jugador_error(endpoint):

	with pytest.raises(JugadorError):

		ETL_Jugador(endpoint)

def test_etl_jugador_no_existe_error():

	with pytest.raises(Exception):

		ETL_Jugador("j-alvarez-772644")

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("c-gallagher-367792",),("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_etl_jugador_datos_correctos_con_equipo(conexion, jugador):

	conexion.insertarJugador(jugador)

	ETL_Jugador(jugador)

	conexion.c.execute(f"SELECT * FROM jugadores WHERE Jugador_Id='{jugador}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert datos_actualizados["equipo_id"] is not None
	assert datos_actualizados["codigo_pais"] is not None
	assert datos_actualizados["codigo_jugador"] is not None
	assert datos_actualizados["puntuacion"] is not None
	assert datos_actualizados["valor"] is not None
	assert datos_actualizados["dorsal"] is not None
	assert datos_actualizados["posicion"] is not None

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["jugador"],
	[("f-torres-29366",),("d-villa-23386",),("f-beckenbauer-321969",)]
)
def test_etl_jugador_datos_correctos_sin_equipo(conexion, jugador):

	conexion.insertarJugador(jugador)

	ETL_Jugador(jugador)

	conexion.c.execute(f"SELECT * FROM jugadores WHERE Jugador_Id='{jugador}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert not datos_actualizados["equipo_id"]
	assert datos_actualizados["codigo_pais"] is not None
	assert datos_actualizados["codigo_jugador"] is not None
	assert datos_actualizados["puntuacion"] is not None
	assert not datos_actualizados["valor"]
	assert not datos_actualizados["dorsal"]
	assert datos_actualizados["posicion"] is not None

	conexion.c.execute("SELECT * FROM equipos")

	assert not conexion.c.fetchall()

def test_etl_partido_goleadores_error():

	with pytest.raises(PartidoGoleadoresError):

		ETL_Partido_Goleadores("equipo1", "equipo2", "partido_id")

def test_etl_partido_goleadores_error_no_existe():

	with pytest.raises(PartidoGoleadoresError):

		ETL_Partido_Goleadores("atletico-madrid", "alianza-lima", "201313927")

def test_etl_partido_goleadores_error_no_hay():

	with pytest.raises(PartidoGoleadoresError):

		ETL_Partido_Goleadores("betis", "atletico-madrid", "202430028")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_etl_partido_goleadores_datos_correctos(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Goleadores(local, visitante, partido_id)

	conexion.c.execute("SELECT * FROM jugadores")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_goleador")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_etl_partido_goleadores_existentes(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Goleadores(local, visitante, partido_id)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_jugadores=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_goleador")

	numero_registros_goleadores=len(conexion.c.fetchall())

	ETL_Partido_Goleadores(local, visitante, partido_id)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_jugadores_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_goleador")

	numero_registros_goleadores_nuevos=len(conexion.c.fetchall())

	assert numero_registros_jugadores==numero_registros_jugadores_nuevos
	assert numero_registros_goleadores==numero_registros_goleadores_nuevos

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_estadio_error(endpoint):

	with pytest.raises(EstadioError):

		ETL_Estadio(endpoint)

def test_etl_estadio_no_existe_error():

	with pytest.raises(Exception):

		ETL_Estadio("riyadh-air-metropolitano-23")

@pytest.mark.parametrize(["estadio_id"],
	[("riyadh-air-metropolitano-23",),("municipal-football-santa-amalia-4902",),("celtic-park-82",),("stadion-feijenoord-71",)]
)
def test_etl_estadio_datos_correctos(conexion, estadio_id):

	estadio=[estadio_id, 1, "Metropolitano", "Metropo", 40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	ETL_Estadio(estadio_id)

	conexion.c.execute(f"SELECT * FROM estadios WHERE Estadio_Id='{estadio_id}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["pais"] is not None
	assert datos_actualizados["codigo_pais"] is not None

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_etl_proximos_partidos_equipo_error(equipo_id, temporada):

	with pytest.raises(PartidosEquipoError):

		ETL_Proximos_Partidos_Equipo(equipo_id, temporada)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_proximos_partidos_equipo_no_hay(conexion, equipo_id, temporada):

	with pytest.raises(Exception):	

		ETL_Proximos_Partidos_Equipo(equipo_id, temporada)

def test_etl_proximos_partidos_equipo(conexion):

	mock_data=pd.DataFrame({"Partido_Id": ["match-2025225057", "match-20256430"],
							"Link": ["https://es.besoccer.com/partido/cacereno/atletico-madrid/2025225057",
									"https://es.besoccer.com/partido/atletico-madrid/sevilla/20256430"],
							"Estado": [-1, -1],
							"Fecha_Inicio": ["2024-12-05T19:00:00+01:00", "2024-12-08T21:00:00+01:00"],
							"Competicion": ["Copa del Rey", "Primera División"],
							"Local": ["CP Cacereño", "Atlético"],
							"Visitante": ["Atlético", "Sevilla"],
							"Marcador": ["19:00", "21:00"],
							"Fecha_Str": ["05 DIC", "08 DIC"]})
   
	with patch("src.etl_proximos_partidos.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert conexion.c.fetchall()

def test_etl_proximos_partidos_equipo_todo_existente(conexion):

	mock_data=pd.DataFrame({"Partido_Id": ["match-2025225057", "match-20256430"],
							"Link": ["https://es.besoccer.com/partido/cacereno/atletico-madrid/2025225057",
									"https://es.besoccer.com/partido/atletico-madrid/sevilla/20256430"],
							"Estado": [-1, -1],
							"Fecha_Inicio": ["2024-12-05T19:00:00+01:00", "2024-12-08T21:00:00+01:00"],
							"Competicion": ["Copa del Rey", "Primera División"],
							"Local": ["CP Cacereño", "Atlético"],
							"Visitante": ["Atlético", "Sevilla"],
							"Marcador": ["19:00", "21:00"],
							"Fecha_Str": ["05 DIC", "08 DIC"]})
   
	with patch("src.etl_proximos_partidos.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025)

	conexion.c.execute("SELECT * FROM equipos")

	equipos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos=conexion.c.fetchall()

	with patch("src.etl_proximos_partidos.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025)

	conexion.c.execute("SELECT * FROM equipos")

	equipos_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos_nuevos=conexion.c.fetchall()

	assert len(equipos)==len(equipos_nuevos)
	assert len(proximos_partidos)==len(proximos_partidos_nuevos)

def test_etl_proximos_partidos_equipo_partido_nuevo(conexion):

	mock_data=pd.DataFrame({"Partido_Id": ["match-2025225057", "match-20256430"],
							"Link": ["https://es.besoccer.com/partido/cacereno/atletico-madrid/2025225057",
									"https://es.besoccer.com/partido/atletico-madrid/sevilla/20256430"],
							"Estado": [-1, -1],
							"Fecha_Inicio": ["2024-12-05T19:00:00+01:00", "2024-12-08T21:00:00+01:00"],
							"Competicion": ["Copa del Rey", "Primera División"],
							"Local": ["CP Cacereño", "Atlético"],
							"Visitante": ["Atlético", "Sevilla"],
							"Marcador": ["19:00", "21:00"],
							"Fecha_Str": ["05 DIC", "08 DIC"]})
   
	with patch("src.etl_proximos_partidos.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025)

	conexion.c.execute("""DELETE FROM proximos_partidos
						WHERE Partido_Id IN (SELECT Partido_Id
										    FROM proximos_partidos
										    ORDER BY RANDOM()
										    LIMIT 1)""")

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos=conexion.c.fetchall()

	with patch("src.etl_proximos_partidos.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025)

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos_nuevos=conexion.c.fetchall()

	assert len(proximos_partidos_nuevos)==len(proximos_partidos)+1