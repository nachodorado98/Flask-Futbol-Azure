import pandas as pd
from typing import Optional

from .scrapers.scraper_partidos import ScraperPartidos

from .utils import limpiarFechaInicio

def extraerDataProximosPartidosEquipo(equipo_id:int, ano:int)->Optional[pd.DataFrame]:

	scraper=ScraperPartidos(equipo_id, ano)

	return scraper.obtenerPartidosEquipo()

def limpiarDataProximosPartidosEquipo(tabla:pd.DataFrame)->Optional[pd.DataFrame]:

	tabla["Estado_Partido"]=tabla["Estado"].apply(lambda estado: int(estado))

	tabla_filtrada=tabla[tabla["Estado_Partido"]==-1]

	if tabla_filtrada.empty:

		raise Exception("No hay proximos partidos jugados disponibles")

	tabla_filtrada=tabla_filtrada.reset_index(drop=True)

	tabla_filtrada["Partido_Id"]=tabla_filtrada["Partido_Id"].apply(lambda partido_id: partido_id.split("-")[1])

	tabla_filtrada[["Fecha", "Hora"]]=tabla_filtrada["Fecha_Inicio"].apply(lambda fecha_inicio: pd.Series(limpiarFechaInicio(fecha_inicio)))

	def obtenerEquiposId(link:str)->tuple:

		local, visitante, partido_id=link.split("partido/")[1].split("/")

		return local.strip(), visitante.strip()

	tabla_filtrada[["Equipo_Id_Local", "Equipo_Id_Visitante"]]=tabla_filtrada["Link"].apply(lambda link: pd.Series(obtenerEquiposId(link)))

	columnas=["Partido_Id", "Equipo_Id_Local", "Equipo_Id_Visitante", "Fecha",
				"Hora", "Competicion"]

	return tabla_filtrada[columnas]