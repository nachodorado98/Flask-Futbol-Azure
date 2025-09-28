import pytest
import pandas as pd

from src.etl_equipo_palmares import extraerDataEquipoPalmares
from src.scrapers.excepciones_scrapers import EquipoPalmaresError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_palmares_error_endpoint(endpoint):

	with pytest.raises(EquipoPalmaresError):

		extraerDataEquipoPalmares(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("cd-valdehornillo-a-senior",),("seleccion-santa-amalia",)]
)
def test_extraer_data_equipo_palmares_error_no_existe(equipo):

	with pytest.raises(EquipoPalmaresError):

		extraerDataEquipoPalmares(equipo)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_extraer_data_equipo_palmares(equipo):

	data=extraerDataEquipoPalmares(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)>1