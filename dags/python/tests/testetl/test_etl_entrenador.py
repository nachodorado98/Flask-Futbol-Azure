import pytest
import pandas as pd

from src.etl_entrenador import extraerDataEntrenador, limpiarDataEntrenador, cargarDataEntrenador
from src.scrapers.excepciones_scrapers import EntrenadorError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_entrenador_error_endpoint(endpoint):

	with pytest.raises(EntrenadorError):

		extraerDataEntrenador(endpoint)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),
	("fernando-torres-47437",),("luis-aragones-1918",),("radomir-antic-2601",)]
)
def test_extraer_data_entrenador(entrenador):

	data=extraerDataEntrenador(entrenador)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),
	("fernando-torres-47437",),("luis-aragones-1918",),("radomir-antic-2601",)]
)
def test_limpiar_data_entrenador(entrenador):

	data=extraerDataEntrenador(entrenador)

	data_limpia=limpiarDataEntrenador(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==5
	assert len(data_limpia)==1

def test_cargar_data_entrenador_error_no_existe(conexion):

	data=extraerDataEntrenador("diego-simeone-13")

	data_limpia=limpiarDataEntrenador(data)

	with pytest.raises(Exception):

		cargarDataEntrenador(data_limpia, "diego-simeone-13")

def test_cargar_data_entrenador_datos_error(conexion):

	conexion.insertarEntrenador("diego-simeone-13")

	data=extraerDataEntrenador("diego-simeone-13")

	data_limpia=limpiarDataEntrenador(data)

	data_limpia["Puntuacion"]="puntuacion"

	with pytest.raises(Exception):

		cargarDataEntrenador(data_limpia, "diego-simeone-13")

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_cargar_data_entrenador_datos_correctos_con_equipo(conexion, entrenador):

	conexion.insertarEntrenador(entrenador)

	data=extraerDataEntrenador(entrenador)

	data_limpia=limpiarDataEntrenador(data)

	cargarDataEntrenador(data_limpia, entrenador)

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
def test_cargar_data_entrenador_datos_correctos_sin_equipo(conexion, entrenador):

	conexion.insertarEntrenador(entrenador)

	data=extraerDataEntrenador(entrenador)

	data_limpia=limpiarDataEntrenador(data)

	cargarDataEntrenador(data_limpia, entrenador)

	conexion.c.execute(f"SELECT * FROM entrenadores WHERE Entrenador_Id='{entrenador}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert not datos_actualizados["equipo_id"]
	assert datos_actualizados["codigo_pais"] is not None
	assert datos_actualizados["codigo_entrenador"] is not None
	assert datos_actualizados["puntuacion"] is not None

	conexion.c.execute("SELECT * FROM equipos")

	assert not conexion.c.fetchall()