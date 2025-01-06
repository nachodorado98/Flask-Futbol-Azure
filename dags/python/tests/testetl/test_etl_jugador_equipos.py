import pytest
import pandas as pd

from src.etl_jugador_equipos import extraerDataJugadorEquipos, limpiarDataJugadorEquipos, cargarDataJugadorEquipos
from src.scrapers.excepciones_scrapers import JugadorEquiposError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_jugador_equipos_error_endpoint(endpoint):

	with pytest.raises(JugadorEquiposError):

		extraerDataJugadorEquipos(endpoint)

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_extraer_data_jugador_equipos(jugador):

	data=extraerDataJugadorEquipos(jugador)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data.columns)==4

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_limpiar_data_jugador_equipos(jugador):

	data=extraerDataJugadorEquipos(jugador)

	data_limpia=limpiarDataJugadorEquipos(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==4

def test_cargar_data_jugador_equipos_error_no_existe(conexion):

	data=extraerDataJugadorEquipos("j-alvarez-772644")

	data_limpia=limpiarDataJugadorEquipos(data)

	with pytest.raises(Exception):

		cargarDataJugadorEquipos(data_limpia, "j-alvarez-772644")

def test_cargar_data_jugador_equipos_datos_error(conexion):

	conexion.insertarJugador("j-alvarez-772644")

	data=extraerDataJugadorEquipos("j-alvarez-772644")

	data_limpia=limpiarDataJugadorEquipos(data)

	data_limpia["Goles"]="gol"

	with pytest.raises(Exception):

		cargarDataJugadorEquipos(data_limpia, "j-alvarez-772644")

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_cargar_data_jugador_equipos(conexion, jugador):

	conexion.insertarJugador(jugador)

	data=extraerDataJugadorEquipos(jugador)

	data_limpia=limpiarDataJugadorEquipos(data)

	cargarDataJugadorEquipos(data_limpia, jugador)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM jugadores_equipo")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_cargar_data_jugador_equipos_equipos_existente(conexion, jugador):

	conexion.insertarJugador(jugador)

	data=extraerDataJugadorEquipos(jugador)

	data_limpia=limpiarDataJugadorEquipos(data)

	cargarDataJugadorEquipos(data_limpia, jugador)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_equipos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM jugadores_equipo")

	numero_registros_equipos_jugador=len(conexion.c.fetchall())

	data=extraerDataJugadorEquipos(jugador)

	data_limpia=limpiarDataJugadorEquipos(data)

	cargarDataJugadorEquipos(data_limpia, jugador)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_equipos_nuevos=len(conexion.c.fetchall())

	conexion.c.execute("SELECT * FROM jugadores_equipo")

	numero_registros_equipos_jugador_nuevos=len(conexion.c.fetchall())

	assert numero_registros_equipos==numero_registros_equipos_nuevos
	assert numero_registros_equipos_jugador==numero_registros_equipos_jugador_nuevos