import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_estadio import ScraperPartidoEstadio

def extraerDataPartidoEstadio(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoEstadio(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoEstadio()