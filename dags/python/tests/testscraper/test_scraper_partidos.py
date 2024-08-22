import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_partidos import ScraperPartidos
from src.scrapers.excepciones_scrapers import PaginaError, PartidosEquipoError

def test_crear_objeto_scraper_partidos():

	scraper=ScraperPartidos(13, 22)

def test_scraper_partidos_realizar_peticion_error_json():

	scraper=ScraperPartidos("equipo", 2023)

	with pytest.raises(PaginaError):

		scraper._ScraperPartidos__realizarPeticion()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024)]
)
def test_scraper_partidos_realizar_peticion_error_sin_contenido(equipo_id, temporada):

	scraper=ScraperPartidos(equipo_id, temporada)

	with pytest.raises(PaginaError):

		scraper._ScraperPartidos__realizarPeticion()

def test_scraper_partidos_realizar_peticion(scraper_partidos):

	contenido=scraper_partidos._ScraperPartidos__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_partidos_obtener_paneles(scraper_partidos):

	contenido=scraper_partidos._ScraperPartidos__realizarPeticion()

	paneles=scraper_partidos._ScraperPartidos__obtenerPaneles(contenido)

	assert paneles

def test_scraper_partidos_obtener_partidos_panel(scraper_partidos):

	contenido=scraper_partidos._ScraperPartidos__realizarPeticion()

	paneles=scraper_partidos._ScraperPartidos__obtenerPaneles(contenido)

	for panel in paneles:

		partidos_panel=scraper_partidos._ScraperPartidos__obtenerPartidosPanel(panel)

		for partido_panel in partidos_panel:

			assert len(partido_panel)==9
			assert partido_panel[0].startswith("match-")
			assert partido_panel[1].startswith("https://es.besoccer.com/partido/")

def test_scraper_partidos_obtener_partidos(scraper_partidos):

	contenido=scraper_partidos._ScraperPartidos__realizarPeticion()

	paneles=scraper_partidos._ScraperPartidos__obtenerPaneles(contenido)

	partidos=scraper_partidos._ScraperPartidos__obtenerPartidos(paneles)

	for partido in partidos:

		assert len(partido)==9

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000)]
)
def test_scraper_partidos_obtener_data_limpia(equipo_id, temporada):

	scraper_partidos=ScraperPartidos(equipo_id, temporada)

	contenido=scraper_partidos._ScraperPartidos__realizarPeticion()

	paneles=scraper_partidos._ScraperPartidos__obtenerPaneles(contenido)

	data_limpia=scraper_partidos._ScraperPartidos__obtenerDataLimpia(paneles)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_scraper_partidos_obtener_partidos_equipo_error(equipo_id, temporada):

	scraper=ScraperPartidos(equipo_id, temporada)

	with pytest.raises(PartidosEquipoError):

		scraper.obtenerPartidosEquipo()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971)]
)
def test_scraper_partidos_obtener_partidos_equipo(equipo_id, temporada):

	scraper=ScraperPartidos(equipo_id, temporada)

	df_partidos=scraper.obtenerPartidosEquipo()

	assert isinstance(df_partidos, pd.DataFrame)