import pytest
import pandas as pd

from src.etl_partido_goleadores import extraerDataPartidoGoleadores, limpiarDataPartidoGoleadores, cargarDataPartidoGoleadores
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

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_limpiar_data_partido_goleadores(local, visitante, partido_id):

	data=extraerDataPartidoGoleadores(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoGoleadores(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==4

def test_cargar_data_partido_goleadores_error_no_existe(conexion):

	data=extraerDataPartidoGoleadores("atletico-madrid", "internazionale", "2024645009")

	data_limpia=limpiarDataPartidoGoleadores(data)

	with pytest.raises(Exception):

		cargarDataPartidoGoleadores(data_limpia, "2024645009")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_cargar_data_partido_competicion(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoGoleadores(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoGoleadores(data)

	cargarDataPartidoGoleadores(data_limpia, partido_id)

	conexion.c.execute("SELECT * FROM jugadores")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_goleador")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_cargar_data_partido_competicion_existentes(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoGoleadores(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoGoleadores(data)

	cargarDataPartidoGoleadores(data_limpia, partido_id)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_jugadores=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_goleador")

	numero_registros_goleadores=len(conexion.c.fetchall())

	data=extraerDataPartidoGoleadores(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoGoleadores(data)

	cargarDataPartidoGoleadores(data_limpia, partido_id)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_jugadores_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_goleador")

	numero_registros_goleadores_nuevos=len(conexion.c.fetchall())

	assert numero_registros_jugadores==numero_registros_jugadores_nuevos
	assert numero_registros_goleadores==numero_registros_goleadores_nuevos