import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_competicion import ScraperPartidoCompeticion

def extraerDataPartidoCompeticion(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoCompeticion(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoCompeticion()