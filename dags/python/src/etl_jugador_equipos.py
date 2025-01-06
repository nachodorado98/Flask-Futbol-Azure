import pandas as pd
from typing import Optional

from .scrapers.scraper_jugador_equipos import ScraperJugadorEquipos

from .utils import limpiarCodigoImagen

def extraerDataJugadorEquipos(jugador:str)->Optional[pd.DataFrame]:

	scraper=ScraperJugadorEquipos(jugador)

	return scraper.obtenerJugadorEquipos()

def limpiarDataJugadorEquipos(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Equipo"]=tabla["Equipo_URL"].apply(limpiarCodigoImagen)

	tabla["Temporadas"]=tabla["Temporadas"].apply(lambda temporada: int(temporada.split(" ")[0]))

	tabla=tabla.astype({"Goles": int, "Partidos": int})

	columnas=["Codigo_Equipo", "Temporadas", "Goles", "Partidos"]

	return tabla[columnas]