import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_goleadores import ScraperPartidoGoleadores

from .utils import limpiarCodigoImagen, limpiarMinuto

from .database.conexion import Conexion

def extraerDataPartidoGoleadores(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoGoleadores(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoGoleadores()

def limpiarDataPartidoGoleadores(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Jugador"]=tabla["Jugador_URL"].apply(limpiarCodigoImagen)

	tabla[["Minuto", "Anadido"]]=tabla["Minuto"].apply(lambda minuto: pd.Series(limpiarMinuto(minuto)))

	tabla["Local"]=tabla["Equipo"].apply(lambda equipo: True if equipo==1 else False)

	columnas=["Codigo_Jugador", "Minuto", "Anadido", "Local"]

	return tabla[columnas]

def cargarDataPartidoGoleadores(tabla:pd.DataFrame, partido_id:str, entorno:str)->None:

	datos_goleadores=tabla.values.tolist()

	con=Conexion(entorno)

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar la competicion del partido {partido_id}. No existe")

	try:

		for goleador, minuto, anadido, local in datos_goleadores:

			if not con.existe_jugador(goleador):

				con.insertarJugador(goleador)

			if not con.existe_partido_goleador(partido_id, goleador, minuto, anadido):

				con.insertarPartidoGoleador((partido_id, goleador, minuto, anadido, local))

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los goleadores del partido {partido_id}")