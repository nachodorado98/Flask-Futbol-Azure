import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_alineaciones import ScraperPartidoAlineaciones

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataPartidoAlineaciones(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoAlineaciones(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoAlineaciones()

def limpiarDataPartidoAlineaciones(tabla:pd.DataFrame)->pd.DataFrame:

	tabla_filtrada=tabla[~((tabla["Puntos"].isna())|(tabla["Tactica"].isna())|(tabla["Entrenador_URL"].isna()))]

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

	tabla_filtrada["Numero"]=tabla_filtrada["Numero"].apply(lambda numero: int(numero) if numero!="" and numero else 0)

	tabla_filtrada["Puntos"]=tabla_filtrada["Puntos"].apply(lambda numero: float(numero) if numero!="" and numero else 0.0)

	columnas=["Codigo_Jugador", "Numero", "Puntos", "Titular", "Local", "Posicion", "Codigo_Entrenador", "Tactica"]

	return tabla_filtrada[columnas]

def cargarDataPartidoAlineaciones(tabla:pd.DataFrame, partido_id:str, entorno:str)->None:

	tabla_entrenadores_partido=tabla[["Codigo_Entrenador", "Tactica", "Local"]].drop_duplicates()

	datos_entrenadores_partido=tabla_entrenadores_partido.values.tolist()

	tabla_alineaciones_partido=tabla[["Codigo_Jugador", "Numero", "Puntos", "Titular", "Local", "Posicion"]]

	datos_alineaciones_partido=tabla_alineaciones_partido.values.tolist()

	con=Conexion(entorno)

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar las alineaciones del partido {partido_id}. No existe")

	try:

		for entrenador, tactica, local in datos_entrenadores_partido:

			if not con.existe_entrenador(entrenador):

				con.insertarEntrenador(entrenador)

			if not con.existe_partido_entrenador(partido_id, entrenador):

				con.insertarPartidoEntrenador((partido_id, entrenador, tactica, local))

		for jugador, numero, puntuacion, titular, local, posicion in datos_alineaciones_partido:

			if not con.existe_jugador(jugador):

				con.insertarJugador(jugador)

			if not con.existe_partido_jugador(partido_id, jugador):

				con.insertarPartidoJugador((partido_id, jugador, numero, puntuacion, titular, local, posicion))

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar las alineaciones del partido {partido_id}")