import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_alineaciones import ScraperPartidoAlineaciones

def extraerDataPartidoAlineaciones(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoAlineaciones(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoAlineaciones()