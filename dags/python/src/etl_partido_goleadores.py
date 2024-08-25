import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_goleadores import ScraperPartidoGoleadores

def extraerDataPartidoGoleadores(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoGoleadores(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoGoleadores()