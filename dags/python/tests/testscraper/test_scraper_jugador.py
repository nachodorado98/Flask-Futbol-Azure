import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_jugador import ScraperJugador
from src.scrapers.excepciones_scrapers import PaginaError, JugadorError

def test_crear_objeto_scraper_jugador():

	scraper=ScraperJugador("jugador")

def test_scraper_jugador_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperJugador("redireccion_equipo")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_jugador_realizar_peticion(scraper_jugador):

	contenido=scraper_jugador._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_jugador_obtener_cabecera(scraper_jugador):

	contenido=scraper_jugador._Scraper__realizarPeticion()

	cabecera=scraper_jugador._ScraperJugador__contenido_cabecera(contenido)

	assert cabecera is not None

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_obtener_informacion_nombre(jugador):

	scraper_jugador=ScraperJugador(jugador)

	contenido=scraper_jugador._Scraper__realizarPeticion()

	cabecera=scraper_jugador._ScraperJugador__contenido_cabecera(contenido)

	nombre=scraper_jugador._ScraperJugador__informacion_nombre(cabecera)

	assert nombre is not ""

@pytest.mark.parametrize(["jugador"],
	[("f-torres-29366",),("d-villa-23386",)]
)
def test_scraper_jugador_obtener_informacion_general_sin_equipo(jugador):

	scraper_jugador=ScraperJugador(jugador)

	contenido=scraper_jugador._Scraper__realizarPeticion()

	cabecera=scraper_jugador._ScraperJugador__contenido_cabecera(contenido)

	datos=scraper_jugador._ScraperJugador__informacion_general(contenido)

	assert len(datos)==8

	assert datos[0]==""

	assert datos[1].endswith(".png") or datos[1].endswith(".jpg")
	assert datos[1].startswith("https://cdn.resfu.com/media/img/flags")

	assert datos[2].endswith(".png") or datos[2].endswith(".jpg")
	assert datos[2].startswith("https://cdn.resfu.com/img_data/players/medium")

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_obtener_informacion_general_con_equipo(jugador):

	scraper_jugador=ScraperJugador(jugador)

	contenido=scraper_jugador._Scraper__realizarPeticion()

	cabecera=scraper_jugador._ScraperJugador__contenido_cabecera(contenido)

	datos=scraper_jugador._ScraperJugador__informacion_general(contenido)

	assert len(datos)==8

	assert datos[0].startswith("https://es.besoccer.com/equipo/")

	assert datos[1].endswith(".png") or datos[1].endswith(".jpg")
	assert datos[1].startswith("https://cdn.resfu.com/media/img/flags")

	assert datos[2].endswith(".png") or datos[2].endswith(".jpg")
	assert datos[2].startswith("https://cdn.resfu.com/img_data/players/medium")

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_obtener_data_limpia(jugador):

	scraper_jugador=ScraperJugador(jugador)

	contenido=scraper_jugador._Scraper__realizarPeticion()

	cabecera=scraper_jugador._ScraperJugador__contenido_cabecera(contenido)

	data_limpia=scraper_jugador._ScraperJugador__obtenerDataLimpia(cabecera)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_jugador_obtener_jugador_error(endpoint):

	scraper=ScraperJugador(endpoint)

	with pytest.raises(JugadorError):

		scraper.obtenerJugador()

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_obtener_jugador(jugador):

	scraper=ScraperJugador(jugador)

	df_jugador=scraper.obtenerJugador()

	assert isinstance(df_jugador, pd.DataFrame)