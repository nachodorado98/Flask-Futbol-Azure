import pandas as pd
from typing import Optional

from .scrapers.scraper_estadio import ScraperEstadio

from .utils import limpiarCodigoImagen

def extraerDataEstadio(estadio:str)->Optional[pd.DataFrame]:

	scraper=ScraperEstadio(estadio)

	return scraper.obtenerEstadio()

def limpiarDataEstadio(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Estadio"]=tabla["Codigo_Estadio"].apply(limpiarCodigoImagen)

	tabla["Codigo_Pais"]=tabla["Pais_URL"].apply(limpiarCodigoImagen)

	columnas=["Pais", "Codigo_Pais"]

	return tabla[columnas]