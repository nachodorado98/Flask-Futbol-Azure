import pandas as pd
from typing import Optional

from .scrapers.scraper_competicion import ScraperCompeticion

def extraerDataCompeticion(competicion:str)->Optional[pd.DataFrame]:

	scraper=ScraperCompeticion(competicion)

	return scraper.obtenerCompeticion()