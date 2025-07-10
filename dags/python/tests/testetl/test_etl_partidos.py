import pytest
import pandas as pd

from src.etl_partidos import extraerDataPartidosEquipo, limpiarDataPartidosEquipo, cargarDataPartidosEquipo
from src.scrapers.excepciones_scrapers import PartidosEquipoError

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_extraer_data_partidos_equipo_error_endpoint(equipo_id, temporada):

	with pytest.raises(PartidosEquipoError):

		extraerDataPartidosEquipo(equipo_id, temporada)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024),(369, 2025)]
)
def test_extraer_data_partidos_equipo(equipo_id, temporada):

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024),(369, 2025)]
)
def test_limpiar_data_partidos_equipo(equipo_id, temporada):

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	data_limpia=limpiarDataPartidosEquipo(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==8

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024),(369, 2025)]
)
def test_cargar_data_partidos_equipo(conexion, entorno, equipo_id, temporada):

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	data_limpia=limpiarDataPartidosEquipo(data)

	cargarDataPartidosEquipo(data_limpia, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024),(369, 2025)]
)
def test_cargar_data_partidos_equipo_todo_existente(conexion, entorno, equipo_id, temporada):

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	data_limpia=limpiarDataPartidosEquipo(data)

	cargarDataPartidosEquipo(data_limpia, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	equipos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	partidos=conexion.c.fetchall()

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	data_limpia=limpiarDataPartidosEquipo(data)

	cargarDataPartidosEquipo(data_limpia, entorno)

	conexion.c.execute("SELECT * FROM equipos")

	equipos_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM partidos")

	partidos_nuevos=conexion.c.fetchall()

	assert len(equipos)==len(equipos_nuevos)
	assert len(partidos)==len(partidos_nuevos)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971),(2115, 2024),(369, 2025)]
)
def test_cargar_data_partidos_equipo_partido_nuevo(conexion, entorno, equipo_id, temporada):

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	data_limpia=limpiarDataPartidosEquipo(data)
	
	data_limpia_dropeada=data_limpia.drop(0)

	assert data_limpia.shape[0]>data_limpia_dropeada.shape[0]

	cargarDataPartidosEquipo(data_limpia_dropeada, entorno)

	conexion.c.execute("SELECT * FROM partidos")

	partidos=conexion.c.fetchall()

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	data_limpia=limpiarDataPartidosEquipo(data)

	cargarDataPartidosEquipo(data_limpia, entorno)

	conexion.c.execute("SELECT * FROM partidos")

	partidos_nuevos=conexion.c.fetchall()

	assert len(partidos_nuevos)==len(partidos)+1