import pandas as pd
from typing import Optional

from .scrapers.scraper_jugadores import ScraperJugadores

def extraerDataJugadoresEquipo(equipo_id:int, ano:int)->Optional[pd.DataFrame]:

	scraper=ScraperJugadores(equipo_id, ano)

	return scraper.obtenerJugadoresEquipo()