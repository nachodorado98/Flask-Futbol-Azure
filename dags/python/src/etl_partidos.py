import pandas as pd
from typing import Optional

from .scrapers.scraper_partidos import ScraperPartidos

def extraerDataPartidosEquipo(equipo_id:int, ano:int)->Optional[pd.DataFrame]:

	scraper=ScraperPartidos(equipo_id, ano)

	return scraper.obtenerPartidosEquipo()