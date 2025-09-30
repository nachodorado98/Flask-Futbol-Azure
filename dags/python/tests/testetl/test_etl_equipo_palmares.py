import pytest
import pandas as pd

from src.etl_equipo_palmares import extraerDataEquipoPalmares, limpiarDataEquipoPalmares, cargarDataEquipoPalmares
from src.scrapers.excepciones_scrapers import EquipoPalmaresError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_extraer_data_equipo_palmares_error_endpoint(endpoint):

	with pytest.raises(EquipoPalmaresError):

		extraerDataEquipoPalmares(endpoint)

@pytest.mark.parametrize(["equipo"],
	[("cd-valdehornillo-a-senior",),("seleccion-santa-amalia",)]
)
def test_extraer_data_equipo_palmares_error_no_existe(equipo):

	with pytest.raises(EquipoPalmaresError):

		extraerDataEquipoPalmares(equipo)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_extraer_data_equipo_palmares(equipo):

	data=extraerDataEquipoPalmares(equipo)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)>1

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_limpiar_data_equipo_palmares(equipo):

	data=extraerDataEquipoPalmares(equipo)

	data_limpia=limpiarDataEquipoPalmares(data)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data.empty
	assert len(data)==len(data_limpia)
	assert len(data_limpia.columns)==5

def test_cargar_data_equipo_palmares_error_no_existe(conexion, entorno):

	data=extraerDataEquipoPalmares("atletico-madrid")

	data_limpia=limpiarDataEquipoPalmares(data)

	with pytest.raises(Exception):

		cargarDataEquipoPalmares(data_limpia, "atletico-madrid", entorno)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_cargar_data_equipo_palmares_no_competiciones(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	data=extraerDataEquipoPalmares(equipo)

	data_limpia=limpiarDataEquipoPalmares(data)

	cargarDataEquipoPalmares(data_limpia, equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert not conexion.c.fetchall()

	conexion.c.execute("SELECT * FROM equipo_titulo")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_cargar_data_equipo_palmares_no_competicion_logo(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	conexion.insertarCompeticion("primera")

	data=extraerDataEquipoPalmares(equipo)

	data_limpia=limpiarDataEquipoPalmares(data)

	cargarDataEquipoPalmares(data_limpia, equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	assert not conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM equipo_titulo")

	assert not conexion.c.fetchall()

def test_cargar_data_equipo_palmares_datos_error(conexion, entorno):

	conexion.insertarEquipo("atletico-madrid")

	conexion.insertarCompeticion("primera")

	conexion.actualizarDatosCompeticion(["Nombre", "primera-division-ea", "Pais"], "primera")

	data=extraerDataEquipoPalmares("atletico-madrid")

	data_limpia=limpiarDataEquipoPalmares(data)

	data_limpia["Numero"]="numero"

	with pytest.raises(Exception):

		cargarDataEquipoPalmares(data_limpia, "atletico-madrid", entorno)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("barcelona",)]
)
def test_cargar_data_equipo_palmares(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	conexion.insertarCompeticion("primera")

	conexion.actualizarDatosCompeticion(["Nombre", "primera-division-ea", "Pais"], "primera")

	data=extraerDataEquipoPalmares(equipo)

	data_limpia=limpiarDataEquipoPalmares(data)

	cargarDataEquipoPalmares(data_limpia, equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	assert conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	assert conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM equipo_titulo")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("barcelona",)]
)
def test_cargar_data_equipo_palmares_existente(conexion, entorno, equipo):

	conexion.insertarEquipo(equipo)

	conexion.insertarCompeticion("primera")

	conexion.actualizarDatosCompeticion(["Nombre", "primera-division-ea", "Pais"], "primera")

	data=extraerDataEquipoPalmares(equipo)

	data_limpia=limpiarDataEquipoPalmares(data)

	cargarDataEquipoPalmares(data_limpia, equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones=conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	codigo_titulo=conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM equipo_titulo")

	numero_registros_equipo_titulo=conexion.c.fetchall()

	data=extraerDataEquipoPalmares(equipo)

	data_limpia=limpiarDataEquipoPalmares(data)

	cargarDataEquipoPalmares(data_limpia, equipo, entorno)

	conexion.c.execute("SELECT * FROM competiciones")

	numero_registros_competiciones_nuevos=conexion.c.fetchall()

	conexion.c.execute("SELECT Codigo_Titulo FROM competiciones")

	codigo_titulo_nuevo=conexion.c.fetchone()["codigo_titulo"]

	conexion.c.execute("SELECT * FROM equipo_titulo")

	numero_registros_equipo_titulo_nuevos=conexion.c.fetchall()

	assert numero_registros_competiciones==numero_registros_competiciones_nuevos
	assert codigo_titulo==codigo_titulo_nuevo
	assert numero_registros_equipo_titulo==numero_registros_equipo_titulo_nuevos