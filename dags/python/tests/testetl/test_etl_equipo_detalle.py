import pytest
import pandas as pd

from src.etl_equipo import extraerDataEquipoDetalle, limpiarDataEquipoDetalle, cargarDataEquipoDetalle
from src.scrapers.excepciones_scrapers import EquipoError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_detalle_error_endpoint(endpoint):

	with pytest.raises(EquipoError):

		extraerDataEquipoDetalle(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),
	("kakamega-homeboyz",),("sporting-gijon",),("albacete",),
	("racing",),("atalanta",),("malaga",),("hull-city",)]
)
def test_extraer_data_equipo_detalle(equipo):

	data=extraerDataEquipoDetalle(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),
	("kakamega-homeboyz",),("sporting-gijon",),("albacete",),
	("racing",),("atalanta",),("malaga",),("hull-city",)]
)
def test_limpiar_data_equipo(equipo):

	data=extraerDataEquipoDetalle(equipo)

	data_limpia=limpiarDataEquipoDetalle(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==14
	assert len(data_limpia)==1

def test_cargar_data_equipo_error_no_existe(conexion, entorno):

	data=extraerDataEquipoDetalle("atletico-madrid")

	data_limpia=limpiarDataEquipoDetalle(data)

	with pytest.raises(Exception):

		cargarDataEquipoDetalle(data_limpia, "atletico-madrid", entorno)

def test_cargar_data_equipo_datos_error(conexion, entorno):

	conexion.insertarEquipo("atletico-madrid")

	data=extraerDataEquipoDetalle("atletico-madrid")

	data_limpia=limpiarDataEquipoDetalle(data)

	data_limpia["Fundacion"]="numero"

	with pytest.raises(Exception):

		cargarDataEquipoDetalle(data_limpia, "atletico-madrid", entorno)

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("villarreal",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_cargar_data_equipo_datos_correctos(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	data=extraerDataEquipoDetalle(nombre_equipo)

	data_limpia=limpiarDataEquipoDetalle(data)

	cargarDataEquipoDetalle(data_limpia, nombre_equipo, entorno)

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
def test_cargar_data_equipo_dato_faltante(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	data=extraerDataEquipoDetalle(nombre_equipo)

	data_limpia=limpiarDataEquipoDetalle(data)

	cargarDataEquipoDetalle(data_limpia, nombre_equipo, entorno)

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
def test_cargar_data_equipo_sin_presidente(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	data=extraerDataEquipoDetalle(nombre_equipo)

	data_limpia=limpiarDataEquipoDetalle(data)

	cargarDataEquipoDetalle(data_limpia, nombre_equipo, entorno)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["presidente"] is None
	assert datos_actualizados["presidente_url"] is None
	assert datos_actualizados["codigo_presidente"] is None

@pytest.mark.parametrize(["nombre_equipo"],
	[("sheffield-united",),("afc-bournemouth",)]
)
def test_cargar_data_equipo_sin_codigo_presidente(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	data=extraerDataEquipoDetalle(nombre_equipo)

	data_limpia=limpiarDataEquipoDetalle(data)

	cargarDataEquipoDetalle(data_limpia, nombre_equipo, entorno)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["presidente"] is not None
	assert datos_actualizados["presidente_url"] is not None
	assert datos_actualizados["codigo_presidente"] is None