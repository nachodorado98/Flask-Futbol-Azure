import pandas as pd
from typing import Optional
from datetime import datetime

from .scrapers.scraper_entrenador_equipos import ScraperEntrenadorEquipos

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataEntrenadorEquipos(entrenador:str)->Optional[pd.DataFrame]:

	scraper=ScraperEntrenadorEquipos(entrenador)

	return scraper.obtenerEntrenadorEquipos()

def limpiarDataEntrenadorEquipos(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Equipo"]=tabla["Equipo_URL"].apply(limpiarCodigoImagen)

	tabla["Desde"]=tabla["Desde"].apply(lambda fecha: datetime.strptime(fecha, "%d-%m-%Y").strftime("%Y-%m-%d"))

	tabla["Hasta"]=tabla["Hasta"].apply(lambda fecha: datetime.strptime(fecha, "%d-%m-%Y").strftime("%Y-%m-%d"))

	tabla["_Desde_dt"]=pd.to_datetime(tabla["Desde"])

	tabla=tabla.sort_values("_Desde_dt")

	tabla=tabla.astype({"Partidos_Totales": int, "Ganados": int, "Empatados": int, "Perdidos": int})

	tabla["Duracion"]=tabla["Desde"]+","+tabla["Hasta"]

	tabla=tabla.groupby("Codigo_Equipo").agg({"Partidos_Totales": "sum", "Ganados": "sum", "Empatados": "sum", "Perdidos": "sum",
        										"Duracion": lambda fechas: ";".join(fechas), "Tactica": "first"}).reset_index()

	columnas=["Codigo_Equipo", "Partidos_Totales", "Duracion", "Ganados", "Empatados", "Perdidos", "Tactica"]

	return tabla[columnas]

def cargarDataEntrenadorEquipos(tabla:pd.DataFrame, entrenador_id:str, entorno:str)->None:

	datos_entrenador_equipos=tabla.values.tolist()

	con=Conexion(entorno)

	if not con.existe_entrenador(entrenador_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar los equipos del entrenador {entrenador_id}. No existe")

	try:

		for equipo_id, partidos_totales, duracion, ganados, empatados, perdidos, tactica in datos_entrenador_equipos:

			if not con.existe_equipo(equipo_id):

				con.insertarEquipo(equipo_id)

			if not con.existe_equipo_entrenador(entrenador_id, equipo_id):

				con.insertarEquipoEntrenador((entrenador_id, equipo_id, partidos_totales, duracion, ganados, empatados, perdidos, tactica))

			con.actualizarDatosEquipoEntrenador([partidos_totales, duracion, ganados, empatados, perdidos, tactica], entrenador_id, equipo_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los datos de los equipos del entrenador {equipo_id}")