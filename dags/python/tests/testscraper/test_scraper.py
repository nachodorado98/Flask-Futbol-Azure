import pytest
from bs4 import BeautifulSoup as bs4

from src.scrapers.scraper import Scraper
from src.scrapers.excepciones_scrapers import PaginaError

def test_crear_objeto_scraper():

	scraper=Scraper("endpoint")

def test_scraper_realizar_peticion_error(scraper):

	scraper=Scraper("/endpoint")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_realizar_peticion(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)