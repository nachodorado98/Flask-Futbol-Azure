import pytest
import pandas as pd

from src.scrapers.scraper_jugadores import ScraperJugadores
from src.scrapers.excepciones_scrapers import PaginaError, JugadoresEquipoError

def test_crear_objeto_scraper_jugadores():

	scraper=ScraperJugadores(13, 22)

def test_scraper_jugadores_realizar_peticion_error_json():

	scraper=ScraperJugadores("equipo", 2023)

	with pytest.raises(PaginaError):

		scraper._ScraperJugadores__realizarPeticion()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024)]
)
def test_scraper_jugadores_realizar_peticion_error_sin_contenido(equipo_id, temporada):

	scraper=ScraperJugadores(equipo_id, temporada)

	with pytest.raises(PaginaError):

		scraper._ScraperJugadores__realizarPeticion()

def test_scraper_jugadores_realizar_peticion(scraper_jugadores):

	contenido=scraper_jugadores._ScraperJugadores__realizarPeticion()

	assert isinstance(contenido, list)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000)]
)
def test_scraper_jugadores_obtener_data_limpia(equipo_id, temporada):

	scraper_jugadores=ScraperJugadores(equipo_id, temporada)

	contenido=scraper_jugadores._ScraperJugadores__realizarPeticion()

	data_limpia=scraper_jugadores._ScraperJugadores__obtenerDataLimpia(contenido)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_scraper_jugadores_obtener_jugadores_equipo_error(equipo_id, temporada):

	scraper=ScraperJugadores(equipo_id, temporada)

	with pytest.raises(JugadoresEquipoError):

		scraper.obtenerJugadoresEquipo()

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971)]
)
def test_scraper_jugadores_obtener_jugadores_equipo(equipo_id, temporada):

	scraper=ScraperJugadores(equipo_id, temporada)

	df_jugadores=scraper.obtenerJugadoresEquipo()

	assert isinstance(df_jugadores, pd.DataFrame)