import pytest
import pandas as pd

from src.etl_equipos_liga import extraerDataEquiposLiga, limpiarDataEquiposLiga, cargarDataEquiposLiga
from src.scrapers.excepciones_scrapers import EquiposLigaError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_equipos_liga_error_endpoint(endpoint):

	with pytest.raises(EquiposLigaError):

		extraerDataEquiposLiga(endpoint)

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/1996",),("/primera/2019",), ("bundesliga",),("premier",)]
)
def test_extraer_data_equipos_liga(endpoint):

	data=extraerDataEquiposLiga(endpoint)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/1996",),("/primera/2019",), ("bundesliga",),("premier",)]
)
def test_limpiar_data_equipos_liga(endpoint):

	data=extraerDataEquiposLiga(endpoint)

	data_limpia=limpiarDataEquiposLiga(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==1

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/2019",), ("bundesliga",),("premier",),("/primera/1996",),("/segunda/1990",)]
)
def test_cargar_data_equipos_liga(conexion, endpoint):

	data=extraerDataEquiposLiga(endpoint)

	data_limpia=limpiarDataEquiposLiga(data)

	cargarDataEquiposLiga(data_limpia)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/2019",), ("bundesliga",),("premier",),("/primera/1996",),("/segunda/1990",)]
)
def test_cargar_data_equipos_liga_existentes(conexion, endpoint):

	data=extraerDataEquiposLiga(endpoint)

	data_limpia=limpiarDataEquiposLiga(data)

	cargarDataEquiposLiga(data_limpia)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	data_nueva=extraerDataEquiposLiga(endpoint)

	data_limpia_nueva=limpiarDataEquiposLiga(data_nueva)

	cargarDataEquiposLiga(data_limpia_nueva)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros==numero_registros_nuevos

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/2019",),("bundesliga",),
	("premier",),("/primera/1996",),("/segunda/1990",)]
)
def test_cargar_data_equipos_liga_nuevo_equipo(conexion, endpoint):

	data=extraerDataEquiposLiga(endpoint)

	data_limpia=limpiarDataEquiposLiga(data)

	data_limpia_dropeada=data_limpia.drop(0)

	assert data_limpia.shape[0]>data_limpia_dropeada.shape[0]

	cargarDataEquiposLiga(data_limpia_dropeada)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	data_nueva=extraerDataEquiposLiga(endpoint)

	data_limpia_nueva=limpiarDataEquiposLiga(data_nueva)

	cargarDataEquiposLiga(data_limpia_nueva)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros_nuevos>numero_registros

@pytest.mark.parametrize(["temporada1", "temporada2"],
	[("primera/2019","primera/2020"),("primera/2024","primera/2023"),("premier/2014","premier/2015")]
)
def test_cargar_data_equipos_liga_nueva_temporada(conexion, temporada1, temporada2):

	data=extraerDataEquiposLiga(temporada1)

	data_limpia=limpiarDataEquiposLiga(data)

	cargarDataEquiposLiga(data_limpia)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	data_nueva=extraerDataEquiposLiga(temporada2)

	data_limpia_nueva=limpiarDataEquiposLiga(data_nueva)

	cargarDataEquiposLiga(data_limpia_nueva)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros_nuevos==numero_registros+3