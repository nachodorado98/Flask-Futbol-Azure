import pytest
import pandas as pd
from unittest.mock import patch

from src.etls import ETL_Equipos_Liga, ETL_Detalle_Equipo, ETL_Escudo_Equipo, ETL_Entrenador_Equipo
from src.etls import ETL_Estadio_Equipo, ETL_Partidos_Equipo, ETL_Partido_Estadio, ETL_Competicion
from src.etls import ETL_Campeones_Competicion, ETL_Partido_Competicion, ETL_Jugadores_Equipo
from src.etls import ETL_Jugador, ETL_Partido_Goleadores, ETL_Estadio, ETL_Proximos_Partidos_Equipo
from src.etls import ETL_Entrenador, ETL_Jugador_Equipos, ETL_Jugador_Seleccion, ETL_Palmares_Equipo
from src.etls import ETL_Entrenador_Equipos, ETL_Palmares_Entrenador

from src.scrapers.excepciones_scrapers import EquiposLigaError, EquipoError, EquipoEscudoError
from src.scrapers.excepciones_scrapers import EquipoEntrenadorError, EquipoEstadioError, PartidosEquipoError
from src.scrapers.excepciones_scrapers import PartidoEstadioError, CompeticionError, CompeticionCampeonesError
from src.scrapers.excepciones_scrapers import PartidoCompeticionError, JugadoresEquipoError, JugadorError
from src.scrapers.excepciones_scrapers import PartidoGoleadoresError, EstadioError, EntrenadorError
from src.scrapers.excepciones_scrapers import JugadorEquiposError, JugadorSeleccionError, EquipoPalmaresError
from src.scrapers.excepciones_scrapers import EntrenadorEquiposError, EntrenadorPalmaresError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa-liga",)]
)
def test_etl_equipos_liga_error(entorno, endpoint):

	with pytest.raises(EquiposLigaError):

		ETL_Equipos_Liga(endpoint, entorno)

