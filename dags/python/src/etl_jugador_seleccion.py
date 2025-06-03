import pandas as pd
from typing import Optional

from .scrapers.scraper_jugador_seleccion import ScraperJugadorSeleccion

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

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

def cargarDataJugadorSeleccion(tabla:pd.DataFrame, jugador_id:str, entorno:str)->None:

	datos_jugador_seleccion=tabla.values.tolist()[0]

	con=Conexion(entorno)

	if not con.existe_jugador(jugador_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar la seleccion del jugador {jugador_id}. No existe")

	try:

		if not con.existe_seleccion_jugador(jugador_id):

			con.insertarSeleccionJugador([jugador_id]+datos_jugador_seleccion)

		con.actualizarDatosSeleccionJugador(datos_jugador_seleccion, jugador_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar la seleccion del jugador {jugador_id}")