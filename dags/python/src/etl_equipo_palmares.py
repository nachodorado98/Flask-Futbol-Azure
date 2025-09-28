import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_palmares import ScraperEquipoPalmares

from .utils import limpiarCodigoImagen

def extraerDataEquipoPalmares(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoPalmares(equipo)

	return scraper.obtenerEstadioPalmares()

def limpiarDataEquipoPalmares(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Imagen_Titulo"]=tabla["Imagen_Titulo"].apply(limpiarCodigoImagen)

	tabla["Imagen_Competicion"]=tabla["Imagen_Competicion"].apply(limpiarCodigoImagen)

	tabla["Numero"]=tabla["Numero"].apply(lambda numero: int(numero))

	columnas=["Nombre", "Numero", "Imagen_Competicion", "Imagen_Titulo", "Annos"]

	return tabla[columnas]