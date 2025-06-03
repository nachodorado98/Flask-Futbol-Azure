import pytest
import pandas as pd

from src.etl_jugadores import extraerDataJugadoresEquipo, limpiarDataJugadoresEquipo, cargarDataJugadoresEquipo
from src.scrapers.excepciones_scrapers import JugadoresEquipoError

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_extraer_data_jugadores_equipo_error_endpoint(equipo_id, temporada):

	with pytest.raises(JugadoresEquipoError):

		extraerDataJugadoresEquipo(equipo_id, temporada)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971)]
)
def test_extraer_data_jugadores_equipo(equipo_id, temporada):

	data=extraerDataJugadoresEquipo(equipo_id, temporada)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_limpiar_data_jugadores_equipo(equipo_id, temporada):

	data=extraerDataJugadoresEquipo(equipo_id, temporada)

	data_limpia=limpiarDataJugadoresEquipo(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==1

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_cargar_data_jugadores_equipo(conexion, entorno, equipo_id, temporada):

	data=extraerDataJugadoresEquipo(equipo_id, temporada)

	data_limpia=limpiarDataJugadoresEquipo(data)

	cargarDataJugadoresEquipo(data_limpia, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_cargar_data_jugadores_equipo_existentes(conexion, entorno, equipo_id, temporada):

	data=extraerDataJugadoresEquipo(equipo_id, temporada)

	data_limpia=limpiarDataJugadoresEquipo(data)

	cargarDataJugadoresEquipo(data_limpia, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros=len(conexion.c.fetchall())

	data_nueva=extraerDataJugadoresEquipo(equipo_id, temporada)

	data_limpia_nueva=limpiarDataJugadoresEquipo(data_nueva)

	cargarDataJugadoresEquipo(data_limpia_nueva, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros==numero_registros_nuevos

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_cargar_data_jugadores_equipo_nuevo_jugador(conexion, entorno, equipo_id, temporada):

	data=extraerDataJugadoresEquipo(equipo_id, temporada)

	data_limpia=limpiarDataJugadoresEquipo(data)

	data_limpia_dropeada=data_limpia.drop(0)

	assert data_limpia.shape[0]>data_limpia_dropeada.shape[0]

	cargarDataJugadoresEquipo(data_limpia_dropeada, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros=len(conexion.c.fetchall())

	data_nueva=extraerDataJugadoresEquipo(equipo_id, temporada)

	data_limpia_nueva=limpiarDataJugadoresEquipo(data_nueva)

	cargarDataJugadoresEquipo(data_limpia_nueva, entorno)

	conexion.c.execute("SELECT * FROM jugadores")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros_nuevos>numero_registros