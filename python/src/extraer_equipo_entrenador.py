import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_entrenador import ScraperEquipoEntrenador

def extraerDataEquipoEntrenador(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoEntrenador(equipo)

	return scraper.obtenerEntrenadorEquipo()