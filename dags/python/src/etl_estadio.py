import pandas as pd
from typing import Optional

from .scrapers.scraper_estadio import ScraperEstadio

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataEstadio(estadio:str)->Optional[pd.DataFrame]:

	scraper=ScraperEstadio(estadio)

	return scraper.obtenerEstadio()

def limpiarDataEstadio(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Estadio"]=tabla["Codigo_Estadio"].apply(limpiarCodigoImagen)

	tabla["Codigo_Pais"]=tabla["Pais_URL"].apply(limpiarCodigoImagen)

	columnas=["Pais", "Codigo_Pais"]

	return tabla[columnas]

def cargarDataEstadio(tabla:pd.DataFrame, estadio_id:str, entorno:str)->None:

	datos_estadio=tabla.values.tolist()[0]

	con=Conexion(entorno)

	if not con.existe_estadio(estadio_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el estadio {estadio_id}. No existe")

	try:

		con.actualizarDatosEstadio(datos_estadio, estadio_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los datos del estadio {estadio_id}")