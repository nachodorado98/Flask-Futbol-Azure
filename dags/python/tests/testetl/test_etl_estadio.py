import pytest
import pandas as pd

from src.etl_estadio import extraerDataEstadio, limpiarDataEstadio, cargarDataEstadio
from src.scrapers.excepciones_scrapers import EstadioError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_estadio_error_endpoint(endpoint):

	with pytest.raises(EstadioError):

		extraerDataEstadio(endpoint)

@pytest.mark.parametrize(["estadio"],
	[("riyadh-air-metropolitano-23",),("municipal-football-santa-amalia-4902",),("celtic-park-82",),("stadion-feijenoord-71",)]
)
def test_extraer_data_estadio(estadio):

	data=extraerDataEstadio(estadio)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["estadio"],
	[("riyadh-air-metropolitano-23",),("municipal-football-santa-amalia-4902",),("celtic-park-82",),("stadion-feijenoord-71",)]
)
def test_limpiar_data_estadio(estadio):

	data=extraerDataEstadio(estadio)

	data_limpia=limpiarDataEstadio(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==2
	assert len(data_limpia)==1

def test_cargar_data_estadio_error_no_existe(conexion):

	data=extraerDataEstadio("riyadh-air-metropolitano-23")

	data_limpia=limpiarDataEstadio(data)

	with pytest.raises(Exception):

		cargarDataEstadio(data_limpia, "riyadh-air-metropolitano-23")

def test_cargar_data_estadio_datos_error(conexion):

	estadio=["riyadh-air-metropolitano-23", 1, "Metropolitano", "Metropo",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	data=extraerDataEstadio("riyadh-air-metropolitano-23")

	data_limpia=limpiarDataEstadio(data)

	data_limpia["Codigo_Pais"]="codigo_pais"

	with pytest.raises(Exception):

		cargarDataEstadio(data_limpia, "riyadh-air-metropolitano-23")

@pytest.mark.parametrize(["estadio_id"],
	[("riyadh-air-metropolitano-23",),("municipal-football-santa-amalia-4902",),("celtic-park-82",),("stadion-feijenoord-71",)]
)
def test_cargar_data_estadio_datos_correctos_con_equipo(conexion, estadio_id):

	estadio=[estadio_id, 1, "Metropolitano", "Metropo", 40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	data=extraerDataEstadio(estadio_id)

	data_limpia=limpiarDataEstadio(data)

	cargarDataEstadio(data_limpia, estadio_id)

	conexion.c.execute(f"SELECT * FROM estadios WHERE Estadio_Id='{estadio_id}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["pais"] is not None
	assert datos_actualizados["codigo_pais"] is not None