import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_palmares import ScraperEquipoPalmares

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataEquipoPalmares(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoPalmares(equipo)

	return scraper.obtenerEstadioPalmares()

def limpiarDataEquipoPalmares(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Imagen_Titulo"]=tabla["Imagen_Titulo"].apply(limpiarCodigoImagen)

	tabla["Imagen_Competicion"]=tabla["Imagen_Competicion"].apply(limpiarCodigoImagen)

	tabla["Numero"]=tabla["Numero"].apply(lambda numero: int(numero))

	columnas=["Nombre", "Numero", "Imagen_Competicion", "Imagen_Titulo", "Annos"]

	return tabla[columnas]

def cargarDataEquipoPalmares(tabla:pd.DataFrame, equipo_id:str, entorno:str)->None:

	datos_palmares=tabla.values.tolist()

	con=Conexion(entorno)

	if not con.existe_equipo(equipo_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el palmares del equipo {equipo_id}. No existe")

	try:

		for nombre, numero, logo, titulo, annos in datos_palmares:

			competicion_id=con.obtenerCompeticionPorLogo(logo)

			if competicion_id:

				con.actualizarTituloCompeticion(titulo, competicion_id)

				if not con.existe_titulo_equipo(competicion_id, equipo_id):

					con.insertarTituloEquipo((equipo_id, competicion_id, nombre, numero, annos))

				con.actualizarDatosTituloEquipo([nombre, numero, annos], competicion_id, equipo_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los datos de los titulos del equipo {equipo_id}")