import pandas as pd
from typing import Optional

from .scrapers.scraper_entrenador_palmares import ScraperEntrenadorPalmares

def extraerDataEntrenadorPalmares(entrenador:str)->Optional[pd.DataFrame]:

	scraper=ScraperEntrenadorPalmares(entrenador)

	return scraper.obtenerEntrenadorPalmares()