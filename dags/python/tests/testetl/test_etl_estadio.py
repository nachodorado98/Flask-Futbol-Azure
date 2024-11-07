import pytest
import pandas as pd

from src.etl_estadio import extraerDataEstadio
from src.scrapers.excepciones_scrapers import EstadioError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_estadio_error_endpoint(endpoint):

	with pytest.raises(EstadioError):

		extraerDataEstadio(endpoint)

@pytest.mark.parametrize(["estadio"],
	[("riyadh-air-metropolitano-23",),("municipal-football-santa-amalia-4902",),("celtic-park-82",),("stadion-feijenoord-71",)]
)
def test_extraer_data_estadio(estadio):

	data=extraerDataEstadio(estadio)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1