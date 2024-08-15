import pytest
import pandas as pd

from src.etl_partido_competicion import extraerDataPartidoCompeticion
from src.scrapers.excepciones_scrapers import PartidoCompeticionError

def test_extraer_data_partido_competicion_error_endpoint():

	with pytest.raises(PartidoCompeticionError):

		extraerDataPartidoCompeticion("equipo1", "equipo2", "partido_id")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "202429286"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_extraer_data_partido_competicion(local, visitante, partido_id):

	data=extraerDataPartidoCompeticion(local, visitante, partido_id)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1
	assert len(data.columns)==1

	print(data)