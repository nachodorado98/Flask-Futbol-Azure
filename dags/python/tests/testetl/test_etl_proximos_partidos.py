import pytest
import pandas as pd

from src.etl_proximos_partidos import extraerDataProximosPartidosEquipo, limpiarDataProximosPartidosEquipo, cargarDataProximosPartidosEquipo
from src.scrapers.excepciones_scrapers import PartidosEquipoError

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_extraer_data_proximos_partidos_equipo_error_endpoint(equipo_id, temporada):

	with pytest.raises(PartidosEquipoError):

		extraerDataProximosPartidosEquipo(equipo_id, temporada)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971)]
)
def test_extraer_data_proximos_partidos_equipo(equipo_id, temporada):

	data=extraerDataProximosPartidosEquipo(equipo_id, temporada)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_limpiar_data_proximos_partidos_equipo_no_hay(equipo_id, temporada):

	data=extraerDataProximosPartidosEquipo(equipo_id, temporada)

	with pytest.raises(Exception):

		limpiarDataProximosPartidosEquipo(data)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_limpiar_data_proximos_partidos_equipo(equipo_id, temporada):

	data=extraerDataProximosPartidosEquipo(equipo_id, temporada)

	data["Estado"]=-1

	data_limpia=limpiarDataProximosPartidosEquipo(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==6

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_cargar_data_proximos_partidos_equipo(conexion, equipo_id, temporada):

	data=extraerDataProximosPartidosEquipo(equipo_id, temporada)

	data["Estado"]=-1

	data_limpia=limpiarDataProximosPartidosEquipo(data)

	cargarDataProximosPartidosEquipo(data_limpia)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_cargar_data_proximos_partidos_equipo_todo_existente(conexion, equipo_id, temporada):

	data=extraerDataProximosPartidosEquipo(equipo_id, temporada)

	data["Estado"]=-1

	data_limpia=limpiarDataProximosPartidosEquipo(data)

	cargarDataProximosPartidosEquipo(data_limpia)

	conexion.c.execute("SELECT * FROM equipos")

	equipos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos=conexion.c.fetchall()

	data=extraerDataProximosPartidosEquipo(equipo_id, temporada)

	data["Estado"]=-1

	data_limpia=limpiarDataProximosPartidosEquipo(data)

	cargarDataProximosPartidosEquipo(data_limpia)

	conexion.c.execute("SELECT * FROM equipos")

	equipos_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos_nuevos=conexion.c.fetchall()

	assert len(equipos)==len(equipos_nuevos)
	assert len(proximos_partidos)==len(proximos_partidos_nuevos)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024)]
)
def test_cargar_data_proximos_partidos_equipo_partido_nuevo(conexion, equipo_id, temporada):

	data=extraerDataProximosPartidosEquipo(equipo_id, temporada)

	data["Estado"]=-1

	data_limpia=limpiarDataProximosPartidosEquipo(data)

	data_limpia_dropeada=data_limpia.drop(0)

	assert data_limpia.shape[0]>data_limpia_dropeada.shape[0]

	cargarDataProximosPartidosEquipo(data_limpia_dropeada)

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos=conexion.c.fetchall()

	data=extraerDataProximosPartidosEquipo(equipo_id, temporada)

	data["Estado"]=-1

	data_limpia=limpiarDataProximosPartidosEquipo(data)

	cargarDataProximosPartidosEquipo(data_limpia)

	conexion.c.execute("SELECT * FROM proximos_partidos")

	proximos_partidos_nuevos=conexion.c.fetchall()

	assert len(proximos_partidos_nuevos)==len(proximos_partidos)+1