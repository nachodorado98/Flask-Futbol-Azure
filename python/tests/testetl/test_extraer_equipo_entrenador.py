import pytest
import pandas as pd

from src.extraer_equipo_entrenador import extraerDataEquipoEntrenador
from src.scrapers.excepciones_scrapers import EquipoEntrenadorError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_entrenador_error_endpoint(endpoint):

	with pytest.raises(EquipoEntrenadorError):

		extraerDataEquipoEntrenador(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("kakamega-homeboyz",),("cd-valdehornillo-a-senior",),("seleccion-santa-amalia",)]
)
def test_extraer_data_equipo_entrenador_error_no_existe(equipo):

	with pytest.raises(EquipoEntrenadorError):

		extraerDataEquipoEntrenador(equipo)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_extraer_data_equipo_entrenador(equipo):

	data=extraerDataEquipoEntrenador(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1