import pytest
import pandas as pd

from src.etl_entrenador_palmares import extraerDataEntrenadorPalmares, limpiarDataEntrenadorPalmares, cargarDataEntrenadorPalmares
from src.scrapers.excepciones_scrapers import EntrenadorPalmaresError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_entrenador_palmares_error_endpoint(endpoint):

	with pytest.raises(EntrenadorPalmaresError):

		extraerDataEntrenadorPalmares(endpoint)

@pytest.mark.parametrize(["entrenador"],
	[("jakob-poulsen-63406",),("ricardo-fajardo-19230",),("alejandro-alvarez-43905",)]
)
def test_extraer_data_entrenador_palmares_error_no_existe(entrenador):

	with pytest.raises(EntrenadorPalmaresError):

		extraerDataEntrenadorPalmares(entrenador)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_extraer_data_entrenador_palmares(entrenador):

	data=extraerDataEntrenadorPalmares(entrenador)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)>0

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_limpiar_data_entrenador_palmares(entrenador):

	data=extraerDataEntrenadorPalmares(entrenador)

	data_limpia=limpiarDataEntrenadorPalmares(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data.empty
	assert len(data)==len(data_limpia)
	assert len(data_limpia.columns)==5

def test_cargar_data_entrenador_palmares_error_no_existe(conexion, entorno):

	data=extraerDataEntrenadorPalmares("diego-simeone-13")

	data_limpia=limpiarDataEntrenadorPalmares(data)

	with pytest.raises(Exception):

		cargarDataEntrenadorPalmares(data_limpia, "diego-simeone-13", entorno)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",)]
)
def test_cargar_data_entrenador_palmares_no_competiciones(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	data=extraerDataEntrenadorPalmares(entrenador)

	data_limpia=limpiarDataEntrenadorPalmares(data)

	cargarDataEntrenadorPalmares(data_limpia, entrenador, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert not conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	assert not conexion.c.fetchall()

def test_cargar_data_entrenador_palmares_datos_error(conexion, entorno):

	conexion.insertarEntrenador("diego-simeone-13")

	conexion.insertarCompeticion("primera")

	data=extraerDataEntrenadorPalmares("diego-simeone-13")

	data_limpia=limpiarDataEntrenadorPalmares(data)

	data_limpia["Numero"]="numero"

	with pytest.raises(Exception):

		cargarDataEntrenadorPalmares(data_limpia, "diego-simeone-13", entorno)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",)]
)
def test_cargar_data_entrenador_palmares(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	conexion.insertarCompeticion("primera")

	data=extraerDataEntrenadorPalmares(entrenador)

	data_limpia=limpiarDataEntrenadorPalmares(data)

	cargarDataEntrenadorPalmares(data_limpia, entrenador, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	assert conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",)]
)
def test_cargar_data_entrenador_palmares_existente(conexion, entorno, entrenador):

	conexion.insertarEntrenador(entrenador)

	conexion.insertarCompeticion("primera")

	data=extraerDataEntrenadorPalmares(entrenador)

	data_limpia=limpiarDataEntrenadorPalmares(data)

	cargarDataEntrenadorPalmares(data_limpia, entrenador, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones=conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	codigo_titulo=conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	numero_registros_entrenador_titulo=conexion.c.fetchall()

	data=extraerDataEntrenadorPalmares(entrenador)

	data_limpia=limpiarDataEntrenadorPalmares(data)

	cargarDataEntrenadorPalmares(data_limpia, entrenador, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	codigo_titulo_nuevo=conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	numero_registros_entrenador_titulo_nuevos=conexion.c.fetchall()

	assert numero_registros_competiciones==numero_registros_competiciones_nuevos
	assert codigo_titulo==codigo_titulo_nuevo
	assert numero_registros_entrenador_titulo==numero_registros_entrenador_titulo_nuevos