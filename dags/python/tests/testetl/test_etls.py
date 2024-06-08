import pytest
import pandas as pd

from src.etls import ETL_Equipos_Liga, ETL_Detalle_Equipo
from src.scrapers.excepciones_scrapers import EquiposLigaError, EquipoError

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