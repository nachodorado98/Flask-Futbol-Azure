import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_partido_competicion import ScraperPartidoCompeticion
from src.scrapers.excepciones_scrapers import PaginaError, PartidoCompeticionError

def test_crear_objeto_scraper_partido_competicion():

	scraper=ScraperPartidoCompeticion("equipo1", "equipo2", "partido_id")

def test_scraper_partido_competicion_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperPartidoCompeticion("equipo1", "equipo2", "partido_id")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_partido_competicion_realizar_peticion(scraper_partido_competicion):

	contenido=scraper_partido_competicion._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_partido_competicion_obtener_contenido_competicion(scraper_partido_competicion):

	contenido=scraper_partido_competicion._Scraper__realizarPeticion()

	contenido_competicion=scraper_partido_competicion._ScraperPartidoCompeticion__contenido_competicion(contenido)

	assert contenido_competicion is not None

def test_scraper_partido_competicion_obtener_competicion_partido(scraper_partido_competicion):

	contenido=scraper_partido_competicion._Scraper__realizarPeticion()

	contenido_competicion=scraper_partido_competicion._ScraperPartidoCompeticion__contenido_competicion(contenido)

	competicion=scraper_partido_competicion._ScraperPartidoCompeticion__competicion_partido(contenido_competicion)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "202429286"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_scraper_partido_competicion_obtener_data_limpia(local, visitante, partido_id):

	scraper_partido_competicion=ScraperPartidoCompeticion(local, visitante, partido_id)

	contenido=scraper_partido_competicion._Scraper__realizarPeticion()

	contenido_competicion=scraper_partido_competicion._ScraperPartidoCompeticion__contenido_competicion(contenido)

	data_limpia=scraper_partido_competicion._ScraperPartidoCompeticion__obtenerDataLimpia(contenido_competicion)

	assert isinstance(data_limpia, pd.DataFrame)

def test_scraper_partido_competicion_obtener_partido_competicion_error():

	scraper=ScraperPartidoCompeticion("equipo1", "equipo2", "partido_id")

	with pytest.raises(PartidoCompeticionError):

		scraper.obtenerPartidoCompeticion()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "202429286"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_scraper_partido_competicion_obtener_partido_competicion(local, visitante, partido_id):

	scraper=ScraperPartidoCompeticion(local, visitante, partido_id)

	df_partido_competicion=scraper.obtenerPartidoCompeticion()

	assert isinstance(df_partido_competicion, pd.DataFrame)