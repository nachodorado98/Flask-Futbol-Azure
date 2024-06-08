import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_escudo import ScraperEquipoEscudo

from .utils import limpiarCodigoImagen

def extraerDataEquipoEscudo(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoEscudo(equipo)

	return scraper.obtenerEscudoEquipo()

def limpiarDataEquipoEscudo(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Escudo"]=tabla["Escudo"].apply(limpiarCodigoImagen).apply(lambda codigo: int(codigo))

	tabla["Puntuacion"]=tabla["Puntuacion"].apply(lambda puntuacion: int(puntuacion))

	return tabla[["Codigo_Escudo", "Puntuacion"]]