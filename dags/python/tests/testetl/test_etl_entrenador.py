import pytest
import pandas as pd

from src.etl_entrenador import extraerDataEntrenador
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