import pytest
import pandas as pd

from src.etl_equipo_estadio import extraerDataEquipoEstadio, limpiarDataEquipoEstadio
from src.scrapers.excepciones_scrapers import EquipoEstadioError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_estadio_error_endpoint(endpoint):

	with pytest.raises(EquipoEstadioError):

		extraerDataEquipoEstadio(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("kakamega-homeboyz",),("cd-valdehornillo-a-senior",)]
)
def test_extraer_data_equipo_estadio_error_no_existe(equipo):

	with pytest.raises(EquipoEstadioError):

		extraerDataEquipoEstadio(equipo)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),("seleccion-santa-amalia",)]
)
def test_extraer_data_equipo_estadio(equipo):

	data=extraerDataEquipoEstadio(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),
	("seleccion-santa-amalia",),("fc-porto",),("malaga",),("racing",)]
)
def test_limpiar_data_equipo_estadio(equipo):

	data=extraerDataEquipoEstadio(equipo)

	data_limpia=limpiarDataEquipoEstadio(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==13
	assert len(data_limpia)==1