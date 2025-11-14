import pandas as pd
from typing import Optional
from datetime import datetime

from .scrapers.scraper_entrenador_equipos import ScraperEntrenadorEquipos

from .utils import limpiarCodigoImagen

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