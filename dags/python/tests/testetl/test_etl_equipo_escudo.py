import pytest
import pandas as pd

from src.etl_equipo_escudo import extraerDataEquipoEscudo, limpiarDataEquipoEscudo, cargarDataEquipoEscudo
from src.scrapers.excepciones_scrapers import EquipoEscudoError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_escudo_error_endpoint(endpoint):

	with pytest.raises(EquipoEscudoError):

		extraerDataEquipoEscudo(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),
	("kakamega-homeboyz",),("cd-valdehornillo-a-senior",),("seleccion-santa-amalia",)]
)
def test_extraer_data_equipo_escudo(equipo):

	data=extraerDataEquipoEscudo(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),
	("kakamega-homeboyz",),("cd-valdehornillo-a-senior",),("seleccion-santa-amalia",)]
)
def test_limpiar_data_equipo_escudo(equipo):

	data=extraerDataEquipoEscudo(equipo)

	data_limpia=limpiarDataEquipoEscudo(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia.empty
	assert len(data_limpia.columns)==2
	assert len(data_limpia)==1

def test_cargar_data_equipo_escudo_error_no_existe(conexion):

	data=extraerDataEquipoEscudo("atletico-madrid")

	data_limpia=limpiarDataEquipoEscudo(data)

	with pytest.raises(Exception):

		cargarDataEquipoEscudo(data_limpia, "atletico-madrid")

def test_cargar_data_equipo_escudo_datos_error(conexion):

	conexion.insertarEquipo("atletico-madrid")

	data=extraerDataEquipoEscudo("atletico-madrid")

	data_limpia=limpiarDataEquipoEscudo(data)

	data_limpia["Escudo"]="numero"

	with pytest.raises(Exception):

		cargarDataEquipoEscudo(data_limpia, "atletico-madrid")

@pytest.mark.parametrize(["nombre_equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",), ("racing",),
	("atalanta",),("manchester-city-fc",)]
)
def test_cargar_data_equipo_escudo_datos_correctos(conexion, nombre_equipo):

	conexion.insertarEquipo(nombre_equipo)

	data=extraerDataEquipoEscudo(nombre_equipo)

	data_limpia=limpiarDataEquipoEscudo(data)

	cargarDataEquipoEscudo(data_limpia, nombre_equipo)

	conexion.c.execute(f"SELECT * FROM equipos WHERE Equipo_Id='{nombre_equipo}'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["escudo"] is not None
	assert datos_actualizados["puntuacion"] is not None