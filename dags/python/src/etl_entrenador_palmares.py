import pandas as pd
from typing import Optional

from .scrapers.scraper_entrenador_palmares import ScraperEntrenadorPalmares

from .utils import limpiarCodigoImagen

def extraerDataEntrenadorPalmares(entrenador:str)->Optional[pd.DataFrame]:

	scraper=ScraperEntrenadorPalmares(entrenador)

	return scraper.obtenerEntrenadorPalmares()

def limpiarDataEntrenadorPalmares(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Imagen_Titulo"]=tabla["Imagen_Titulo"].apply(limpiarCodigoImagen)

	columnas=["Nombre", "Competicion", "Imagen_Titulo", "Annos"]

	return tabla[columnas]