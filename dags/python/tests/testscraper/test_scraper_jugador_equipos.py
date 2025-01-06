import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_jugador_equipos import ScraperJugadorEquipos
from src.scrapers.excepciones_scrapers import PaginaError, JugadorEquiposError

def test_crear_objeto_scraper_jugador_equipos():

	scraper=ScraperJugadorEquipos("jugador")

def test_scraper_jugador_equipos_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperJugadorEquipos("redireccion_equipo")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_jugador_equipos_realizar_peticion(scraper_jugador_equipos):

	contenido=scraper_jugador_equipos._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_jugador_equipos_obtener_contenedor_scroll(scraper_jugador_equipos):

	contenido=scraper_jugador_equipos._Scraper__realizarPeticion()

	contenedor_scroll=scraper_jugador_equipos._ScraperJugadorEquipos__contenido_contenedor_scroll(contenido)

	assert contenedor_scroll is not None

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_equipos_obtener_informacion_equipos(jugador):

	scraper_jugador_equipos=ScraperJugadorEquipos(jugador)

	contenido=scraper_jugador_equipos._Scraper__realizarPeticion()

	contenedor_scroll=scraper_jugador_equipos._ScraperJugadorEquipos__contenido_contenedor_scroll(contenido)

	info_equipos=scraper_jugador_equipos._ScraperJugadorEquipos__informacion_equipos(contenedor_scroll)

	for info in info_equipos:

		assert len(info)==4
		assert info[0].startswith("https://es.besoccer.com/equipo/")
		assert "temp." in info[1]

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_equipos_obtener_data_limpia(jugador):

	scraper_jugador_equipos=ScraperJugadorEquipos(jugador)

	contenido=scraper_jugador_equipos._Scraper__realizarPeticion()

	contenedor_scroll=scraper_jugador_equipos._ScraperJugadorEquipos__contenido_contenedor_scroll(contenido)

	data_limpia=scraper_jugador_equipos._ScraperJugadorEquipos__obtenerDataLimpia(contenedor_scroll)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_jugador_equipos_obtener_jugador_equipos_error(endpoint):

	scraper=ScraperJugadorEquipos(endpoint)

	with pytest.raises(JugadorEquiposError):

		scraper.obtenerJugadorEquipos()

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_equipos_obtener_jugador_equipos(jugador):

	scraper=ScraperJugadorEquipos(jugador)

	df_jugador_equipos=scraper.obtenerJugadorEquipos()

	assert isinstance(df_jugador_equipos, pd.DataFrame)