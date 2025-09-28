import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_palmares import ScraperEquipoPalmares

def extraerDataEquipoPalmares(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoPalmares(equipo)

	return scraper.obtenerEstadioPalmares()