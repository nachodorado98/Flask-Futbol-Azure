import pytest
import pandas as pd

from src.etl_partido_estadio import extraerDataPartidoEstadio
from src.scrapers.excepciones_scrapers import PartidoEstadioError

def test_extraer_data_partido_estadio_error_endpoint():

	with pytest.raises(PartidoEstadioError):

		extraerDataPartidoEstadio("equipo1", "equipo2", "partido_id")

def test_extraer_data_partido_estadio_error_no_existe():

	with pytest.raises(PartidoEstadioError):

		extraerDataPartidoEstadio("seleccion-santa-amalia", "cd-valdehornillo-a-senior", "2023350130")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "202429286"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_extraer_data_partido_estadio(local, visitante, partido_id):

	data=extraerDataPartidoEstadio(local, visitante, partido_id)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1