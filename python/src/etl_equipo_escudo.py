import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_escudo import ScraperEquipoEscudo

def extraerDataEquipoEscudo(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoEscudo(equipo)

	return scraper.obtenerEscudoEquipo()