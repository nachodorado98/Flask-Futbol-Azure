import pandas as pd
from typing import Optional

from .scrapers.scraper_competicion import ScraperCompeticion

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataCompeticion(competicion:str)->Optional[pd.DataFrame]:

	scraper=ScraperCompeticion(competicion)

	return scraper.obtenerCompeticion()

def limpiarDataCompeticion(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Logo"]=tabla["Logo_URL"].apply(limpiarCodigoImagen)

	tabla["Codigo_Pais"]=tabla["Pais_URL"].apply(limpiarCodigoImagen)

	columnas=["Nombre", "Codigo_Logo", "Codigo_Pais"]

	return tabla[columnas]

def cargarDataCompeticion(tabla:pd.DataFrame, competicion_id:str, entorno:str)->None:

	datos_competicion=tabla.values.tolist()[0]

	con=Conexion(entorno)

	if not con.existe_competicion(competicion_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar la competicion {competicion_id}. No existe")

	try:

		con.actualizarDatosCompeticion(datos_competicion, competicion_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los datos de la competicion {competicion_id}")