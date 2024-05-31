import pytest
import pandas as pd

from src.extraer_equipos_liga import extraerDataEquiposLiga
from src.scrapers.excepciones_scrapers import EquiposLigaError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_equipos_liga_error_endpoint(endpoint):

	with pytest.raises(EquiposLigaError):

		extraerDataEquiposLiga(endpoint)

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/1996",),("/primera/2019",), ("bundesliga",),("premier",)]
)
def test_extraer_data_equipos_liga(endpoint):

	data=extraerDataEquiposLiga(endpoint)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty