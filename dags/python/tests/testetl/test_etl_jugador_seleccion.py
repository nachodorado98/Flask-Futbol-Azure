import pytest
import pandas as pd

from src.etl_jugador_seleccion import extraerDataJugadorSeleccion, limpiarDataJugadorSeleccion, cargarDataJugadorSeleccion
from src.scrapers.excepciones_scrapers import JugadorSeleccionError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_jugador_seleccion_error_endpoint(endpoint):

	with pytest.raises(JugadorSeleccionError):

		extraerDataJugadorSeleccion(endpoint)

@pytest.mark.parametrize(["jugador"],
	[("j-dorado-3363152",),("m-garcia-348428",),("gonzalez-375633",),
	("carlinos-189054",),("sergio-cordero-parral",)]
)
def test_extraer_data_jugador_seleccion_no_tiene(jugador):

	with pytest.raises(JugadorSeleccionError):

		extraerDataJugadorSeleccion(jugador)

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_extraer_data_jugador_seleccion(jugador):

	data=extraerDataJugadorSeleccion(jugador)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data.columns)==7
	assert len(data)==1

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_limpiar_data_jugador_seleccion(jugador):

	data=extraerDataJugadorSeleccion(jugador)

	data_limpia=limpiarDataJugadorSeleccion(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==4
	assert len(data_limpia)==1

def test_cargar_data_jugador_seleccion_error_no_existe(conexion):

	data=extraerDataJugadorSeleccion("j-alvarez-772644")

	data_limpia=limpiarDataJugadorSeleccion(data)

	with pytest.raises(Exception):

		cargarDataJugadorSeleccion(data_limpia, "j-alvarez-772644")

def test_cargar_data_jugador_seleccion_datos_error(conexion):

	conexion.insertarJugador("j-alvarez-772644")

	data=extraerDataJugadorSeleccion("j-alvarez-772644")

	data_limpia=limpiarDataJugadorSeleccion(data)

	data_limpia["Goles"]="gol"

	with pytest.raises(Exception):

		cargarDataJugadorSeleccion(data_limpia, "j-alvarez-772644")

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_cargar_data_jugador_seleccion(conexion, jugador):

	conexion.insertarJugador(jugador)

	data=extraerDataJugadorSeleccion(jugador)

	data_limpia=limpiarDataJugadorSeleccion(data)

	cargarDataJugadorSeleccion(data_limpia, jugador)

	conexion.c.execute("SELECT * FROM jugadores_seleccion")

	assert len(conexion.c.fetchall())==1

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_cargar_data_jugador_seleccion_seleccion_existente(conexion, jugador):

	conexion.insertarJugador(jugador)

	data=extraerDataJugadorSeleccion(jugador)

	data_limpia=limpiarDataJugadorSeleccion(data)

	cargarDataJugadorSeleccion(data_limpia, jugador)

	conexion.c.execute("SELECT * FROM jugadores_seleccion")

	numero_registros_seleccion_jugador=len(conexion.c.fetchall())

	data=extraerDataJugadorSeleccion(jugador)

	data_limpia=limpiarDataJugadorSeleccion(data)

	cargarDataJugadorSeleccion(data_limpia, jugador)

	conexion.c.execute("SELECT * FROM jugadores_seleccion")

	numero_registros_seleccion_jugador_nuevos=len(conexion.c.fetchall())

	assert numero_registros_seleccion_jugador==numero_registros_seleccion_jugador_nuevos