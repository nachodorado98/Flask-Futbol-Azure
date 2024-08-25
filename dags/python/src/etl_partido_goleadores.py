import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_goleadores import ScraperPartidoGoleadores

from .utils import limpiarCodigoImagen, limpiarMinuto

def extraerDataPartidoGoleadores(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoGoleadores(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoGoleadores()

def limpiarDataPartidoGoleadores(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Jugador"]=tabla["Jugador_URL"].apply(limpiarCodigoImagen)

	tabla[["Minuto", "Anadido"]]=tabla["Minuto"].apply(lambda minuto: pd.Series(limpiarMinuto(minuto)))

	tabla["Local"]=tabla["Equipo"].apply(lambda equipo: True if equipo==1 else False)

	columnas=["Codigo_Jugador", "Minuto", "Anadido", "Local"]

	return tabla[columnas]