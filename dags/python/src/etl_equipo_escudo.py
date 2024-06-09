import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_escudo import ScraperEquipoEscudo

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataEquipoEscudo(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoEscudo(equipo)

	return scraper.obtenerEscudoEquipo()

def limpiarDataEquipoEscudo(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Escudo"]=tabla["Escudo"].apply(limpiarCodigoImagen).apply(lambda codigo: int(codigo))

	tabla["Puntuacion"]=tabla["Puntuacion"].apply(lambda puntuacion: int(puntuacion))

	return tabla[["Codigo_Escudo", "Puntuacion"]]

def cargarDataEquipoEscudo(tabla:pd.DataFrame, equipo_id:str)->None:

	datos_escudo=tabla.values.tolist()[0]

	con=Conexion()

	if not con.existe_equipo(equipo_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el escudo del equipo {equipo_id}. No existe")

	try:

		con.actualizarEscudoEquipo(datos_escudo, equipo_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar el escudo del equipo {equipo_id}")