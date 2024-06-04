import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_entrenador import ScraperEquipoEntrenador

from .utils import normalizarNombre, limpiarCodigoImagen, limpiarFecha, limpiarTiempo

def extraerDataEquipoEntrenador(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoEntrenador(equipo)

	return scraper.obtenerEntrenadorEquipo()

def limpiarDataEquipoEntrenador(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Nombre_URL"]=tabla["Nombre"].apply(normalizarNombre).apply(lambda nombre: "-".join(nombre.lower().split(" ")))

	tabla["Codigo_Entrenador"]=tabla["Entrenador_URL"].apply(limpiarCodigoImagen).apply(lambda codigo: None if not codigo else int(codigo))

	tabla["Fecha"]=tabla["Fecha"].apply(limpiarFecha)

	tabla["Edad"]=tabla["Edad"].apply(limpiarTiempo)

	for tipo in ["Partidos", "Ganados", "Empatados", "Perdidos"]:

		tabla[tipo]=tabla[tipo].apply(lambda valor: int(valor))

	columnas=["Nombre_URL", "Nombre", "Codigo_Entrenador", "Fecha", "Partidos", "Ganados", "Empatados", "Perdidos"]

	return tabla[columnas]