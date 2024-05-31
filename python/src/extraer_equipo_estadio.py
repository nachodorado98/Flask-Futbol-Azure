import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_estadio import ScraperEquipoEstadio

def extraerDataEquipoEstadio(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoEstadio(equipo)

	return scraper.obtenerEstadioEquipo()