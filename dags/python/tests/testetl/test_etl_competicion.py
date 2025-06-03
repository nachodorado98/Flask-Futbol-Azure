import pytest
import pandas as pd

from src.etl_competicion import extraerDataCompeticion, limpiarDataCompeticion, cargarDataCompeticion
from src.scrapers.excepciones_scrapers import CompeticionError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_competicion_error_endpoint(endpoint):

	with pytest.raises(CompeticionError):

		extraerDataCompeticion(endpoint)

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),("primera_division_argentina",),("primera_division_rfef",)]
)
def test_extraer_data_competicion(competicion):

	data=extraerDataCompeticion(competicion)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),("primera_division_argentina",),("primera_division_rfef",)]
)
def test_limpiar_data_competicion(competicion):

	data=extraerDataCompeticion(competicion)

	data_limpia=limpiarDataCompeticion(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==3
	assert len(data_limpia)==1

def test_cargar_data_competicion_error_no_existe(conexion, entorno):

	data=extraerDataCompeticion("primera")

	data_limpia=limpiarDataCompeticion(data)

	with pytest.raises(Exception):

		cargarDataCompeticion(data_limpia, "primera", entorno)

def test_cargar_data_competicion_datos_error(conexion, entorno):

	conexion.insertarCompeticion("primera")

	data=extraerDataCompeticion("primera")

	data_limpia=limpiarDataCompeticion(data)

	data_limpia["Codigo_Pais"]="codigo"

	with pytest.raises(Exception):

		cargarDataCompeticion(data_limpia, "primera", entorno)

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),("primera_division_argentina",),("primera_division_rfef",)]
)
def test_cargar_data_competicion_datos_correctos(conexion, entorno, competicion):

	conexion.insertarCompeticion(competicion)

	data=extraerDataCompeticion(competicion)

	data_limpia=limpiarDataCompeticion(data)

	cargarDataCompeticion(data_limpia, competicion, entorno)

	conexion.c.execute(f"SELECT * FROM competiciones WHERE Competicion_Id='{competicion}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert datos_actualizados["codigo_logo"] is not None
	assert datos_actualizados["codigo_pais"] is not None