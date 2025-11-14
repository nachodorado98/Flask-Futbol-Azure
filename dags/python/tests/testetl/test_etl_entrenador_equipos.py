import pytest
import pandas as pd

from src.etl_entrenador_equipos import extraerDataEntrenadorEquipos, limpiarDataEntrenadorEquipos
from src.scrapers.excepciones_scrapers import EntrenadorEquiposError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_entrenador_equipos_error_endpoint(endpoint):

	with pytest.raises(EntrenadorEquiposError):

		extraerDataEntrenadorEquipos(endpoint)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_extraer_data_entrenador_equipos(entrenador):

	data=extraerDataEntrenadorEquipos(entrenador)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data.columns)==8

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_limpiar_data_entrenador_equipos(entrenador):

	data=extraerDataEntrenadorEquipos(entrenador)

	data_limpia=limpiarDataEntrenadorEquipos(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==7