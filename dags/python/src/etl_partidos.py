import pandas as pd
from typing import Optional

from .scrapers.scraper_partidos import ScraperPartidos

from .utils import limpiarFechaInicio, obtenerResultado

from .database.conexion import Conexion

def extraerDataPartidosEquipo(equipo_id:int, ano:int)->Optional[pd.DataFrame]:

	scraper=ScraperPartidos(equipo_id, ano)

	return scraper.obtenerPartidosEquipo()

def limpiarDataPartidosEquipo(tabla:pd.DataFrame)->Optional[pd.DataFrame]:

	tabla["Estado_Partido"]=tabla["Estado"].apply(lambda estado: int(estado))

	tabla_filtrada=tabla[tabla["Estado_Partido"]==1]

	if tabla_filtrada.empty:

		raise Exception("No hay partidos jugados disponibles")

	tabla_filtrada=tabla_filtrada.reset_index(drop=True)

	tabla_filtrada["Partido_Id"]=tabla_filtrada["Partido_Id"].apply(lambda partido_id: partido_id.split("-")[1])

	tabla_filtrada[["Fecha", "Hora"]]=tabla_filtrada["Fecha_Inicio"].apply(lambda fecha_inicio: pd.Series(limpiarFechaInicio(fecha_inicio)))

	tabla_filtrada["Resultado"]=tabla_filtrada["Marcador"].apply(obtenerResultado)

	def obtenerEquiposId(link:str)->tuple:

		local, visitante, partido_id=link.split("partido/")[1].split("/")

		return local.strip(), visitante.strip()

	tabla_filtrada[["Equipo_Id_Local", "Equipo_Id_Visitante"]]=tabla_filtrada["Link"].apply(lambda link: pd.Series(obtenerEquiposId(link)))

	columnas=["Partido_Id", "Equipo_Id_Local", "Equipo_Id_Visitante", "Fecha",
				"Hora", "Competicion", "Marcador", "Resultado"]

	return tabla_filtrada[columnas]

def cargarDataPartidosEquipo(tabla:pd.DataFrame)->None:

	partidos=tabla.values.tolist()

	def agregarEquipos(equipo_id:str)->None:

		con=Conexion()

		if not con.existe_equipo(equipo_id):

			con.insertarEquipo(equipo_id)

		con.cerrarConexion()

	for partido in partidos:

		agregarEquipos(partido[1])

		agregarEquipos(partido[2])

		con=Conexion()

		if not con.existe_partido(partido[0]):

			try:

				con.insertarPartido(partido)

			except Exception:

				print(f"Error en partido {partido}")

		con.cerrarConexion()

		

	