import pandas as pd
from typing import Optional

from .scrapers.scraper_competicion import ScraperCompeticion

from .utils import limpiarCodigoImagen

def extraerDataCompeticion(competicion:str)->Optional[pd.DataFrame]:

	scraper=ScraperCompeticion(competicion)

	return scraper.obtenerCompeticion()

def limpiarDataCompeticion(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Logo"]=tabla["Logo_URL"].apply(limpiarCodigoImagen)

	tabla["Codigo_Pais"]=tabla["Pais_URL"].apply(limpiarCodigoImagen)

	columnas=["Nombre", "Codigo_Logo", "Codigo_Pais"]

	return tabla[columnas]