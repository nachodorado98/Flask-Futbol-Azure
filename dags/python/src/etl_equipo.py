import pandas as pd
from typing import Optional

from .scrapers.scraper_equipo import ScraperEquipo

from .utils import limpiarCodigoImagen, limpiarFecha, limpiarTiempo

from .database.conexion import Conexion

def extraerDataEquipoDetalle(equipo:str)->Optional[pd.DataFrame]:

	scraper=ScraperEquipo(equipo)

	return scraper.obtenerDetalleEquipo()

def limpiarDataEquipoDetalle(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Pais"]=tabla["Pais_URL"].apply(limpiarCodigoImagen)

	tabla["Codigo_Categoria"]=tabla["Categoria_URL"].apply(limpiarCodigoImagen)

	tabla["Presidente_Codigo"]=tabla["Presidente_URL"].apply(limpiarCodigoImagen).apply(lambda codigo: None if not codigo or codigo=="nofoto_jugador" else int(codigo))

	tabla["Temporadas"]=tabla["Temporadas"].apply(lambda temporada: int(temporada) if temporada!="" else None)

	tabla["Presidente_URL"]=tabla["Presidente"].apply(lambda presidente: "-".join(presidente.lower().split(" ")) if presidente!="" else None)

	tabla["Presidente_Nombre"]=tabla["Presidente_Nombre"].apply(lambda nombre: nombre.strip() if nombre!="" else None)

	tabla["Presidente_Pais"]=tabla["Presidente_Pais"].apply(lambda pais: pais.strip() if pais!="" else None)

	tabla["Presidente_Ciudad"]=tabla["Presidente_Ciudad"].apply(lambda ciudad: ciudad.strip() if ciudad!="" else None)

	tabla["Presidente_Fecha"]=tabla["Presidente_Fecha"].apply(limpiarFecha)

	tabla["Presidente_Edad"]=tabla["Presidente_Edad"].apply(limpiarTiempo)

	tabla["Presidente_Cargo_Anos"]=tabla["Presidente_Cargo_Anos"].apply(limpiarTiempo)

	tabla["Presidente_Cargo_Meses"]=tabla["Presidente_Cargo_Meses"].apply(limpiarTiempo)

	tabla["Ciudad"]=tabla["Ciudad"].apply(lambda ciudad: ciudad.strip() if ciudad!="" else None)

	tabla["Estadio"]=tabla["Estadio"].apply(lambda estadio: estadio.strip() if estadio!="" else None)

	tabla["Fundacion"]=tabla["Fundacion"].apply(lambda fundacion: int(fundacion) if fundacion!="" else None)

	columnas=["Nombre", "Alias", "Siglas", "Pais","Codigo_Pais", "Ciudad", "Categoria", "Codigo_Categoria",
			"Temporadas", "Estadio", "Fundacion", "Presidente_Nombre", "Presidente_URL", "Presidente_Codigo"]

	return tabla[columnas]

def cargarDataEquipoDetalle(tabla:pd.DataFrame, equipo_id:str)->None:

	datos_equipo=tabla.values.tolist()[0]

	con=Conexion()

	if not con.existe_equipo(equipo_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar el equipo {equipo_id}. No existe")

	try:

		con.actualizarDatosEquipo(datos_equipo, equipo_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los datos del equipo {equipo_id}")