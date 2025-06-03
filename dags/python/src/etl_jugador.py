import pandas as pd
from typing import Optional

from .scrapers.scraper_jugador import ScraperJugador

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataJugador(jugador:str)->Optional[pd.DataFrame]:

	scraper=ScraperJugador(jugador)

	return scraper.obtenerJugador()

def limpiarDataJugador(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Nombre"]=tabla["Nombre"].apply(lambda nombre: nombre.strip() if nombre!="" else None)

	tabla["Codigo_Equipo"]=tabla["Equipo_URL"].apply(limpiarCodigoImagen)

	tabla["Codigo_Pais"]=tabla["Pais_URL"].apply(limpiarCodigoImagen)

	tabla["Codigo_Jugador"]=tabla["Cara_URL"].apply(limpiarCodigoImagen)

	tabla["Puntuacion"]=tabla["Puntuacion"].apply(lambda puntuacion: int(puntuacion) if puntuacion!="" else None)

	tabla["Valor"]=tabla["Valor"].apply(lambda valor: float(valor) if valor!="" else None)

	tabla["Dorsal"]=tabla["Dorsal"].apply(lambda dorsal: int(dorsal) if dorsal!="" else None)

	columnas=["Nombre", "Codigo_Equipo", "Codigo_Pais", "Codigo_Jugador", "Puntuacion", "Valor", "Dorsal", "Posicion"]

	return tabla[columnas]

def cargarDataJugador(tabla:pd.DataFrame, jugador_id:str, entorno:str)->None:

	datos_jugador=tabla.values.tolist()[0]

	con=Conexion(entorno)

	if not con.existe_jugador(jugador_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el jugador {jugador_id}. No existe")

	try:

		if datos_jugador[1] and not con.existe_equipo(datos_jugador[1]):

			con.insertarEquipo(datos_jugador[1])

		con.actualizarDatosJugador(datos_jugador, jugador_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los datos del jugador {jugador_id}")