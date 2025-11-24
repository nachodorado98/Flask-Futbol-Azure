import pytest
import pandas as pd

from src.etl_partido_alineaciones import extraerDataPartidoAlineaciones, limpiarDataPartidoAlineaciones
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

def test_limpiar_data_partidos_alineaciones_puntos_nulos():

	data=extraerDataPartidoAlineaciones("valladolid", "atletico-madrid", "20256422")

	data["Puntos"]=None

	with pytest.raises(Exception):

		limpiarDataPartidoAlineaciones(data)

def test_limpiar_data_partidos_alineaciones_tactica_nulos():

	data=extraerDataPartidoAlineaciones("valladolid", "atletico-madrid", "20256422")

	data["Tactica"]=None

	with pytest.raises(Exception):

		limpiarDataPartidoAlineaciones(data)

def test_limpiar_data_partidos_alineaciones_titulares_faltantes_ambos():

	data=extraerDataPartidoAlineaciones("valladolid", "atletico-madrid", "20256422")

	data=data[((data["Tipo"]=="L")&(data["Alineacion"]=="T")&(data["Posicion"].isin([1, 2, 3])))|(data["Tipo"]=="V")]

	data=data[((data["Tipo"]=="V")&(data["Alineacion"]=="T")&(data["Posicion"].isin([1, 2, 3])))|(data["Tipo"]=="L")]

	with pytest.raises(Exception):

		limpiarDataPartidoAlineaciones(data)

def test_limpiar_data_partidos_alineaciones_titulares_faltantes_local():

	data=extraerDataPartidoAlineaciones("valladolid", "atletico-madrid", "20256422")

	data=data[((data["Tipo"]=="L")&(data["Alineacion"]=="T")&(data["Posicion"].isin([1, 2, 3])))|(data["Tipo"]=="V")]
	
	data_limpia=limpiarDataPartidoAlineaciones(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==8
	assert data_limpia[(data_limpia["Local"]==True)&(data_limpia["Titular"]==True)].empty
	assert not data_limpia[(data_limpia["Local"]==False)&(data_limpia["Titular"]==True)].empty
	assert data_limpia[(data_limpia["Local"]==False)&(data_limpia["Titular"]==True)].shape[0]==11

def test_limpiar_data_partidos_alineaciones_titulares_faltantes_visitante():

	data=extraerDataPartidoAlineaciones("valladolid", "atletico-madrid", "20256422")

	data=data[((data["Tipo"]=="V")&(data["Alineacion"]=="T")&(data["Posicion"].isin([1, 2, 3])))|(data["Tipo"]=="L")]
	
	data_limpia=limpiarDataPartidoAlineaciones(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==8
	assert not data_limpia[(data_limpia["Local"]==True)&(data_limpia["Titular"]==True)].empty
	assert data_limpia[(data_limpia["Local"]==False)&(data_limpia["Titular"]==True)].empty
	assert data_limpia[(data_limpia["Local"]==True)&(data_limpia["Titular"]==True)].shape[0]==11

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("atletico-madrid", "almeria", "2021113990"),
		("cd-arcangel", "atletico-madrid", "201210617")
	]
)
def test_limpiar_data_partido_alineaciones(local, visitante, partido_id):

	data=extraerDataPartidoAlineaciones(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoAlineaciones(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==8
	assert data_limpia[(data_limpia["Local"]==True)&(data_limpia["Titular"]==True)].shape[0]==11 or data_limpia[(data_limpia["Local"]==False)&(data_limpia["Titular"]==True)].shape[0]==11