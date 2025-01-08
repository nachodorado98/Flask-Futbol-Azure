import pandas as pd
from typing import Optional

from .scrapers.scraper_jugador_seleccion import ScraperJugadorSeleccion

from .utils import limpiarCodigoImagen

def extraerDataJugadorSeleccion(jugador:str)->Optional[pd.DataFrame]:

	scraper=ScraperJugadorSeleccion(jugador)

	return scraper.obtenerJugadorSeleccion()

def limpiarDataJugadorSeleccion(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Seleccion"]=tabla["Codigo_Seleccion"].apply(limpiarCodigoImagen)

	tabla["Convocatorias"]=tabla["Convocatorias"].apply(lambda texto: int(texto.split(" veces")[0]))

	tabla["Goles"]=tabla["Goles"].apply(lambda goles: 0 if goles=="-" else int(goles))

	tabla["Media"]=tabla["Media"].apply(lambda media: 0.0 if media=="-" else float(media))

	tabla["Asistencias"]=tabla["Asistencias"].apply(lambda asistencias: 0 if asistencias=="-" else int(asistencias))

	tabla["Amarillas"]=tabla["Amarillas"].apply(lambda amarillas: 0 if amarillas=="-" else int(amarillas))

	tabla["Rojas"]=tabla["Rojas"].apply(lambda rojas: 0 if rojas=="-" else int(rojas))

	columnas=["Codigo_Seleccion", "Convocatorias", "Goles", "Asistencias"]

	return tabla[columnas]