import pandas as pd
from typing import Optional

from .scrapers.scraper_entrenador import ScraperEntrenador

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataEntrenador(entrenador:str)->Optional[pd.DataFrame]:

	scraper=ScraperEntrenador(entrenador)

	return scraper.obtenerEntrenador()

def limpiarDataEntrenador(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Nombre"]=tabla["Nombre"].apply(lambda nombre: nombre.strip() if nombre!="" else None)

	tabla["Codigo_Equipo"]=tabla["Equipo_URL"].apply(limpiarCodigoImagen)

	tabla["Codigo_Pais"]=tabla["Pais_URL"].apply(limpiarCodigoImagen)

	tabla["Codigo_Entrenador"]=tabla["Cara_URL"].apply(limpiarCodigoImagen)

	tabla["Puntuacion"]=tabla["Puntuacion"].apply(lambda puntuacion: int(puntuacion) if puntuacion!="" else None)

	columnas=["Nombre", "Codigo_Equipo", "Codigo_Pais", "Codigo_Entrenador", "Puntuacion"]
	
	return tabla[columnas]

def cargarDataEntrenador(tabla:pd.DataFrame, entrenador_id:str)->None:

	datos_entrenador=tabla.values.tolist()[0]

	con=Conexion()

	if not con.existe_entrenador(entrenador_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el jugador {entrenador_id}. No existe")

	try:

		if datos_entrenador[1] and not con.existe_equipo(datos_entrenador[1]):

			con.insertarEquipo(datos_entrenador[1])

		con.actualizarDatosEntrenador(datos_entrenador, entrenador_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los datos del entrenador {entrenador_id}")