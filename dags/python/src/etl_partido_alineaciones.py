import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_alineaciones import ScraperPartidoAlineaciones

from .utils import limpiarCodigoImagen

def extraerDataPartidoAlineaciones(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoAlineaciones(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoAlineaciones()

def limpiarDataPartidoAlineaciones(tabla:pd.DataFrame)->pd.DataFrame:

	tabla_filtrada=tabla[~((tabla["Puntos"].isna())|(tabla["Tactica"].isna()))]

	if tabla_filtrada.empty:

		raise Exception("No hay alineaciones disponibles")

	filas_titulares_local=tabla_filtrada[(tabla_filtrada["Alineacion"]=="T")&(tabla_filtrada["Tipo"]=="L")].shape[0]

	filas_titulares_visitante=tabla_filtrada[(tabla_filtrada["Alineacion"]=="T")&(tabla_filtrada["Tipo"]=="V")].shape[0]

	tabla_corregida=tabla_filtrada.copy()

	if filas_titulares_local!=11:

		tabla_corregida=tabla_corregida[tabla_corregida["Tipo"]!="L"]

	if filas_titulares_visitante!=11:

		tabla_corregida=tabla_corregida[tabla_corregida["Tipo"]!="V"]

	if tabla_corregida.empty:

		raise Exception("No hay alineaciones completas")

	tabla_filtrada=tabla_corregida

	tabla_filtrada=tabla_filtrada.reset_index(drop=True)

	tabla_filtrada["Codigo_Jugador"]=tabla_filtrada["Jugador_URL"].apply(limpiarCodigoImagen)

	tabla_filtrada["Codigo_Entrenador"]=tabla_filtrada["Entrenador_URL"].apply(limpiarCodigoImagen)

	tabla_filtrada["Local"]=tabla_filtrada["Tipo"].apply(lambda tipo: True if tipo=="L" else False)

	tabla_filtrada["Titular"]=tabla_filtrada["Alineacion"].apply(lambda alineacion: True if alineacion=="T" else False)

	tabla_filtrada["Numero"]=tabla_filtrada["Numero"].apply(lambda numero: int(numero) if numero!="" and numero else None)

	tabla_filtrada["Puntos"]=tabla_filtrada["Puntos"].apply(lambda numero: float(numero) if numero!="" and numero else None)

	columnas=["Codigo_Jugador", "Numero", "Puntos", "Titular", "Local", "Posicion", "Codigo_Entrenador", "Tactica"]

	return tabla_filtrada[columnas]