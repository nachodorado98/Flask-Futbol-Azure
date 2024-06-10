import pytest
import pandas as pd

from src.etls import ETL_Equipos_Liga, ETL_Detalle_Equipo, ETL_Escudo_Equipo, ETL_Entrenador_Equipo
from src.etls import ETL_Estadio_Equipo
from src.scrapers.excepciones_scrapers import EquiposLigaError, EquipoError, EquipoEscudoError
from src.scrapers.excepciones_scrapers import EquipoEntrenadorError, EquipoEstadioError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_equipos_liga_error(endpoint):

	with pytest.raises(EquiposLigaError):

		ETL_Equipos_Liga(endpoint)

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/2019",), ("bundesliga",),
	("premier",),("/primera/1996",),("/segunda/1990",)]
)
def test_etl_equipos_liga(conexion, endpoint):

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/2019",), ("bundesliga",),("premier",),
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
		("primera",12),
		("segunda",4),
		("/primera/2019",2),
		("bundesliga",5),
		("premier",3),
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
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
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
	assert datos_actualizados["ciudad"] is None
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

def test_etl_escudo_equipo_no_existe_error():

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