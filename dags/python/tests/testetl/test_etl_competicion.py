import pytest
import pandas as pd

from src.etl_competicion import extraerDataCompeticion
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