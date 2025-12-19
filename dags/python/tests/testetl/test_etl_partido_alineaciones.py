import pytest
import pandas as pd

from src.etl_partido_alineaciones import extraerDataPartidoAlineaciones, limpiarDataPartidoAlineaciones, cargarDataPartidoAlineaciones
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

def test_limpiar_data_partidos_alineaciones_entrenador_nulos():

	data=extraerDataPartidoAlineaciones("atletico-madrid", "real-union-club-irun", "1921954")

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
		("atletico-madrid", "almeria", "2021113990")
	]
)
def test_limpiar_data_partido_alineaciones(local, visitante, partido_id):

	data=extraerDataPartidoAlineaciones(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoAlineaciones(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==8
	assert data_limpia[(data_limpia["Local"]==True)&(data_limpia["Titular"]==True)].shape[0]==11 or data_limpia[(data_limpia["Local"]==False)&(data_limpia["Titular"]==True)].shape[0]==11

def test_cargar_data_partido_alineaciones_error_no_existe(conexion, entorno):

	data=extraerDataPartidoAlineaciones("atletico-madrid", "internazionale", "2024645009")

	data_limpia=limpiarDataPartidoAlineaciones(data)

	with pytest.raises(Exception):

		cargarDataPartidoAlineaciones(data_limpia, "2024645009", entorno)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009"),
		("atletico-madrid", "almeria", "2021113990"),
		("atletico-madrid", "paok", "199818752"),
		("atletico-madrid", "internazionale", "2026180098")
	]
)
def test_cargar_data_partido_alineaciones(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoAlineaciones(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoAlineaciones(data)

	cargarDataPartidoAlineaciones(data_limpia, partido_id, entorno)

	conexion.c.execute("SELECT * FROM entrenadores")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_entrenador")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM jugadores")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_jugador")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009"),
		("atletico-madrid", "almeria", "2021113990"),
		("atletico-madrid", "paok", "199818752"),
		("atletico-madrid", "internazionale", "2026180098")
	]
)
def test_cargar_data_partido_alineaciones_existentes(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoAlineaciones(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoAlineaciones(data)

	cargarDataPartidoAlineaciones(data_limpia, partido_id, entorno)

	conexion.c.execute("SELECT * FROM entrenadores")

	numero_registros_entrenadores=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_entrenador")

	numero_registros_partido_entrenadores=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_jugadores=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_jugador")

	numero_registros_partido_jugadores=conexion.c.fetchall()

	data=extraerDataPartidoAlineaciones(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoAlineaciones(data)

	cargarDataPartidoAlineaciones(data_limpia, partido_id, entorno)

	conexion.c.execute("SELECT * FROM entrenadores")

	numero_registros_entrenadores_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_entrenador")

	numero_registros_partido_entrenadores_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_jugadores_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_jugador")

	numero_registros_partido_jugadores_nuevos=conexion.c.fetchall()

	assert numero_registros_entrenadores==numero_registros_entrenadores_nuevos
	assert numero_registros_partido_entrenadores==numero_registros_partido_entrenadores_nuevos
	assert numero_registros_jugadores==numero_registros_jugadores_nuevos
	assert numero_registros_partido_jugadores==numero_registros_partido_jugadores_nuevos