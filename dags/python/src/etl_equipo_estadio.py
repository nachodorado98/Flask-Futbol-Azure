import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo_estadio import ScraperEquipoEstadio

from .utils import limpiarCodigoImagen, normalizarNombre, obtenerCoordenadasEstadio, limpiarTamano

def extraerDataEquipoEstadio(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipoEstadio(equipo)

	return scraper.obtenerEstadioEquipo()

def limpiarDataEquipoEstadio(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Estadio"]=tabla["Codigo_Estadio"].apply(limpiarCodigoImagen).apply(lambda codigo: None if not codigo or codigo=="estadio_nofoto" else int(codigo))

	tabla["Nombre"]=tabla["Nombre"].apply(lambda nombre: nombre.strip())

	tabla["Nombre_URL"]=tabla["Nombre"].apply(normalizarNombre).apply(lambda nombre: "-".join(nombre.lower().split(" ")))

	tabla["Direccion"]=tabla["Direccion"].apply(lambda direccion: direccion.strip())

	tabla[["Latitud", "Longitud"]]=tabla["Nombre"].apply(lambda estadio: pd.Series(obtenerCoordenadasEstadio(estadio)))

	tabla["Capacidad"]=tabla["Capacidad"].apply(lambda capacidad: int(capacidad.replace(".","")) if capacidad!="" else None)

	tabla["Fecha"]=tabla["Fecha construccion"].apply(lambda fecha: int(fecha) if fecha!="" else None)

	tabla[["Largo", "Ancho"]]=tabla["Tamaño"].apply(lambda tamano: pd.Series(limpiarTamano(tamano)))

	tabla["Cesped"]=tabla["Cesped"].apply(lambda cesped: cesped.strip() if cesped!="" else None)

	columnas=["Nombre_URL", "Codigo_Estadio", "Nombre", "Direccion", "Latitud", "Longitud", "Ciudad",
				"Capacidad", "Fecha", "Largo", "Ancho", "Telefono", "Cesped"]

	return tabla[columnas]