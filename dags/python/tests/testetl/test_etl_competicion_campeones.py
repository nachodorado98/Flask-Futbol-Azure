import pytest
import pandas as pd

from src.etl_competicion_campeones import extraerDataCampeonesCompeticion, limpiarDataCampeonesCompeticion, cargarDataCampeonesCompeticion
from src.scrapers.excepciones_scrapers import CompeticionCampeonesError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_competicion_campeones_error_endpoint(endpoint):

	with pytest.raises(CompeticionCampeonesError):

		extraerDataCampeonesCompeticion(endpoint)

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_extraer_data_competicion_campeones(competicion):

	data=extraerDataCampeonesCompeticion(competicion)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty

def test_limpiar_data_competicion_campeones_anos_nulos():

	data=extraerDataCampeonesCompeticion("primera")

	data["Ano"]=None

	with pytest.raises(Exception):

		limpiarDataCampeonesCompeticion(data)

def test_limpiar_data_competicion_campeones_equipos_nulos():

	data=extraerDataCampeonesCompeticion("primera")

	data["Equipo_URL"]=None

	with pytest.raises(Exception):

		limpiarDataCampeonesCompeticion(data)

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_limpiar_data_competicion_campeones(competicion):

	data=extraerDataCampeonesCompeticion(competicion)

	data_limpia=limpiarDataCampeonesCompeticion(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==2

def test_cargar_data_competicion_campeones_error_no_existe(conexion, entorno):

	data=extraerDataCampeonesCompeticion("primera")

	data_limpia=limpiarDataCampeonesCompeticion(data)

	with pytest.raises(Exception):

		cargarDataCampeonesCompeticion(data_limpia, "primera", entorno)

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_cargar_data_competicion_campeones(conexion, entorno, competicion):

	conexion.insertarCompeticion(competicion)

	data=extraerDataCampeonesCompeticion(competicion)

	data_limpia=limpiarDataCampeonesCompeticion(data)

	cargarDataCampeonesCompeticion(data_limpia, competicion, entorno)

	conexion.c.execute("SELECT * FROM competiciones_campeones")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_cargar_data_competicion_campeones_existentes(conexion, entorno, competicion):

	conexion.insertarCompeticion(competicion)

	data=extraerDataCampeonesCompeticion(competicion)

	data_limpia=limpiarDataCampeonesCompeticion(data)

	cargarDataCampeonesCompeticion(data_limpia, competicion, entorno)

	conexion.c.execute("SELECT * FROM competiciones_campeones")

	numero_registros_campeones=len(conexion.c.fetchall())

	data=extraerDataCampeonesCompeticion(competicion)

	data_limpia=limpiarDataCampeonesCompeticion(data)

	cargarDataCampeonesCompeticion(data_limpia, competicion, entorno)

	conexion.c.execute("SELECT * FROM competiciones_campeones")

	numero_registros_nuevos_campeones=len(conexion.c.fetchall())

	assert numero_registros_campeones==numero_registros_nuevos_campeones