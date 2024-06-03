import pytest
import pandas as pd

from src.etl_equipo import extraerDataEquipoDetalle, limpiarDataEquipoDetalle
from src.scrapers.excepciones_scrapers import EquipoError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_detalle_error_endpoint(endpoint):

	with pytest.raises(EquipoError):

		extraerDataEquipoDetalle(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),
	("kakamega-homeboyz",),("sporting-gijon",),("albacete",),
	("racing",),("atalanta",),("malaga",),("hull-city",)]
)
def test_extraer_data_equipo_detalle(equipo):

	data=extraerDataEquipoDetalle(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),
	("kakamega-homeboyz",),("sporting-gijon",),("albacete",),
	("racing",),("atalanta",),("malaga",),("hull-city",)]
)
def test_limpiar_data_equipo(equipo):

	data=extraerDataEquipoDetalle(equipo)

	data_limpia=limpiarDataEquipoDetalle(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==14
	assert len(data_limpia)==1