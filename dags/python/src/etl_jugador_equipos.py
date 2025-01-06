import pandas as pd
from typing import Optional

from .scrapers.scraper_jugador_equipos import ScraperJugadorEquipos

def extraerDataJugadorEquipos(jugador:str)->Optional[pd.DataFrame]:

	scraper=ScraperJugadorEquipos(jugador)

	return scraper.obtenerJugadorEquipos()