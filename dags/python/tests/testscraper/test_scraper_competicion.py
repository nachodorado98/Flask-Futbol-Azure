import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_competicion import ScraperCompeticion
from src.scrapers.excepciones_scrapers import PaginaError, CompeticionError

def test_crear_objeto_scraper_competicion():

	scraper=ScraperCompeticion("competicion")

def test_scraper_competicion_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperCompeticion("redireccion_competicion")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_competicion_realizar_peticion(scraper_competicion):

	contenido=scraper_competicion._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_competicion_obtener_cabecera(scraper_competicion):

	contenido=scraper_competicion._Scraper__realizarPeticion()

	cabecera=scraper_competicion._ScraperCompeticion__contenido_cabecera(contenido)

	assert cabecera is not None

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),("primera_division_argentina",),("primera_division_rfef",)]
)
def test_scraper_competicion_obtener_informacion_nombre(competicion):

	scraper_competicion=ScraperCompeticion(competicion)

	contenido=scraper_competicion._Scraper__realizarPeticion()

	cabecera=scraper_competicion._ScraperCompeticion__contenido_cabecera(contenido)

	nombre=scraper_competicion._ScraperCompeticion__informacion_nombre(cabecera)

	assert nombre is not ""

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),("primera_division_argentina",),("primera_division_rfef",)]
)
def test_scraper_competicion_obtener_informacion_logo_pais(competicion):

	scraper_competicion=ScraperCompeticion(competicion)

	contenido=scraper_competicion._Scraper__realizarPeticion()

	cabecera=scraper_competicion._ScraperCompeticion__contenido_cabecera(contenido)

	imagen_logo, imagen_pais=scraper_competicion._ScraperCompeticion__informacion_logo_pais(cabecera)

	assert imagen_logo.endswith(".png") or imagen_logo.endswith(".jpg")
	assert imagen_logo.startswith("https://cdn.resfu.com/media/img/league_logos/")

	assert imagen_pais.endswith(".png") or imagen_pais.endswith(".jpg")
	assert imagen_pais.startswith("https://cdn.resfu.com/media/img/flags")

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),("primera_division_argentina",),("primera_division_rfef",)]
)
def test_scraper_competicion_obtener_data_limpia(competicion):

	scraper_competicion=ScraperCompeticion(competicion)

	contenido=scraper_competicion._Scraper__realizarPeticion()

	cabecera=scraper_competicion._ScraperCompeticion__contenido_cabecera(contenido)

	data_limpia=scraper_competicion._ScraperCompeticion__obtenerDataLimpia(cabecera)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_competicion_obtener_competicion_error(endpoint):

	scraper=ScraperCompeticion(endpoint)

	with pytest.raises(CompeticionError):

		scraper.obtenerCompeticion()

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),("primera_division_argentina",),("primera_division_rfef",)]
)
def test_scraper_competicion_obtener_competicion(competicion):

	scraper=ScraperCompeticion(competicion)

	df_competicion=scraper.obtenerCompeticion()

	assert isinstance(df_competicion, pd.DataFrame)