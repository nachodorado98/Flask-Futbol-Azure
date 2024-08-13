import pandas as pd
from typing import Optional

from .scrapers.scraper_competicion_campeones import ScraperCompeticionCampeones

def extraerDataCampeonesCompeticion(competicion:str)->Optional[pd.DataFrame]:

	scraper=ScraperCompeticionCampeones(competicion)

	return scraper.obtenerCampeonesCompeticion()

def limpiarDataCampeonesCompeticion(tabla:pd.DataFrame)->pd.DataFrame:

	tabla_filtrada=tabla[~(tabla["Ano"].isna())|tabla["Equipo_URL"].isna()]

	if tabla_filtrada.empty:

		raise Exception("No hay campeones disponibles")

	tabla_filtrada=tabla_filtrada.reset_index(drop=True)

	tabla_filtrada["Temporada"]=tabla_filtrada["Ano"].apply(lambda ano: int(ano))

	tabla_filtrada["Equipo"]=tabla_filtrada["Equipo_URL"].apply(lambda url: url.split("/")[-1].strip())

	columnas=["Temporada", "Equipo"]

	return tabla_filtrada[columnas]