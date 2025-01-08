import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_jugador_seleccion import ScraperJugadorSeleccion
from src.scrapers.excepciones_scrapers import PaginaError, JugadorSeleccionError

def test_crear_objeto_scraper_jugador_seleccion():

	scraper=ScraperJugadorSeleccion("jugador")

def test_scraper_jugador_seleccion_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperJugadorSeleccion("redireccion_equipo")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_jugador_seleccion_realizar_peticion(scraper_jugador_seleccion):

	contenido=scraper_jugador_seleccion._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_jugador_seleccion_obtener_contenedor_seleccion(scraper_jugador_seleccion):

	contenido=scraper_jugador_seleccion._Scraper__realizarPeticion()

	contenedor_seleccion=scraper_jugador_seleccion._ScraperJugadorSeleccion__contenido_contenedor_seleccion(contenido)

	assert contenedor_seleccion is not None

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_seleccion_obtener_informacion_basica(jugador):

	scraper_jugador_seleccion=ScraperJugadorSeleccion(jugador)

	contenido=scraper_jugador_seleccion._Scraper__realizarPeticion()

	contenedor_seleccion=scraper_jugador_seleccion._ScraperJugadorSeleccion__contenido_contenedor_seleccion(contenido)

	informacion_basica=scraper_jugador_seleccion._ScraperJugadorSeleccion__informacion_basica(contenedor_seleccion)

	assert len(informacion_basica)==2
	assert informacion_basica[0].startswith("https://cdn.resfu.com/img_data/equipos/")
	assert "veces en internacional absoluto" in informacion_basica[1]

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_seleccion_obtener_informacion_stats(jugador):

	scraper_jugador_seleccion=ScraperJugadorSeleccion(jugador)

	contenido=scraper_jugador_seleccion._Scraper__realizarPeticion()

	contenedor_seleccion=scraper_jugador_seleccion._ScraperJugadorSeleccion__contenido_contenedor_seleccion(contenido)

	informacion_stats=scraper_jugador_seleccion._ScraperJugadorSeleccion__informacion_stats(contenedor_seleccion)

	assert len(informacion_stats)==5
	assert None not in informacion_stats

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_seleccion_obtener_data_limpia(jugador):

	scraper_jugador_seleccion=ScraperJugadorSeleccion(jugador)

	contenido=scraper_jugador_seleccion._Scraper__realizarPeticion()

	contenedor_seleccion=scraper_jugador_seleccion._ScraperJugadorSeleccion__contenido_contenedor_seleccion(contenido)

	data_limpia=scraper_jugador_seleccion._ScraperJugadorSeleccion__obtenerDataLimpia(contenedor_seleccion)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_jugador_seleccion_obtener_jugador_seleccion_error(endpoint):

	scraper=ScraperJugadorSeleccion(endpoint)

	with pytest.raises(JugadorSeleccionError):

		scraper.obtenerJugadorSeleccion()

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_scraper_jugador_seleccion_obtener_jugador_seleccion(jugador):

	scraper=ScraperJugadorSeleccion(jugador)

	df_jugador_seleccion=scraper.obtenerJugadorSeleccion()

	assert isinstance(df_jugador_seleccion, pd.DataFrame)