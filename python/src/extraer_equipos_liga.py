import pandas as pd
from typing import Optional

from .scrapers.scraper_equipos_liga import ScraperEquiposLiga

def extraerDataEquiposLiga(nombre_liga:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquiposLiga(nombre_liga)

	return scraper.obtenerClasificacionLiga()