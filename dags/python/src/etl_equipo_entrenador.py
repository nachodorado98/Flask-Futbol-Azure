import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_entrenador import ScraperEquipoEntrenador

from .utils import normalizarNombre, limpiarCodigoImagen, limpiarFecha, limpiarTiempo

from .database.conexion import Conexion

def extraerDataEquipoEntrenador(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoEntrenador(equipo)

	return scraper.obtenerEntrenadorEquipo()

def limpiarDataEquipoEntrenador(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Entrenador"]=tabla["Entrenador_URL"].apply(limpiarCodigoImagen).apply(lambda codigo: None if not codigo or codigo=="nofoto_jugador" else int(codigo))

	tabla["Codigo_Entrenador_String"]=tabla["Codigo_Entrenador"].apply(lambda codigo: "" if not codigo else str(codigo))

	tabla["Nombre_Normalizado"]=tabla["Nombre"].apply(normalizarNombre).apply(lambda nombre: "-".join(nombre.lower().split(" ")))

	tabla["Nombre_URL"]=tabla["Nombre_Normalizado"]+"-"+tabla["Codigo_Entrenador_String"]

	tabla["Fecha"]=tabla["Fecha"].apply(limpiarFecha)

	tabla["Edad"]=tabla["Edad"].apply(limpiarTiempo)

	for tipo in ["Partidos", "Ganados", "Empatados", "Perdidos"]:

		tabla[tipo]=tabla[tipo].apply(lambda valor: int(valor))

	columnas=["Nombre", "Nombre_URL", "Codigo_Entrenador", "Partidos"]

	return tabla[columnas]

def cargarDataEquipoEntrenador(tabla:pd.DataFrame, equipo_id:str)->None:

	datos_entrenador=tabla.values.tolist()[0]

	con=Conexion()

	if not con.existe_equipo(equipo_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el entrenador del equipo {equipo_id}. No existe")

	try:

		con.actualizarEntrenadorEquipo(datos_entrenador, equipo_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar el entrenador del equipo {equipo_id}")