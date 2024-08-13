import pandas as pd
from typing import Optional

from .scrapers.scraper_competicion_campeones import ScraperCompeticionCampeones

def extraerDataCampeonesCompeticion(competicion:str)->Optional[pd.DataFrame]:

	scraper=ScraperCompeticionCampeones(competicion)

	return scraper.obtenerCampeonesCompeticion()