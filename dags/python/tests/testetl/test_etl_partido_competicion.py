import pytest
import pandas as pd

from src.etl_partido_competicion import extraerDataPartidoCompeticion, limpiarDataPartidoCompeticion, cargarDataPartidoCompeticion
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

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "202429286"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_limpiar_data_partido_competicion(local, visitante, partido_id):

	data=extraerDataPartidoCompeticion(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoCompeticion(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data)==1
	assert len(data_limpia.columns)==1

def test_cargar_data_partido_competicion_error_no_existe(conexion, entorno):

	data=extraerDataPartidoCompeticion("atletico-madrid", "internazionale", "2024645009")

	data_limpia=limpiarDataPartidoCompeticion(data)

	with pytest.raises(Exception):

		cargarDataPartidoCompeticion(data_limpia, "2024645009", entorno)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "202429286"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_cargar_data_partido_competicion(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoCompeticion(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoCompeticion(data)

	cargarDataPartidoCompeticion(data_limpia, partido_id, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_competicion")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "202429286"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_cargar_data_partido_competicion_existente(conexion, entorno, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoCompeticion(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoCompeticion(data)

	cargarDataPartidoCompeticion(data_limpia, partido_id, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_competicion")

	numero_registros_partido_competicion=len(conexion.c.fetchall())

	data=extraerDataPartidoCompeticion(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoCompeticion(data)

	cargarDataPartidoCompeticion(data_limpia, partido_id, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_competicion")

	numero_registros_partido_competicion_nuevos=len(conexion.c.fetchall())

	assert numero_registros_competiciones==numero_registros_competiciones_nuevos
	assert numero_registros_partido_competicion==numero_registros_partido_competicion_nuevos