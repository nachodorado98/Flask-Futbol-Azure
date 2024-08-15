import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_competicion import ScraperPartidoCompeticion

def extraerDataPartidoCompeticion(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoCompeticion(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoCompeticion()

def limpiarDataPartidoCompeticion(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Competicion"]=tabla["Competicion_URL"].apply(lambda url: url.split("/resultados/")[-1].split("/")[0].strip())

	columnas=["Codigo_Competicion"]

	return tabla[columnas]