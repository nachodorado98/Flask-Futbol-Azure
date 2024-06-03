import pandas as pd
from typing import Optional

from .scrapers.scraper_equipos_liga import ScraperEquiposLiga

from .utils import limpiarCodigoImagen

def extraerDataEquiposLiga(nombre_liga:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquiposLiga(nombre_liga)

	return scraper.obtenerClasificacionLiga()

def limpiarDataEquiposLiga(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Nombre_URL"]=tabla["Nombre_URL"].apply(lambda nombre_url: nombre_url.strip())

	tabla["Codigo_Escudo"]=tabla["Escudo"].apply(limpiarCodigoImagen).apply(lambda codigo: int(codigo))

	return tabla[["Nombre_URL", "Codigo_Escudo"]]