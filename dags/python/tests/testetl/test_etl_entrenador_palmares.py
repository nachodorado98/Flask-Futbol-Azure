import pytest
import pandas as pd

from src.etl_entrenador_palmares import extraerDataEntrenadorPalmares
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