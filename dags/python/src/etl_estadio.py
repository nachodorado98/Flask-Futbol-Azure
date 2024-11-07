import pandas as pd
from typing import Optional

from .scrapers.scraper_estadio import ScraperEstadio

def extraerDataEstadio(estadio:str)->Optional[pd.DataFrame]:

	scraper=ScraperEstadio(estadio)

	return scraper.obtenerEstadio()