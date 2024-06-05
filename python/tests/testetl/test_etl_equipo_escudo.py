import pytest
import pandas as pd

from src.etl_equipo_escudo import extraerDataEquipoEscudo
from src.scrapers.excepciones_scrapers import EquipoEscudoError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_escudo_error_endpoint(endpoint):

	with pytest.raises(EquipoEscudoError):

		extraerDataEquipoEscudo(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),
	("kakamega-homeboyz",),("cd-valdehornillo-a-senior",),("seleccion-santa-amalia",)]
)
def test_extraer_data_equipo_escudo(equipo):

	data=extraerDataEquipoEscudo(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1