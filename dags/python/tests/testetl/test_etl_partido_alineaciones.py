import pytest
import pandas as pd

from src.etl_partido_alineaciones import extraerDataPartidoAlineaciones
from src.scrapers.excepciones_scrapers import PartidoAlineacionesError

def test_extraer_data_partido_alineaciones_error_endpoint():

	with pytest.raises(PartidoAlineacionesError):

		extraerDataPartidoAlineaciones("equipo1", "equipo2", "partido_id")

def test_extraer_data_partido_alineaciones_no_existe():

	with pytest.raises(PartidoAlineacionesError):

		extraerDataPartidoAlineaciones("atletico-madrid", "liverpool", "198923660")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("atletico-madrid", "almeria", "2021113990"),
		("gimnastica-segoviana", "atletico-madrid", "201210634"),
		("cd-arcangel", "atletico-madrid", "201210617")
	]
)
def test_extraer_data_partido_alineaciones(local, visitante, partido_id):

	data=extraerDataPartidoAlineaciones(local, visitante, partido_id)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data.columns)==8