import pytest
import pandas as pd

from src.etl_equipo_estadio import extraerDataEquipoEstadio, limpiarDataEquipoEstadio, cargarDataEquipoEstadio
from src.scrapers.excepciones_scrapers import EquipoEstadioError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_estadio_error_endpoint(endpoint):

	with pytest.raises(EquipoEstadioError):

		extraerDataEquipoEstadio(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("kakamega-homeboyz",),("cd-valdehornillo-a-senior",)]
)
def test_extraer_data_equipo_estadio_error_no_existe(equipo):

	with pytest.raises(EquipoEstadioError):

		extraerDataEquipoEstadio(equipo)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),("seleccion-santa-amalia",)]
)
def test_extraer_data_equipo_estadio(equipo):

	data=extraerDataEquipoEstadio(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),
	("seleccion-santa-amalia",),("fc-porto",),("malaga",),("racing",),
	("salzburgo",),("manchester-united-fc",),("losc-lille",)]
)
def test_limpiar_data_equipo_estadio(equipo):

	data=extraerDataEquipoEstadio(equipo)

	data_limpia=limpiarDataEquipoEstadio(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==13
	assert len(data_limpia)==1

def test_cargar_data_equipo_estadio_error_no_existe(conexion, entorno):

	data=extraerDataEquipoEstadio("atletico-madrid")

	data_limpia=limpiarDataEquipoEstadio(data)

	with pytest.raises(Exception):

		cargarDataEquipoEstadio(data_limpia, "atletico-madrid", entorno)

def test_cargar_data_equipo_estadio_datos_error(conexion, entorno):

	conexion.insertarEquipo("atletico-madrid")

	data=extraerDataEquipoEstadio("atletico-madrid")

	data_limpia=limpiarDataEquipoEstadio(data)

	data_limpia["Fecha"]="numero"

	with pytest.raises(Exception):

		cargarDataEquipoEstadio(data_limpia, "atletico-madrid", entorno)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),
	("seleccion-santa-amalia",),("fc-porto",),("malaga",),("racing",),
	("salzburgo",),("manchester-united-fc",),("losc-lille",)]
)
def test_cargar_data_equipo_estadio(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	data=extraerDataEquipoEstadio(equipo)

	data_limpia=limpiarDataEquipoEstadio(data)

	cargarDataEquipoEstadio(data_limpia, equipo, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM equipo_estadio")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),
	("seleccion-santa-amalia",),("fc-porto",),("malaga",),("racing",),
	("salzburgo",),("manchester-united-fc",),("losc-lille",)]
)
def test_cargar_data_equipo_estadio_existente(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	data=extraerDataEquipoEstadio(equipo)

	data_limpia=limpiarDataEquipoEstadio(data)

	cargarDataEquipoEstadio(data_limpia, equipo, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio=len(conexion.c.fetchall())

	data=extraerDataEquipoEstadio(equipo)

	data_limpia=limpiarDataEquipoEstadio(data)

	cargarDataEquipoEstadio(data_limpia, equipo, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio_nuevos=len(conexion.c.fetchall())

	assert numero_registros_estadio==numero_registros_estadio_nuevos
	assert numero_registros_equipo_estadio==numero_registros_equipo_estadio_nuevos

def test_cargar_data_equipo_estadio_nuevo(conexion, entorno):

	conexion.insertarEquipo("atletico-madrid")

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarEquipoEstadio(("atletico-madrid", "vicente-calderon"))

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio=len(conexion.c.fetchall())

	data=extraerDataEquipoEstadio("atletico-madrid")

	data_limpia=limpiarDataEquipoEstadio(data)

	cargarDataEquipoEstadio(data_limpia, "atletico-madrid", entorno)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevo=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio_nuevo=len(conexion.c.fetchall())

	assert numero_registros_estadio_nuevo==numero_registros_estadio+1
	assert numero_registros_equipo_estadio_nuevo==numero_registros_equipo_estadio

def test_cargar_data_equipo_estadio_mas_de_uno(conexion, entorno):

	conexion.insertarEquipo("atletico-madrid")

	estadio=['riyadh-air-metropolitano-23', 23, 'Metropolitano', 'Av Luis Aragones',
			40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarEquipoEstadio(("atletico-madrid", "riyadh-air-metropolitano-23"))

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarEquipoEstadio(("atletico-madrid", "vicente-calderon"))

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio=len(conexion.c.fetchall())

	data=extraerDataEquipoEstadio("atletico-madrid")

	data_limpia=limpiarDataEquipoEstadio(data)

	cargarDataEquipoEstadio(data_limpia, "atletico-madrid", entorno)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevo=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM equipo_estadio")

	numero_registros_equipo_estadio_nuevo=len(conexion.c.fetchall())

	assert numero_registros_estadio_nuevo==numero_registros_estadio
	assert numero_registros_equipo_estadio_nuevo==numero_registros_equipo_estadio-1

@pytest.mark.parametrize(["equipo1", "equipo2"],
	[
		("flamengo-rio-janeiro", "fluminense-rio-janeiro"),
		# ("milan", "internazionale"), # Han cambiado el nombre (San Siro y Giussepe Meazza pero realmente es el mismo)
		("roma", "lazio")
	]
)
def test_cargar_data_equipo_estadio_compartido(conexion, entorno, equipo1, equipo2):

	conexion.insertarEquipo(equipo1)

	data=extraerDataEquipoEstadio(equipo1)

	data_limpia=limpiarDataEquipoEstadio(data)

	cargarDataEquipoEstadio(data_limpia, equipo1, entorno)

	conexion.insertarEquipo(equipo2)

	data=extraerDataEquipoEstadio(equipo2)

	data_limpia=limpiarDataEquipoEstadio(data)

	cargarDataEquipoEstadio(data_limpia, equipo2, entorno)

	conexion.c.execute("SELECT * FROM estadios")

	assert len(conexion.c.fetchall())==1

	conexion.c.execute("SELECT * FROM equipo_estadio")

	assert len(conexion.c.fetchall())==2