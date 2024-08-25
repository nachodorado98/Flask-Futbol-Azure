import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_partido_goleadores import ScraperPartidoGoleadores
from src.scrapers.excepciones_scrapers import PaginaError, PartidoGoleadoresError

def test_crear_objeto_scraper_partido_goleadores():

	scraper=ScraperPartidoGoleadores("equipo1", "equipo2", "partido_id")

def test_scraper_partido_goleadores_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperPartidoGoleadores("equipo1", "equipo2", "partido_id")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_partido_goleadores_realizar_peticion(scraper_partido_goleadores):

	contenido=scraper_partido_goleadores._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "alianza-lima", "201313927"),
		("atletico-madrid", "montevideo-wanderers", "2011272699"),
		("atletico-madrid", "bologna", "197915377"),
		("atletico-madrid", "ca-river-plate", "197915379")
	]
)
def test_scraper_partido_goleadores_obtener_contenido_eventos_no_existe(local, visitante, partido_id):

	scraper_partido_goleadores=ScraperPartidoGoleadores(local, visitante, partido_id)

	contenido=scraper_partido_goleadores._Scraper__realizarPeticion()

	with pytest.raises(PartidoGoleadoresError):

		scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_eventos_partido(contenido)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("betis", "atletico-madrid", "202430028"),
		("getafe", "rayo-vallecano", "20256292"),
		("atletico-madrid", "real-sociedad", "202426"),
		("atletico-madrid", "club-brugge", "2023365650"),
		("atletico-madrid", "manchester-city-fc", "2022431041")
	]
)
def test_scraper_partido_goleadores_obtener_contenido_goleadores_no_hay(local, visitante, partido_id):

	scraper_partido_goleadores=ScraperPartidoGoleadores(local, visitante, partido_id)

	contenido=scraper_partido_goleadores._Scraper__realizarPeticion()

	contenido_eventos=scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_eventos_partido(contenido)

	with pytest.raises(PartidoGoleadoresError):

		scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_goleadores_partido(contenido_eventos)

def test_scraper_partido_goleadores_obtener_contenido_goleadores(scraper_partido_goleadores):

	contenido=scraper_partido_goleadores._Scraper__realizarPeticion()

	contenido_eventos=scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_eventos_partido(contenido)

	contenido_goleadores=scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_goleadores_partido(contenido_eventos)

	assert contenido_goleadores is not None

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_scraper_partido_goleadores_obtener_lista_goleadores(local, visitante, partido_id):

	scraper_partido_goleadores=ScraperPartidoGoleadores(local, visitante, partido_id)

	contenido=scraper_partido_goleadores._Scraper__realizarPeticion()

	contenido_eventos=scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_eventos_partido(contenido)

	contenido_goleadores=scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_goleadores_partido(contenido_eventos)

	lista_goleadores=scraper_partido_goleadores._ScraperPartidoGoleadores__obtener_lista_goleadores(contenido_goleadores)

	assert len(lista_goleadores)>0

	for goleador in lista_goleadores:

		assert len(goleador)==3

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("betis", "atletico-madrid", "202430028"),
		("getafe", "rayo-vallecano", "20256292"),
		("atletico-madrid", "real-sociedad", "202426"),
		("atletico-madrid", "club-brugge", "2023365650"),
		("atletico-madrid", "manchester-city-fc", "2022431041")
	]
)
def test_scraper_partido_goleadores_obtener_goleadores_no_hay(local, visitante, partido_id):

	scraper_partido_goleadores=ScraperPartidoGoleadores(local, visitante, partido_id)

	contenido=scraper_partido_goleadores._Scraper__realizarPeticion()

	contenido_eventos=scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_eventos_partido(contenido)

	with pytest.raises(PartidoGoleadoresError):

		scraper_partido_goleadores._ScraperPartidoGoleadores__goleadores(contenido_eventos)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_scraper_partido_goleadores_obtener_goleadores(local, visitante, partido_id):

	scraper_partido_goleadores=ScraperPartidoGoleadores(local, visitante, partido_id)

	contenido=scraper_partido_goleadores._Scraper__realizarPeticion()

	contenido_eventos=scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_eventos_partido(contenido)

	goleadores=scraper_partido_goleadores._ScraperPartidoGoleadores__goleadores(contenido_eventos)

	assert len(goleadores)>0

	for goleador in goleadores:

		assert len(goleador)==3

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_scraper_partido_goleadores_obtener_data_limpia(local, visitante, partido_id):

	scraper_partido_goleadores=ScraperPartidoGoleadores(local, visitante, partido_id)

	contenido=scraper_partido_goleadores._Scraper__realizarPeticion()

	contenido_eventos=scraper_partido_goleadores._ScraperPartidoGoleadores__contenido_eventos_partido(contenido)

	data_limpia=scraper_partido_goleadores._ScraperPartidoGoleadores__obtenerDataLimpia(contenido_eventos)

	assert isinstance(data_limpia, pd.DataFrame)

def test_scraper_partido_goleadores_obtener_partido_goleadores_error():

	scraper=ScraperPartidoGoleadores("equipo1", "equipo2", "partido_id")

	with pytest.raises(PartidoGoleadoresError):

		scraper.obtenerPartidoGoleadores()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "alianza-lima", "201313927"),
		("atletico-madrid", "montevideo-wanderers", "2011272699"),
		("atletico-madrid", "bologna", "197915377"),
		("atletico-madrid", "ca-river-plate", "197915379")
	]
)
def test_scraper_partido_goleadores_obtener_partido_goleadores_no_existe(local, visitante, partido_id):

	scraper=ScraperPartidoGoleadores(local, visitante, partido_id)

	with pytest.raises(PartidoGoleadoresError):

		scraper.obtenerPartidoGoleadores()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("betis", "atletico-madrid", "202430028"),
		("getafe", "rayo-vallecano", "20256292"),
		("atletico-madrid", "real-sociedad", "202426"),
		("atletico-madrid", "club-brugge", "2023365650"),
		("atletico-madrid", "manchester-city-fc", "2022431041")
	]
)
def test_scraper_partido_goleadores_obtener_partido_goleadores_no_hay(local, visitante, partido_id):

	scraper=ScraperPartidoGoleadores(local, visitante, partido_id)

	with pytest.raises(PartidoGoleadoresError):

		scraper.obtenerPartidoGoleadores()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "real-madrid", "2024664923"),
		("rayo-vallecano", "atletico-madrid", "202430031"),
		("celtic-fc", "atletico-madrid", "2024555815"),
		("feyenoord", "atletico-madrid", "2024555825"),
		("atletico-madrid", "internazionale", "2024645009")
	]
)
def test_scraper_partido_goleadores_obtener_partido_goleadores(local, visitante, partido_id):

	scraper=ScraperPartidoGoleadores(local, visitante, partido_id)

	df_partido_goleadores=scraper.obtenerPartidoGoleadores()

	assert isinstance(df_partido_goleadores, pd.DataFrame)