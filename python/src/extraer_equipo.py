import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo import ScraperEquipo

def extraerDataEquipoDetalle(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipo(equipo)

	return scraper.obtenerDetalleEquipo()