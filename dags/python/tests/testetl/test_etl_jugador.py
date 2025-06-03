import pytest
import pandas as pd

from src.etl_jugador import extraerDataJugador, limpiarDataJugador, cargarDataJugador
from src.scrapers.excepciones_scrapers import JugadorError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_jugador_error_endpoint(endpoint):

	with pytest.raises(JugadorError):

		extraerDataJugador(endpoint)

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_extraer_data_jugador(jugador):

	data=extraerDataJugador(jugador)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_limpiar_data_jugador(jugador):

	data=extraerDataJugador(jugador)

	data_limpia=limpiarDataJugador(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==8
	assert len(data_limpia)==1

def test_cargar_data_jugador_error_no_existe(conexion, entorno):

	data=extraerDataJugador("j-alvarez-772644")

	data_limpia=limpiarDataJugador(data)

	with pytest.raises(Exception):

		cargarDataJugador(data_limpia, "j-alvarez-772644", entorno)

def test_cargar_data_jugador_datos_error(conexion, entorno):

	conexion.insertarJugador("j-alvarez-772644")

	data=extraerDataJugador("j-alvarez-772644")

	data_limpia=limpiarDataJugador(data)

	data_limpia["Valor"]="valor"

	with pytest.raises(Exception):

		cargarDataJugador(data_limpia, "j-alvarez-772644", entorno)

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("c-gallagher-367792",),("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_cargar_data_jugador_datos_correctos_con_equipo(conexion, entorno, jugador):

	conexion.insertarJugador(jugador)

	data=extraerDataJugador(jugador)

	data_limpia=limpiarDataJugador(data)

	cargarDataJugador(data_limpia, jugador, entorno)

	conexion.c.execute(f"SELECT * FROM jugadores WHERE Jugador_Id='{jugador}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert datos_actualizados["equipo_id"] is not None
	assert datos_actualizados["codigo_pais"] is not None
	assert datos_actualizados["codigo_jugador"] is not None
	assert datos_actualizados["puntuacion"] is not None
	assert datos_actualizados["valor"] is not None
	assert datos_actualizados["dorsal"] is not None
	assert datos_actualizados["posicion"] is not None

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["jugador"],
	[("f-torres-29366",),("d-villa-23386",),("f-beckenbauer-321969",)]
)
def test_cargar_data_jugador_datos_correctos_sin_equipo(conexion, entorno, jugador):

	conexion.insertarJugador(jugador)

	data=extraerDataJugador(jugador)

	data_limpia=limpiarDataJugador(data)

	cargarDataJugador(data_limpia, jugador, entorno)

	conexion.c.execute(f"SELECT * FROM jugadores WHERE Jugador_Id='{jugador}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"] is not None
	assert not datos_actualizados["equipo_id"]
	assert datos_actualizados["codigo_pais"] is not None
	assert datos_actualizados["codigo_jugador"] is not None
	assert datos_actualizados["puntuacion"] is not None
	assert not datos_actualizados["valor"]
	assert not datos_actualizados["dorsal"]
	assert datos_actualizados["posicion"] is not None

	conexion.c.execute("SELECT * FROM equipos")

	assert not conexion.c.fetchall()