import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest

from src.scrapers.scraper import Scraper
from src.scrapers.scraper_equipos_liga import ScraperEquiposLiga
from src.scrapers.scraper_equipo import ScraperEquipo
from src.scrapers.scraper_equipo_estadio import ScraperEquipoEstadio
from src.scrapers.scraper_equipo_entrenador import ScraperEquipoEntrenador
from src.scrapers.scraper_equipo_escudo import ScraperEquipoEscudo
from src.scrapers.scraper_partidos import ScraperPartidos
from src.scrapers.configscrapers import ENDPOINT_COMPETICION

from src.database.conexion import Conexion

from src.datalake.conexion_data_lake import ConexionDataLake

@pytest.fixture
def scraper():

	return Scraper(f"{ENDPOINT_COMPETICION}/primera")

@pytest.fixture
def scraper_equipos_liga():

	return ScraperEquiposLiga("primera")

@pytest.fixture
def scraper_equipo():

	return ScraperEquipo("atletico-madrid")

@pytest.fixture
def scraper_equipo_estadio():

	return ScraperEquipoEstadio("atletico-madrid")

@pytest.fixture
def scraper_equipo_entrenador():

	return ScraperEquipoEntrenador("atletico-madrid")

@pytest.fixture
def scraper_equipo_escudo():

	return ScraperEquipoEscudo("atletico-madrid")

@pytest.fixture()
def conexion():

	con=Conexion()

	con.c.execute("DELETE FROM equipos")

	con.c.execute("DELETE FROM estadios")

	con.c.execute("DELETE FROM partidos")

	con.confirmar()

	return con

@pytest.fixture()
def datalake():

    return ConexionDataLake()

@pytest.fixture
def scraper_partidos():

	return ScraperPartidos(369, 2019)