import pandas as pd
from typing import Optional

from .scrapers.scraper_entrenador import ScraperEntrenador

def extraerDataEntrenador(entrenador:str)->Optional[pd.DataFrame]:

	scraper=ScraperEntrenador(entrenador)

	return scraper.obtenerEntrenador()