import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_equipos_liga import ScraperEquiposLiga
from src.scrapers.excepciones_scrapers import PaginaError, EquiposLigaError

def test_crear_objeto_scraper_equipos_liga():

	scraper=ScraperEquiposLiga("/primera/2014")

def test_scraper_equipos_liga_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperEquiposLiga("redireccion_competiciones")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_equipos_liga_realizar_peticion(scraper_equipos_liga):

	contenido=scraper_equipos_liga._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_equipos_liga_obtener_tabla_general(scraper_equipos_liga):

	contenido=scraper_equipos_liga._Scraper__realizarPeticion()

	tabla_general=scraper_equipos_liga._ScraperEquiposLiga__contenido_a_tabla_general(contenido)

	assert tabla_general is not None

def test_scraper_equipos_liga_obtener_tabla_total(scraper_equipos_liga):

	contenido=scraper_equipos_liga._Scraper__realizarPeticion()

	tabla_general=scraper_equipos_liga._ScraperEquiposLiga__contenido_a_tabla_general(contenido)

	tabla_total=scraper_equipos_liga._ScraperEquiposLiga__tabla_general_tabla_total(tabla_general)

	assert tabla_total is not None

def test_scraper_equipos_liga_obtener_tabla(scraper_equipos_liga):

	contenido=scraper_equipos_liga._Scraper__realizarPeticion()

	tabla=scraper_equipos_liga._ScraperEquiposLiga__contenido_a_tabla(contenido)

	assert tabla is not None

def test_scraper_equipos_liga_obtener_columnas_semi_vacias(scraper_equipos_liga):

	contenido=scraper_equipos_liga._Scraper__realizarPeticion()

	tabla=scraper_equipos_liga._ScraperEquiposLiga__contenido_a_tabla(contenido)

	columnas_semi_vacias=scraper_equipos_liga._ScraperEquiposLiga__obtenerColumnasSemiVacias(tabla)

	assert isinstance(columnas_semi_vacias, list)
	assert len(columnas_semi_vacias)==11
	assert columnas_semi_vacias[0]==""
	assert columnas_semi_vacias[1]==""
	assert columnas_semi_vacias[2]==""

def test_scraper_equipos_liga_obtener_columnas(scraper_equipos_liga):

	contenido=scraper_equipos_liga._Scraper__realizarPeticion()

	tabla=scraper_equipos_liga._ScraperEquiposLiga__contenido_a_tabla(contenido)

	columnas=scraper_equipos_liga._ScraperEquiposLiga__obtenerColumnas(tabla)

	assert isinstance(columnas, list)
	assert len(columnas)==11
	assert columnas[0]!=""
	assert columnas[1]!=""
	assert columnas[2]!=""

def test_scraper_equipos_liga_obtener_filas(scraper_equipos_liga):

	contenido=scraper_equipos_liga._Scraper__realizarPeticion()

	tabla=scraper_equipos_liga._ScraperEquiposLiga__contenido_a_tabla(contenido)

	filas=scraper_equipos_liga._ScraperEquiposLiga__obtenerFilas(tabla)

	assert isinstance(filas, list)

def test_scraper_equipos_liga_obtener_contenido_filas(scraper_equipos_liga):

	contenido=scraper_equipos_liga._Scraper__realizarPeticion()

	tabla=scraper_equipos_liga._ScraperEquiposLiga__contenido_a_tabla(contenido)

	filas=scraper_equipos_liga._ScraperEquiposLiga__obtenerFilas(tabla)

	contenido_filas=scraper_equipos_liga._ScraperEquiposLiga__obtenerContenidoFilas(filas)

	assert isinstance(contenido_filas, list)

	for fila in contenido_filas:

		assert len(fila)==12

def test_scraper_equipos_liga_obtener_data_limpia(scraper_equipos_liga):

	contenido=scraper_equipos_liga._Scraper__realizarPeticion()

	tabla=scraper_equipos_liga._ScraperEquiposLiga__contenido_a_tabla(contenido)

	data_limpia=scraper_equipos_liga._ScraperEquiposLiga__obtenerDataLimpia(tabla)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_equipos_liga_obtener_clasificacion_liga_error(endpoint):

	scraper=ScraperEquiposLiga(endpoint)

	with pytest.raises(EquiposLigaError):

		scraper.obtenerClasificacionLiga()

@pytest.mark.parametrize(["endpoint"],
	[("primera/2024",),("segunda/2024",),("/primera/1996",),("/primera/2019",)]
)
def test_scraper_equipos_liga_obtener_clasificacion_liga(endpoint):

	scraper=ScraperEquiposLiga(endpoint)

	df_clasificacion=scraper.obtenerClasificacionLiga()

	assert isinstance(df_clasificacion, pd.DataFrame)