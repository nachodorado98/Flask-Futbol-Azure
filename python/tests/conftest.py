import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest

from src.scrapers.scraper import Scraper
from src.scrapers.scraper_equipos_liga import ScraperEquiposLiga
from src.scrapers.configscrapers import ENDPOINT_COMPETICION

@pytest.fixture
def scraper():

	return Scraper(f"{ENDPOINT_COMPETICION}/primera")

@pytest.fixture
def scraper_equipos_liga():

	return ScraperEquiposLiga("primera")