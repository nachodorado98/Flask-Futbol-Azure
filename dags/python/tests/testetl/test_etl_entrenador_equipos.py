import pytest
import pandas as pd

from src.etl_entrenador_equipos import extraerDataEntrenadorEquipos, limpiarDataEntrenadorEquipos, cargarDataEntrenadorEquipos
from src.scrapers.excepciones_scrapers import EntrenadorEquiposError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_entrenador_equipos_error_endpoint(endpoint):

	with pytest.raises(EntrenadorEquiposError):

		extraerDataEntrenadorEquipos(endpoint)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_extraer_data_entrenador_equipos(entrenador):

	data=extraerDataEntrenadorEquipos(entrenador)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data.columns)==8

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_limpiar_data_entrenador_equipos(entrenador):

	data=extraerDataEntrenadorEquipos(entrenador)

	data_limpia=limpiarDataEntrenadorEquipos(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==7

def test_cargar_data_entrenador_equipos_error_no_existe(conexion, entorno):

	data=extraerDataEntrenadorEquipos("diego-simeone-13")

	data_limpia=limpiarDataEntrenadorEquipos(data)

	with pytest.raises(Exception):

		cargarDataEntrenadorEquipos(data_limpia, "diego-simeone-13", entorno)

def test_cargar_data_entrenador_equipos_datos_error(conexion, entorno):

	conexion.insertarEntrenador("diego-simeone-13")

	data=extraerDataEntrenadorEquipos("diego-simeone-13")

	data_limpia=limpiarDataEntrenadorEquipos(data)

	data_limpia["Partidos_Totales"]="cien"

	with pytest.raises(Exception):

		cargarDataEntrenadorEquipos(data_limpia, "diego-simeone-13", entorno)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_cargar_data_entrenador_equipos(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	data=extraerDataEntrenadorEquipos(entrenador)

	data_limpia=limpiarDataEntrenadorEquipos(data)

	cargarDataEntrenadorEquipos(data_limpia, entrenador, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM entrenadores_equipo")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_cargar_data_entrenador_equipos_equipos_existente(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	data=extraerDataEntrenadorEquipos(entrenador)

	data_limpia=limpiarDataEntrenadorEquipos(data)

	cargarDataEntrenadorEquipos(data_limpia, entrenador, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_equipos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM entrenadores_equipo")

	numero_registros_equipos_entrenador=len(conexion.c.fetchall())

	data=extraerDataEntrenadorEquipos(entrenador)

	data_limpia=limpiarDataEntrenadorEquipos(data)

	cargarDataEntrenadorEquipos(data_limpia, entrenador, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_equipos_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM entrenadores_equipo")

	numero_registros_equipos_entrenador_nuevos=len(conexion.c.fetchall())

	assert numero_registros_equipos==numero_registros_equipos_nuevos
	assert numero_registros_equipos_entrenador==numero_registros_equipos_entrenador_nuevos