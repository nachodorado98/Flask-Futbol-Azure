import pytest
import pandas as pd

from src.etl_partido_estadio import extraerDataPartidoEstadio, limpiarDataPartidoEstadio, cargarDataPartidoEstadio
from src.scrapers.excepciones_scrapers import PartidoEstadioError

def test_extraer_data_partido_estadio_error_endpoint():

	with pytest.raises(PartidoEstadioError):

		extraerDataPartidoEstadio("equipo1", "equipo2", "partido_id")

def test_extraer_data_partido_estadio_error_no_existe():

	with pytest.raises(PartidoEstadioError):

		extraerDataPartidoEstadio("numancia", "atletico-madrid", "2024489479")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_extraer_data_partido_estadio(local, visitante, partido_id):

	data=extraerDataPartidoEstadio(local, visitante, partido_id)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_limpiar_data_partido_estadio(local, visitante, partido_id):

	data=extraerDataPartidoEstadio(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoEstadio(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==13
	assert len(data_limpia)==1

def test_cargar_data_partido_estadio_error_no_existe(conexion):

	data=extraerDataPartidoEstadio("atletico-madrid", "internazionale", "2024645009")

	data_limpia=limpiarDataPartidoEstadio(data)

	with pytest.raises(Exception):

		cargarDataPartidoEstadio(data_limpia, "2024645009")

def test_cargar_data_partido_estadio_datos_error(conexion):

	conexion.insertarEquipo("atletico-madrid")

	partido=["1", "atletico-madrid", "atletico-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoEstadio("atletico-madrid", "internazionale", "2024645009")

	data_limpia=limpiarDataPartidoEstadio(data)

	data_limpia["Fecha"]="numero"

	with pytest.raises(Exception):

		cargarDataPartidoEstadio(data_limpia, "2024645009")

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_cargar_data_partido_estadio(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoEstadio(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoEstadio(data)

	cargarDataPartidoEstadio(data_limpia, partido_id)

	conexion.c.execute("SELECT * FROM estadios")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partido_estadio")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_cargar_data_partido_estadio_existente(conexion, local, visitante, partido_id):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoEstadio(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoEstadio(data)

	cargarDataPartidoEstadio(data_limpia, partido_id)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_estadio")

	numero_registros_partido_estadio=len(conexion.c.fetchall())

	data=extraerDataPartidoEstadio(local, visitante, partido_id)

	data_limpia=limpiarDataPartidoEstadio(data)

	cargarDataPartidoEstadio(data_limpia, partido_id)

	conexion.c.execute("SELECT * FROM estadios")

	numero_registros_estadio_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM partido_estadio")

	numero_registros_partido_estadio_nuevos=len(conexion.c.fetchall())

	assert numero_registros_estadio==numero_registros_estadio_nuevos
	assert numero_registros_partido_estadio==numero_registros_partido_estadio_nuevos


@pytest.mark.parametrize(["local", "visitante", "partido_id_ida", "partido_id_vuelta"],
	[
		# ("milan", "internazionale", "2024103419", "202524914"), # Han cambiado el nombre (San Siro y Giussepe Meazza pero realmente es el mismo)
		("flamengo-rio-janeiro", "fluminense-rio-janeiro", "2024706960", "2024706771"),
		("roma", "lazio", "2024103401", "2024662727")
	]
)
def test_cargar_data_partido_estadio_compartido(conexion, local, visitante, partido_id_ida, partido_id_vuelta):

	conexion.insertarEquipo(local)

	conexion.insertarEquipo(visitante)

	partido=[partido_id_ida, local, visitante, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoEstadio(local, visitante, partido_id_ida)

	data_limpia=limpiarDataPartidoEstadio(data)

	cargarDataPartidoEstadio(data_limpia, partido_id_ida)

	partido=[partido_id_vuelta, visitante, local, "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	data=extraerDataPartidoEstadio(visitante, local, partido_id_vuelta)

	data_limpia=limpiarDataPartidoEstadio(data)

	cargarDataPartidoEstadio(data_limpia, partido_id_vuelta)

	conexion.c.execute("SELECT * FROM estadios")

	assert len(conexion.c.fetchall())==1

	conexion.c.execute("SELECT * FROM partido_estadio")

	assert len(conexion.c.fetchall())==2