@pytest.mark.parametrize(["endpoint"],
	[("primera/2024",),("segunda/2024",),("/primera/2019",), ("bundesliga/2024",),
	("premier/2024",),("/primera/1996",),("/segunda/1990",)]
)
def test_etl_equipos_liga(conexion, entorno, endpoint):

	ETL_Equipos_Liga(endpoint, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["endpoint"],
	[("primera/2024",),("segunda/2024",),("/primera/2019",), ("bundesliga/2024",),("premier/2024",),
	("/primera/1996",),("/segunda/1990",)]
)
def test_etl_equipos_liga_equipos_existentes(conexion, entorno, endpoint):

	ETL_Equipos_Liga(endpoint, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	ETL_Equipos_Liga(endpoint, entorno)

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
def test_etl_equipos_liga_equipos_nuevos_equipos(conexion, entorno, endpoint, nuevos_equipos):

	ETL_Equipos_Liga(endpoint, entorno)

	conexion.c.execute(f"""DELETE FROM equipos
							WHERE Equipo_Id IN (SELECT Equipo_Id
												FROM equipos
												ORDER BY RANDOM()
												LIMIT {nuevos_equipos})""")

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	ETL_Equipos_Liga(endpoint, entorno)

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
def test_etl_equipos_liga_equipos_nueva_temporada(conexion, entorno, temporada1, temporada2):

	ETL_Equipos_Liga(temporada1, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	ETL_Equipos_Liga(temporada2, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros+3==numero_registros_nuevos

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_detalle_equipo_error(entorno, endpoint):

	with pytest.raises(EquipoError):

		ETL_Detalle_Equipo(endpoint, entorno)

def test_etl_detalle_equipo_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Detalle_Equipo("atletico-madrid", entorno)

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("villarreal",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_detalle_equipo_datos_correctos(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Detalle_Equipo(nombre_equipo, entorno)

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
def test_etl_detalle_equipo_dato_faltante(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Detalle_Equipo(nombre_equipo, entorno)

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
def test_etl_detalle_equipo_sin_presidente(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Detalle_Equipo(nombre_equipo, entorno)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["presidente"] is None
	assert datos_actualizados["presidente_url"] is None
	assert datos_actualizados["codigo_presidente"] is None

@pytest.mark.parametrize(["nombre_equipo"],
	[("sheffield-united",),("afc-bournemouth",)]
)
def test_etl_detalle_equipo_sin_codigo_presidente(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Detalle_Equipo(nombre_equipo, entorno)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["presidente"] is not None
	assert datos_actualizados["presidente_url"] is not None
	assert datos_actualizados["codigo_presidente"] is None

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_escudo_equipo_error(entorno, endpoint):

	with pytest.raises(EquipoEscudoError):

		ETL_Escudo_Equipo(endpoint, entorno)

def test_etl_escudo_equipo_no_existe_error(conexion, entorno):

	with pytest.raises(Exception):

		ETL_Escudo_Equipo("atletico-madrid", entorno)

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_escudo_equipo_datos_correctos(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Escudo_Equipo(nombre_equipo, entorno)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["escudo"] is not None
	assert datos_actualizados["puntuacion"] is not None

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_entrenador_equipo_error(entorno, endpoint):

	with pytest.raises(EquipoEntrenadorError):

		ETL_Entrenador_Equipo(endpoint, entorno)

def test_etl_entrenador_equipo_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Entrenador_Equipo("atletico-madrid", entorno)

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_entrenador_equipo_datos_correctos(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Entrenador_Equipo(nombre_equipo, entorno)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["entrenador"] is not None
	assert datos_actualizados["entrenador_url"] is not None
	assert datos_actualizados["codigo_entrenador"] is not None
	assert datos_actualizados["partidos"] is not None

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_estadio_equipo_error(entorno, endpoint):

	with pytest.raises(EquipoEstadioError):

		ETL_Estadio_Equipo(endpoint, entorno)

def test_etl_estadio_equipo_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Estadio_Equipo("atletico-madrid", entorno)

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_estadio_equipo_datos_correctos(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Estadio_Equipo(nombre_equipo, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM equipo_estadio")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_etl_estadio_equipo_estadio_existente(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	ETL_Estadio_Equipo(nombre_equipo, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio=len(conexion.c.fetchall())

	ETL_Estadio_Equipo(nombre_equipo, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio_nuevos=len(conexion.c.fetchall())

	assert numero_registros_estadio==numero_registros_estadio_nuevos
	assert numero_registros_equipo_estadio==numero_registros_equipo_estadio_nuevos

def test_etl_estadio_equipo_estadio_nuevo(conexion, entorno):

	conexion.insertarEquipo("atletico-madrid")

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarEquipoEstadio(("atletico-madrid", "vicente-calderon"))

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio=len(conexion.c.fetchall())

	ETL_Estadio_Equipo("atletico-madrid", entorno)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevo=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio_nuevo=len(conexion.c.fetchall())

	assert numero_registros_estadio_nuevo==numero_registros_estadio+1
	assert numero_registros_equipo_estadio_nuevo==numero_registros_equipo_estadio+1

@pytest.mark.parametrize(["equipo1", "equipo2"],
	[
		("flamengo-rio-janeiro", "fluminense-rio-janeiro"),
		# ("milan", "internazionale"), # Han cambiado el nombre (San Siro y Giussepe Meazza pero realmente es el mismo)
		("roma", "lazio")
	]
)
def test_etl_estadio_equipo_estadio_compartido(conexion, entorno, equipo1, equipo2):

	conexion.insertarEquipo(equipo1)

	ETL_Estadio_Equipo(equipo1, entorno)

	conexion.insertarEquipo(equipo2)

	ETL_Estadio_Equipo(equipo2, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	assert len(conexion.c.fetchall())==1

	conexion.c.execute("SELECT * FROM equipo_estadio")

	assert len(conexion.c.fetchall())==2

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_equipo_palmares_error(entorno, endpoint):

	with pytest.raises(EquipoPalmaresError):

		ETL_Palmares_Equipo(endpoint, entorno)

def test_etl_equipo_palmares_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Palmares_Equipo("atletico-madrid", entorno)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("barcelona",)]
)
def test_etl_equipo_palmares_no_competiciones(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	ETL_Palmares_Equipo(equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert not conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM equipo_titulo")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("barcelona",)]
)
def test_etl_equipo_palmares_no_competicion_logo(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	conexion.insertarCompeticion("primera")

	ETL_Palmares_Equipo(equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	assert not conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM equipo_titulo")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("barcelona",)]
)
def test_etl_equipo_palmares(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	conexion.insertarCompeticion("primera")

	conexion.actualizarDatosCompeticion(["Nombre", "primera-division-ea", "Pais"], "primera")

	ETL_Palmares_Equipo(equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	assert conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM equipo_titulo")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("barcelona",)]
)
def test_etl_equipo_palmares_existente(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	conexion.insertarCompeticion("primera")

	conexion.actualizarDatosCompeticion(["Nombre", "primera-division-ea", "Pais"], "primera")

	ETL_Palmares_Equipo(equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones=conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	codigo_titulo=conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM equipo_titulo")

	numero_registros_equipo_titulo=conexion.c.fetchall()

	ETL_Palmares_Equipo(equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	codigo_titulo_nuevo=conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM equipo_titulo")

	numero_registros_equipo_titulo_nuevos=conexion.c.fetchall()

	assert numero_registros_competiciones==numero_registros_competiciones_nuevos
	assert codigo_titulo==codigo_titulo_nuevo
	assert numero_registros_equipo_titulo==numero_registros_equipo_titulo_nuevos

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_etl_partidos_equipo_error(entorno, equipo_id, temporada):

	with pytest.raises(PartidosEquipoError):

		ETL_Partidos_Equipo(equipo_id, temporada, entorno)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_partidos_equipo(conexion, entorno, equipo_id, temporada):

	ETL_Partidos_Equipo(equipo_id, temporada, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_partidos_equipo_todo_existente(conexion, entorno, equipo_id, temporada):

	ETL_Partidos_Equipo(equipo_id, temporada, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	equipos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	partidos=conexion.c.fetchall()

	ETL_Partidos_Equipo(equipo_id, temporada, entorno)

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
def test_etl_partidos_equipo_partidos_nuevos(conexion, entorno, equipo_id, temporada, nuevos_partidos):

	ETL_Partidos_Equipo(equipo_id, temporada, entorno)

	conexion.c.execute(f"""DELETE FROM partidos
							WHERE Partido_Id IN (SELECT Partido_Id
												FROM partidos
												ORDER BY RANDOM()
												LIMIT {nuevos_partidos})""")

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM partidos")

	partidos=conexion.c.fetchall()

	ETL_Partidos_Equipo(equipo_id, temporada, entorno)

	equipos_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	partidos_nuevos=conexion.c.fetchall()

	assert len(partidos_nuevos)==len(partidos)+nuevos_partidos

def test_etl_partido_estadio_error(entorno):

	with pytest.raises(PartidoEstadioError):

		ETL_Partido_Estadio("equipo1", "equipo2", "partido_id", entorno)

def test_etl_partido_estadio_no_existe_error(entorno):

	with pytest.raises(PartidoEstadioError):

		ETL_Partido_Estadio("numancia", "atletico-madrid", "2024489479", entorno)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_etl_partido_estadio_datos_correctos(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Estadio(local, visitante, partido_id, entorno)

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
def test_etl_partido_estadio_estadio_existente(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Estadio(local, visitante, partido_id, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_estadio")

	numero_registros_partido_estadio=conexion.c.fetchall()

	ETL_Partido_Estadio(local, visitante, partido_id, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_estadio")

	numero_registros_partido_estadio_nuevos=conexion.c.fetchall()

	assert numero_registros_estadio==numero_registros_estadio_nuevos
	assert numero_registros_partido_estadio==numero_registros_partido_estadio_nuevos

@pytest.mark.parametrize(["local", "visitante", "partido_id_ida", "partido_id_vuelta"],
	[
		# ("milan", "internazionale", "2024103419", "202524914"), # Han cambiado el nombre (San Siro y Giussepe Meazza pero realmente es el mismo)
		("flamengo-rio-janeiro", "fluminense-rio-janeiro", "2024706960", "2024706771"),
		("roma", "lazio", "2024103401", "2024662727")
	]
)
def test_etl_partido_estadio_estadio_compartido(conexion, entorno, local, visitante, partido_id_ida, partido_id_vuelta):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id_ida, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Estadio(local, visitante, partido_id_ida, entorno)

	partido=[partido_id_vuelta, visitante, local, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Estadio(visitante, local, partido_id_vuelta, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	assert len(conexion.c.fetchall())==1

	conexion.c.execute("SELECT * FROM partido_estadio")

	assert len(conexion.c.fetchall())==2

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_competicion_error(entorno, endpoint):

	with pytest.raises(CompeticionError):

		ETL_Competicion(endpoint, entorno)

def test_etl_competicion_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Competicion("primera", entorno)

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",)]
)
def test_etl_competicion_datos_correctos(conexion, entorno, competicion):

	conexion.insertarCompeticion(competicion)

	ETL_Competicion(competicion, entorno)

	conexion.c.execute(f"SELECT * FROM competiciones WHERE Competicion_Id='{competicion}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert datos_actualizados["codigo_logo"] is not None
	assert datos_actualizados["codigo_pais"] is not None

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_competicion_campeones_error(entorno, endpoint):

	with pytest.raises(CompeticionCampeonesError):

		ETL_Campeones_Competicion(endpoint, entorno)

def test_etl_competicion_campeones_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Campeones_Competicion("primera", entorno)

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_etl_competicion_campeones_datos_correctos(conexion, entorno, competicion):

	conexion.insertarCompeticion(competicion)

	ETL_Campeones_Competicion(competicion, entorno)

	conexion.c.execute(f"SELECT * FROM competiciones_campeones")

	assert conexion.c.fetchone()

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_etl_competicion_campeones_existentes(conexion, entorno, competicion):

	conexion.insertarCompeticion(competicion)

	ETL_Campeones_Competicion(competicion, entorno)

	conexion.c.execute(f"SELECT * FROM competiciones_campeones")

	numero_registros=len(conexion.c.fetchone())

	ETL_Campeones_Competicion(competicion, entorno)

	conexion.c.execute(f"SELECT * FROM competiciones_campeones")

	numero_registros_nuevos=len(conexion.c.fetchone())

	assert numero_registros==numero_registros_nuevos

def test_etl_partido_competicion_error(entorno):

	with pytest.raises(PartidoCompeticionError):

		ETL_Partido_Competicion("equipo1", "equipo2", "partido_id", entorno)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_etl_partido_competicion_datos_correctos(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Competicion(local, visitante, partido_id, entorno)

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
def test_etl_partido_competicion_existente(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Competicion(local, visitante, partido_id, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_competicion")

	numero_registros_partido_competicion=len(conexion.c.fetchall())

	ETL_Partido_Competicion(local, visitante, partido_id, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_competicion")

	numero_registros_partido_competicion_nuevos=len(conexion.c.fetchall())

	assert numero_registros_competiciones==numero_registros_competiciones_nuevos
	assert numero_registros_partido_competicion==numero_registros_partido_competicion_nuevos

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_etl_jugadores_equipo_error(entorno, equipo_id, temporada):

	with pytest.raises(JugadoresEquipoError):

		ETL_Jugadores_Equipo(equipo_id, temporada, entorno)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_jugadores_equipo(conexion, entorno, equipo_id, temporada):

	ETL_Jugadores_Equipo(equipo_id, temporada, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_jugadores_equipo_existentes(conexion, entorno, equipo_id, temporada):

	ETL_Jugadores_Equipo(equipo_id, temporada, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	jugadores=conexion.c.fetchall()

	ETL_Jugadores_Equipo(equipo_id, temporada, entorno)

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
def test_etl_jugadores_equipo_jugadores_nuevos(conexion, entorno, equipo_id, temporada, nuevos_jugadores):

	ETL_Jugadores_Equipo(equipo_id, temporada, entorno)

	conexion.c.execute(f"""DELETE FROM jugadores
							WHERE Jugador_Id IN (SELECT Jugador_Id
												FROM jugadores
												ORDER BY RANDOM()
												LIMIT {nuevos_jugadores})""")

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM jugadores")

	jugadores=conexion.c.fetchall()

	ETL_Jugadores_Equipo(equipo_id, temporada, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	jugadores_nuevos=conexion.c.fetchall()

	assert len(jugadores_nuevos)==len(jugadores)+nuevos_jugadores

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_jugador_error(entorno, endpoint):

	with pytest.raises(JugadorError):

		ETL_Jugador(endpoint, entorno)

def test_etl_jugador_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Jugador("j-alvarez-772644", entorno)

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("c-gallagher-367792",),("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_etl_jugador_datos_correctos_con_equipo(conexion, entorno, jugador):

	conexion.insertarJugador(jugador)

	ETL_Jugador(jugador, entorno)

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
def test_etl_jugador_datos_correctos_sin_equipo(conexion, entorno, jugador):

	conexion.insertarJugador(jugador)

	ETL_Jugador(jugador, entorno)

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

def test_etl_partido_goleadores_error(entorno):

	with pytest.raises(PartidoGoleadoresError):

		ETL_Partido_Goleadores("equipo1", "equipo2", "partido_id", entorno)

def test_etl_partido_goleadores_error_no_existe(entorno):

	with pytest.raises(PartidoGoleadoresError):

		ETL_Partido_Goleadores("atletico-madrid", "alianza-lima", "201313927", entorno)

def test_etl_partido_goleadores_error_no_hay(entorno):

	with pytest.raises(PartidoGoleadoresError):

		ETL_Partido_Goleadores("betis", "atletico-madrid", "202430028", entorno)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_etl_partido_goleadores_datos_correctos(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Goleadores(local, visitante, partido_id, entorno)

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
def test_etl_partido_goleadores_existentes(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	ETL_Partido_Goleadores(local, visitante, partido_id, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_jugadores=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_goleador")

	numero_registros_goleadores=len(conexion.c.fetchall())

	ETL_Partido_Goleadores(local, visitante, partido_id, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_jugadores_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_goleador")

	numero_registros_goleadores_nuevos=len(conexion.c.fetchall())

	assert numero_registros_jugadores==numero_registros_jugadores_nuevos
	assert numero_registros_goleadores==numero_registros_goleadores_nuevos

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_estadio_error(entorno, endpoint):

	with pytest.raises(EstadioError):

		ETL_Estadio(endpoint, entorno)

def test_etl_estadio_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Estadio("riyadh-air-metropolitano-23", entorno)

@pytest.mark.parametrize(["estadio_id"],
	[("riyadh-air-metropolitano-23",),("municipal-football-santa-amalia-4902",),("celtic-park-82",),("stadion-feijenoord-71",)]
)
def test_etl_estadio_datos_correctos(conexion, entorno, estadio_id):

	estadio=[estadio_id, 1, "Metropolitano", "Metropo", 40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	ETL_Estadio(estadio_id, entorno)

	conexion.c.execute(f"SELECT * FROM estadios WHERE Estadio_Id='{estadio_id}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["pais"] is not None
	assert datos_actualizados["codigo_pais"] is not None

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_etl_proximos_partidos_equipo_error(entorno, equipo_id, temporada):

	with pytest.raises(PartidosEquipoError):

		ETL_Proximos_Partidos_Equipo(equipo_id, temporada, entorno)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_etl_proximos_partidos_equipo_no_hay(conexion, entorno, equipo_id, temporada):

	with pytest.raises(Exception):	

		ETL_Proximos_Partidos_Equipo(equipo_id, temporada, entorno)

def test_etl_proximos_partidos_equipo(conexion, entorno):

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
   
	with patch("src.etls.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert conexion.c.fetchall()

def test_etl_proximos_partidos_equipo_todo_existente(conexion, entorno):

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
   
	with patch("src.etls.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	equipos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos=conexion.c.fetchall()

	with patch("src.etls.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	equipos_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos_nuevos=conexion.c.fetchall()

	assert len(equipos)==len(equipos_nuevos)
	assert len(proximos_partidos)==len(proximos_partidos_nuevos)

def test_etl_proximos_partidos_equipo_partido_nuevo(conexion, entorno):

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
   
	with patch("src.etls.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025, entorno)

	conexion.c.execute("""DELETE FROM proximos_partidos
						WHERE Partido_Id IN (SELECT Partido_Id
										    FROM proximos_partidos
										    ORDER BY RANDOM()
										    LIMIT 1)""")

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos=conexion.c.fetchall()

	with patch("src.etls.extraerDataProximosPartidosEquipo", return_value=mock_data):

		ETL_Proximos_Partidos_Equipo(369, 2025, entorno)

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos_nuevos=conexion.c.fetchall()

	assert len(proximos_partidos_nuevos)==len(proximos_partidos)+1

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_entrenador_error(entorno, endpoint):

	with pytest.raises(EntrenadorError):

		ETL_Entrenador(endpoint, entorno)

def test_etl_entrenador_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Entrenador("diego-simeone-13", entorno)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("pep-guardiola-114",),("fernando-torres-47437",)]
)
def test_etl_entrenador_datos_correctos_con_equipo(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	ETL_Entrenador(entrenador, entorno)

	conexion.c.execute(f"SELECT * FROM entrenadores WHERE Entrenador_Id='{entrenador}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert datos_actualizados["equipo_id"] is not None
	assert datos_actualizados["codigo_pais"] is not None
	assert datos_actualizados["codigo_entrenador"] is not None
	assert datos_actualizados["puntuacion"] is not None

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["entrenador"],
	[("luis-aragones-1918",),("radomir-antic-2601",)]
)
def test_etl_entrenador_datos_correctos_sin_equipo(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	ETL_Entrenador(entrenador, entorno)

	conexion.c.execute(f"SELECT * FROM entrenadores WHERE Entrenador_Id='{entrenador}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert not datos_actualizados["equipo_id"]
	assert datos_actualizados["codigo_pais"] is not None
	assert datos_actualizados["codigo_entrenador"] is not None
	assert datos_actualizados["puntuacion"] is not None

	conexion.c.execute("SELECT * FROM equipos")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_jugador_equipos_error(entorno, endpoint):

	with pytest.raises(JugadorEquiposError):

		ETL_Jugador_Equipos(endpoint, entorno)

def test_etl_jugador_equipos_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Jugador_Equipos("j-alvarez-772644", entorno)

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_etl_jugador_equipos(conexion, entorno, jugador):

	conexion.insertarJugador(jugador)

	ETL_Jugador_Equipos(jugador, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM jugadores_equipo")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_etl_jugador_equipos_existentes(conexion, entorno, jugador):

	conexion.insertarJugador(jugador)

	ETL_Jugador_Equipos(jugador, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_equipos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM jugadores_equipo")

	numero_registros_equipos_jugador=len(conexion.c.fetchall())

	ETL_Jugador_Equipos(jugador, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_equipos_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM jugadores_equipo")

	numero_registros_equipos_jugador_nuevos=len(conexion.c.fetchall())

	assert numero_registros_equipos==numero_registros_equipos_nuevos
	assert numero_registros_equipos_jugador==numero_registros_equipos_jugador_nuevos

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_jugador_seleccion_error(entorno, endpoint):

	with pytest.raises(JugadorSeleccionError):

		ETL_Jugador_Seleccion(endpoint, entorno)

def test_etl_jugador_seleccion_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Jugador_Seleccion("j-alvarez-772644", entorno)

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_etl_jugador_seleccion(conexion, entorno, jugador):

	conexion.insertarJugador(jugador)

	ETL_Jugador_Seleccion(jugador, entorno)

	conexion.c.execute("SELECT * FROM jugadores_seleccion")

	assert len(conexion.c.fetchall())==1

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_etl_jugador_seleccion_existentes(conexion, entorno, jugador):

	conexion.insertarJugador(jugador)

	ETL_Jugador_Seleccion(jugador, entorno)

	conexion.c.execute("SELECT * FROM jugadores_seleccion")

	numero_registros_seleccion_jugador=len(conexion.c.fetchall())

	ETL_Jugador_Seleccion(jugador, entorno)

	conexion.c.execute("SELECT * FROM jugadores_seleccion")

	numero_registros_seleccion_jugador_nuevos=len(conexion.c.fetchall())

	assert numero_registros_seleccion_jugador==numero_registros_seleccion_jugador_nuevos

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("premier-league",)]
)
def test_etl_entrenador_equipos_error(entorno, endpoint):

	with pytest.raises(EntrenadorEquiposError):

		ETL_Entrenador_Equipos(endpoint, entorno)

def test_etl_entrenador_equipos_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Entrenador_Equipos("diego-simeone-13", entorno)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_etl_entrenador_equipos(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	ETL_Entrenador_Equipos(entrenador, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM entrenadores_equipo")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_etl_entrenador_equipos_existentes(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	ETL_Entrenador_Equipos(entrenador, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_equipos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM entrenadores_equipo")

	numero_registros_equipos_entrenador=len(conexion.c.fetchall())

	ETL_Entrenador_Equipos(entrenador, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_equipos_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM entrenadores_equipo")

	numero_registros_equipos_entrenador_nuevos=len(conexion.c.fetchall())

	assert numero_registros_equipos==numero_registros_equipos_nuevos
	assert numero_registros_equipos_entrenador==numero_registros_equipos_entrenador_nuevos

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_entrenador_palmares_error(entorno, endpoint):

	with pytest.raises(EntrenadorPalmaresError):

		ETL_Palmares_Entrenador(endpoint, entorno)

def test_etl_entrenador_palmares_no_existe_error(entorno):

	with pytest.raises(Exception):

		ETL_Palmares_Entrenador("diego-simeone-13", entorno)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",)]
)
def test_etl_entrenador_palmares_no_competiciones(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	ETL_Palmares_Entrenador(entrenador, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert not conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",)]
)
def test_etl_entrenador_palmares(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	conexion.insertarCompeticion("primera")

	ETL_Palmares_Entrenador(entrenador, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	assert conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",)]
)
def test_etl_entrenador_palmares_existente(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	conexion.insertarCompeticion("primera")

	ETL_Palmares_Entrenador(entrenador, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones=conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	codigo_titulo=conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	numero_registros_entrenador_titulo=conexion.c.fetchall()

	ETL_Palmares_Entrenador(entrenador, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	codigo_titulo_nuevo=conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	numero_registros_entrenador_titulo_nuevos=conexion.c.fetchall()

	assert numero_registros_competiciones==numero_registros_competiciones_nuevos
	assert codigo_titulo==codigo_titulo_nuevo
	assert numero_registros_entrenador_titulo==numero_registros_entrenador_titulo_nuevos