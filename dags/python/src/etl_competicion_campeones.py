import pandas as pd
from typing import Optional

from .scrapers.scraper_competicion_campeones import ScraperCompeticionCampeones

from .database.conexion import Conexion

def extraerDataCampeonesCompeticion(competicion:str)->Optional[pd.DataFrame]:

	scraper=ScraperCompeticionCampeones(competicion)

	return scraper.obtenerCampeonesCompeticion()

def limpiarDataCampeonesCompeticion(tabla:pd.DataFrame)->pd.DataFrame:

	tabla_filtrada=tabla[~(tabla["Ano"].isna())|tabla["Equipo_URL"].isna()]

	if tabla_filtrada.empty:

		raise Exception("No hay campeones disponibles")

	tabla_filtrada=tabla_filtrada.reset_index(drop=True)

	tabla_filtrada["Temporada"]=tabla_filtrada["Ano"].apply(lambda ano: int(ano))

	tabla_filtrada["Equipo"]=tabla_filtrada["Equipo_URL"].apply(lambda url: url.split("/")[-1].strip())

	columnas=["Temporada", "Equipo"]

	return tabla_filtrada[columnas]

def cargarDataCampeonesCompeticion(tabla:pd.DataFrame, competicion_id:str, entorno:str)->None:

	datos_campeones=tabla.values.tolist()

	con=Conexion(entorno)

	if not con.existe_competicion(competicion_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el campeon de la competicion {competicion_id}. No existe competicion")

	try:

		for temporada, equipo in datos_campeones:

			if not con.existe_equipo(equipo):

				con.insertarEquipo(equipo)

			if not con.existe_campeon_competicion(competicion_id, temporada, equipo):

				con.insertarCampeonCompeticion([competicion_id, temporada, equipo])

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar el campeon de la competicion {competicion_id}")
