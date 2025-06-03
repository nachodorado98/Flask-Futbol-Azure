import pytest
import pandas as pd

from src.etl_equipo_entrenador import extraerDataEquipoEntrenador, limpiarDataEquipoEntrenador, cargarDataEquipoEntrenador
from src.scrapers.excepciones_scrapers import EquipoEntrenadorError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_entrenador_error_endpoint(endpoint):

	with pytest.raises(EquipoEntrenadorError):

		extraerDataEquipoEntrenador(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("kakamega-homeboyz",),("cd-valdehornillo-a-senior",),("k-league-all-star",)]
)
def test_extraer_data_equipo_entrenador_error_no_existe(equipo):

	with pytest.raises(EquipoEntrenadorError):

		extraerDataEquipoEntrenador(equipo)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_extraer_data_equipo_entrenador(equipo):

	data=extraerDataEquipoEntrenador(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),("fc-porto",)]
)
def test_limpiar_data_equipo_entrenador(equipo):

	data=extraerDataEquipoEntrenador(equipo)

	data_limpia=limpiarDataEquipoEntrenador(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==4
	assert len(data_limpia)==1

def test_cargar_data_equipo_entrenador_error_no_existe(conexion, entorno):

	data=extraerDataEquipoEntrenador("atletico-madrid")

	data_limpia=limpiarDataEquipoEntrenador(data)

	with pytest.raises(Exception):

		cargarDataEquipoEntrenador(data_limpia, "atletico-madrid", entorno)

def test_cargar_data_equipo_entrenador_datos_error(conexion, entorno):

	conexion.insertarEquipo("atletico-madrid")

	data=extraerDataEquipoEntrenador("atletico-madrid")

	data_limpia=limpiarDataEquipoEntrenador(data)

	data_limpia["Partidos"]="numero"

	with pytest.raises(Exception):

		cargarDataEquipoEntrenador(data_limpia, "atletico-madrid", entorno)

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_cargar_data_equipo_entrenador_datos_correctos(conexion, entorno, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	data=extraerDataEquipoEntrenador(nombre_equipo)

	data_limpia=limpiarDataEquipoEntrenador(data)

	cargarDataEquipoEntrenador(data_limpia, nombre_equipo, entorno)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["entrenador"] is not None
	assert datos_actualizados["entrenador_url"] is not None
	assert datos_actualizados["codigo_entrenador"] is not None
	assert datos_actualizados["partidos"] is not None