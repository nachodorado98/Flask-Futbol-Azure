import pandas as pd
from typing import Optional

from .scrapers.scraper_partido_estadio import ScraperPartidoEstadio

from .utils import limpiarCodigoImagen, normalizarNombre, obtenerCoordenadasEstadio, limpiarTamano

from .database.conexion import Conexion

def extraerDataPartidoEstadio(equipo_local:str, equipo_visitante:str, partido_id:str)->Optional[pd.DataFrame]:

	scraper=ScraperPartidoEstadio(equipo_local, equipo_visitante, partido_id)

	return scraper.obtenerPartidoEstadio()

def limpiarDataPartidoEstadio(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Estadio"]=tabla["Codigo_Estadio"].apply(limpiarCodigoImagen).apply(lambda codigo: None if not codigo or codigo=="estadio_nofoto" else int(codigo))

	tabla["Nombre"]=tabla["Nombre"].apply(lambda nombre: None if nombre=="" else nombre.strip())

	tabla["Ciudad"]=tabla["Ciudad"].apply(lambda ciudad: None if ciudad=="" else ciudad.strip())

	tabla["Direccion"]=tabla["Direccion"].apply(lambda direccion: None if direccion=="" else direccion.strip())

	tabla["Nombre_URL"]=tabla["Nombre"].apply(normalizarNombre).apply(lambda nombre: "-".join(nombre.lower().split(" ")))

	tabla[["Latitud", "Longitud"]]=tabla["Nombre"].apply(lambda estadio: pd.Series(obtenerCoordenadasEstadio(estadio)))

	tabla["Capacidad"]=tabla["Capacidad"].apply(lambda capacidad: int(capacidad.replace(".","")) if capacidad!="" else None)

	tabla["Fecha"]=tabla["Fecha construccion"].apply(lambda fecha: int(fecha) if fecha!="" else None)

	tabla[["Largo", "Ancho"]]=tabla["Tamaño"].apply(lambda tamano: pd.Series(limpiarTamano(tamano)))

	tabla["Cesped"]=tabla["Cesped"].apply(lambda cesped: cesped.strip() if cesped!="" else None)

	columnas=["Nombre_URL", "Codigo_Estadio", "Nombre", "Direccion", "Latitud", "Longitud", "Ciudad",
				"Capacidad", "Fecha", "Largo", "Ancho", "Telefono", "Cesped"]

	return tabla[columnas]

def cargarDataPartidoEstadio(tabla:pd.DataFrame, partido_id:str)->None:

	datos_estadio=tabla.values.tolist()[0]

	con=Conexion()

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el estadio del partido {partido_id}. No existe")

	try:

		if not con.existe_estadio(datos_estadio[0]):

			con.insertarEstadio(datos_estadio)

		if not con.existe_partido_estadio(partido_id, datos_estadio[0]):

			con.insertarPartidoEstadio((partido_id, datos_estadio[0]))

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar el estadio del partido {partido_id}")