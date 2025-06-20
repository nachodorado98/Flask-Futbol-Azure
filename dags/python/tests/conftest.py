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
from src.scrapers.scraper_partido_estadio import ScraperPartidoEstadio
from src.scrapers.scraper_partido_competicion import ScraperPartidoCompeticion
from src.scrapers.scraper_partido_goleadores import ScraperPartidoGoleadores
from src.scrapers.scraper_competicion import ScraperCompeticion
from src.scrapers.scraper_competicion_campeones import ScraperCompeticionCampeones
from src.scrapers.scraper_jugadores import ScraperJugadores
from src.scrapers.scraper_jugador import ScraperJugador
from src.scrapers.scraper_estadio import ScraperEstadio
from src.scrapers.scraper_entrenador import ScraperEntrenador
from src.scrapers.scraper_jugador_equipos import ScraperJugadorEquipos
from src.scrapers.scraper_jugador_seleccion import ScraperJugadorSeleccion

from src.scrapers.configscrapers import ENDPOINT_COMPETICION

from src.database.conexion import Conexion

from src.datalake.conexion_data_lake import ConexionDataLake

@pytest.fixture()
def entorno():

	return "DEV"

@pytest.fixture
def scraper():

	return Scraper(f"{ENDPOINT_COMPETICION}/primera/2024")

@pytest.fixture
def scraper_equipos_liga():

	return ScraperEquiposLiga("primera/2024")

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
def conexion(entorno):

	con=Conexion(entorno)

	con.c.execute("DELETE FROM equipos")

	con.c.execute("DELETE FROM estadios")

	con.c.execute("DELETE FROM partidos")

	con.c.execute("DELETE FROM competiciones")

	con.c.execute("DELETE FROM jugadores")

	con.c.execute("DELETE FROM entrenadores")

	con.c.execute("DELETE FROM temporada_jugadores")

	con.c.execute("DELETE FROM proximos_partidos")

	con.confirmar()

	return con

@pytest.fixture()
def conexion_clonar():

	return Conexion("CLONAR")

@pytest.fixture()
def datalake():

    return ConexionDataLake()

@pytest.fixture
def scraper_partidos():

	return ScraperPartidos(369, 2019)

@pytest.fixture
def scraper_partido_estadio():

	return ScraperPartidoEstadio("atletico-madrid", "betis", "202220871")

@pytest.fixture
def scraper_partido_competicion():

	return ScraperPartidoCompeticion("atletico-madrid", "betis", "202220871")

@pytest.fixture
def scraper_partido_goleadores():

	return ScraperPartidoGoleadores("atletico-madrid", "real-madrid", "2024664923")

@pytest.fixture
def scraper_competicion():

	return ScraperCompeticion("primera")

@pytest.fixture
def scraper_competicion_campeones():

	return ScraperCompeticionCampeones("primera")

@pytest.fixture
def scraper_jugadores():

	return ScraperJugadores(369, 2019)

@pytest.fixture
def scraper_jugador():

	return ScraperJugador("j-alvarez-772644")

@pytest.fixture
def scraper_estadio():

	return ScraperEstadio("riyadh-air-metropolitano-23")

@pytest.fixture
def scraper_entrenador():

	return ScraperEntrenador("diego-simeone-13")

@pytest.fixture
def scraper_jugador_equipos():

	return ScraperJugadorEquipos("j-alvarez-772644")

@pytest.fixture
def scraper_jugador_seleccion():

	return ScraperJugadorSeleccion("j-alvarez-772644")

def pytest_sessionfinish(session, exitstatus):

	con=Conexion("DEV")

	con.c.execute("DELETE FROM equipos")

	con.c.execute("DELETE FROM estadios")

	con.c.execute("DELETE FROM partidos")

	con.c.execute("DELETE FROM competiciones")

	con.c.execute("DELETE FROM jugadores")

	con.c.execute("DELETE FROM entrenadores")

	con.c.execute("DELETE FROM temporada_jugadores")

	con.confirmar()

	con.cerrarConexion()

	print("\nLimpieza de la BBDD correcta")