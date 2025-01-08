import pandas as pd
from typing import Optional

from .scrapers.scraper_jugador_seleccion import ScraperJugadorSeleccion

def extraerDataJugadorSeleccion(jugador:str)->Optional[pd.DataFrame]:

	scraper=ScraperJugadorSeleccion(jugador)

	return scraper.obtenerJugadorSeleccion()