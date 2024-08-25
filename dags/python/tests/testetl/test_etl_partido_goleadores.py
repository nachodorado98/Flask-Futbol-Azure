import pytest
import pandas as pd

from src.etl_partido_goleadores import extraerDataPartidoGoleadores
from src.scrapers.excepciones_scrapers import PartidoGoleadoresError

def test_extraer_data_partido_goleadores_error_endpoint():

	with pytest.raises(PartidoGoleadoresError):

		extraerDataPartidoGoleadores("equipo1", "equipo2", "partido_id")

def test_extraer_data_partido_goleadores_no_existe():

	with pytest.raises(PartidoGoleadoresError):

		extraerDataPartidoGoleadores("atletico-madrid", "alianza-lima", "201313927")

def test_extraer_data_partido_goleadores_no_hay():

	with pytest.raises(PartidoGoleadoresError):

		extraerDataPartidoGoleadores("betis", "atletico-madrid", "202430028")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_extraer_data_partido_goleadores(local, visitante, partido_id):

	data=extraerDataPartidoGoleadores(local, visitante, partido_id)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data.columns)==3