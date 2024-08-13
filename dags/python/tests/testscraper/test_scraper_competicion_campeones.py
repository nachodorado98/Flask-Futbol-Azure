import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_competicion_campeones import ScraperCompeticionCampeones
from src.scrapers.excepciones_scrapers import PaginaError, CompeticionCampeonesError

def test_crear_objeto_scraper_competicion_campeones():

	scraper=ScraperCompeticionCampeones("competicion")

def test_scraper_competicion_campeones_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperCompeticionCampeones("redireccion_competicion")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_competicion_campeones_realizar_peticion(scraper_competicion_campeones):

	contenido=scraper_competicion_campeones._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_competicion_obtener_contenido_campeones(scraper_competicion_campeones):

	contenido=scraper_competicion_campeones._Scraper__realizarPeticion()

	contenido_campeones=scraper_competicion_campeones._ScraperCompeticionCampeones__contenido_campeones(contenido)

	assert contenido_campeones is not None

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_rfef",),("primera_division_argentina",),("champions",)]
)
def test_scraper_competicion_campeones_obtener_campeones_todos_correctos(competicion):

	scraper_competicion_campeones=ScraperCompeticionCampeones(competicion)

	contenido=scraper_competicion_campeones._Scraper__realizarPeticion()

	contenido_campeones=scraper_competicion_campeones._ScraperCompeticionCampeones__contenido_campeones(contenido)

	campeones=scraper_competicion_campeones._ScraperCompeticionCampeones__obtener_campeones(contenido_campeones)

	assert isinstance(campeones, list)
	assert len(campeones)>0
	assert not [None, None] in campeones

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_scraper_competicion_campeones_obtener_data_limpia(competicion):

	scraper_competicion_campeones=ScraperCompeticionCampeones(competicion)

	contenido=scraper_competicion_campeones._Scraper__realizarPeticion()

	contenido_campeones=scraper_competicion_campeones._ScraperCompeticionCampeones__contenido_campeones(contenido)

	data_limpia=scraper_competicion_campeones._ScraperCompeticionCampeones__obtenerDataLimpia(contenido_campeones)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_competicion_campeones_obtener_campeones_competicion_error(endpoint):

	scraper=ScraperCompeticionCampeones(endpoint)

	with pytest.raises(CompeticionCampeonesError):

		scraper.obtenerCampeonesCompeticion()

@pytest.mark.parametrize(["competicion"],
	[("primera",),("segunda",),("premier",),("serie_a",),("escocia",),
	("primera_division_argentina",),("primera_division_rfef",),("champions",)]
)
def test_scraper_competicion_campeones_obtener_campeones_competicion(competicion):

	scraper=ScraperCompeticionCampeones(competicion)

	df_campeones=scraper.obtenerCampeonesCompeticion()

	assert isinstance(df_campeones, pd.DataFrame)