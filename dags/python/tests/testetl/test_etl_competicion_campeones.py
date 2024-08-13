import pytest
import pandas as pd

from src.etl_competicion_campeones import extraerDataCampeonesCompeticion, limpiarDataCampeonesCompeticion
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