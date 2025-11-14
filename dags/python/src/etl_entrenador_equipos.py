import pandas as pd
from typing import Optional

from .scrapers.scraper_entrenador_equipos import ScraperEntrenadorEquipos

def extraerDataEntrenadorEquipos(entrenador:str)->Optional[pd.DataFrame]:

	scraper=ScraperEntrenadorEquipos(entrenador)

	return scraper.obtenerEntrenadorEquipos()