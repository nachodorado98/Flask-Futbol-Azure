import pandas as pd
from typing import Optional

from .scrapers.scraper_entrenador import ScraperEntrenador

from .utils import limpiarCodigoImagen

def extraerDataEntrenador(entrenador:str)->Optional[pd.DataFrame]:

	scraper=ScraperEntrenador(entrenador)

	return scraper.obtenerEntrenador()

def limpiarDataEntrenador(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Nombre"]=tabla["Nombre"].apply(lambda nombre: nombre.strip() if nombre!="" else None)

	tabla["Codigo_Equipo"]=tabla["Equipo_URL"].apply(limpiarCodigoImagen)

	tabla["Codigo_Pais"]=tabla["Pais_URL"].apply(limpiarCodigoImagen)

	tabla["Codigo_Entrenador"]=tabla["Cara_URL"].apply(limpiarCodigoImagen)

	tabla["Puntuacion"]=tabla["Puntuacion"].apply(lambda puntuacion: int(puntuacion) if puntuacion!="" else None)

	columnas=["Nombre", "Codigo_Equipo", "Codigo_Pais", "Codigo_Entrenador", "Puntuacion"]
	
	return tabla[columnas]