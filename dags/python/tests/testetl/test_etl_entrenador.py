import pytest
import pandas as pd

from src.etl_entrenador import extraerDataEntrenador, limpiarDataEntrenador
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