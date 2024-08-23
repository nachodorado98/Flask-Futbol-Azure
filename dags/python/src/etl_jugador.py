import pandas as pd
from typing import Optional

from .scrapers.scraper_jugador import ScraperJugador

def extraerDataJugador(jugador:str)->Optional[pd.DataFrame]:

	scraper=ScraperJugador(jugador)

	return scraper.obtenerJugador()