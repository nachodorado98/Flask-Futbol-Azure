import pandas as pd
from typing import Optional

from .scrapers.scraper_entrenador_palmares import ScraperEntrenadorPalmares

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataEntrenadorPalmares(entrenador:str)->Optional[pd.DataFrame]:

	scraper=ScraperEntrenadorPalmares(entrenador)

	return scraper.obtenerEntrenadorPalmares()

def limpiarDataEntrenadorPalmares(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Imagen_Titulo"]=tabla["Imagen_Titulo"].apply(limpiarCodigoImagen)

	tabla["Numero"]=tabla["Annos"].apply(lambda annos: len(annos.split(";")))

	columnas=["Nombre", "Numero", "Competicion", "Imagen_Titulo", "Annos"]

	return tabla[columnas]

def cargarDataEntrenadorPalmares(tabla:pd.DataFrame, entrenador_id:str, entorno:str)->None:

	datos_palmares=tabla.values.tolist()

	con=Conexion(entorno)

	if not con.existe_entrenador(entrenador_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el palmares del entrenador {entrenador_id}. No existe")

	try:

		for nombre, numero, competicion_id, titulo, annos in datos_palmares:

			if con.existe_competicion(competicion_id):

				con.actualizarTituloCompeticion(titulo, competicion_id)

				if not con.existe_titulo_entrenador(competicion_id, entrenador_id):

					con.insertarTituloEntrenador((entrenador_id, competicion_id, nombre, numero, annos))

				con.actualizarDatosTituloEntrenador([nombre, numero, annos], competicion_id, entrenador_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los datos de los titulos del entrenador {entrenador_id}")