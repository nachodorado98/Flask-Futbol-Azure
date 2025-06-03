import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_competicion import ScraperPartidoCompeticion

from .database.conexion import Conexion

def extraerDataPartidoCompeticion(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoCompeticion(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoCompeticion()

def limpiarDataPartidoCompeticion(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Competicion"]=tabla["Competicion_URL"].apply(lambda url: url.split("/resultados/")[-1].split("/")[0].strip())

	columnas=["Codigo_Competicion"]

	return tabla[columnas]

def cargarDataPartidoCompeticion(tabla:pd.DataFrame, partido_id:str, entorno:str)->None:

	dato_competicion=tabla.values.tolist()[0][0]

	con=Conexion(entorno)

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar la competicion del partido {partido_id}. No existe")

	try:

		if not con.existe_competicion(dato_competicion):

			con.insertarCompeticion(dato_competicion)

		if not con.existe_partido_competicion(partido_id, dato_competicion):

			con.insertarPartidoCompeticion((partido_id,dato_competicion))

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar la competicion del partido {partido_id}")