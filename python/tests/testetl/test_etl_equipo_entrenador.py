import pytest
import pandas as pd

from src.etl_equipo_entrenador import extraerDataEquipoEntrenador, limpiarDataEquipoEntrenador
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

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),("fc-porto",)]
)
def test_limpiar_data_equipo_entrenador(equipo):

	data=extraerDataEquipoEntrenador(equipo)

	data_limpia=limpiarDataEquipoEntrenador(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==8
	assert len(data_limpia)==1
	assert data_limpia.iloc[0]["Partidos"]==data_limpia.iloc[0]["Ganados"]+data_limpia.iloc[0]["Empatados"]+data_limpia.iloc[0]["Perdidos"]