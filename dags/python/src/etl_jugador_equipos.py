import pandas as pd
from typing import Optional

from .scrapers.scraper_jugador_equipos import ScraperJugadorEquipos

from .utils import limpiarCodigoImagen

from .database.conexion import Conexion

def extraerDataJugadorEquipos(jugador:str)->Optional[pd.DataFrame]:

	scraper=ScraperJugadorEquipos(jugador)

	return scraper.obtenerJugadorEquipos()

def limpiarDataJugadorEquipos(tabla:pd.DataFrame)->pd.DataFrame:

	tabla["Codigo_Equipo"]=tabla["Equipo_URL"].apply(limpiarCodigoImagen)

	tabla["Temporadas"]=tabla["Temporadas"].apply(lambda temporada: int(temporada.split(" ")[0]))

	tabla=tabla.astype({"Goles": int, "Partidos": int})

	columnas=["Codigo_Equipo", "Temporadas", "Goles", "Partidos"]

	return tabla[columnas]

def cargarDataJugadorEquipos(tabla:pd.DataFrame, jugador_id:str, entorno:str)->None:

	datos_jugador_equipos=tabla.values.tolist()

	con=Conexion(entorno)

	if not con.existe_jugador(jugador_id):

		con.cerrarConexion()

		raise Exception(f"Error al cargar los equipos del jugador {jugador_id}. No existe")


	try:

		for equipo_id, temporadas, goles, partidos in datos_jugador_equipos:

			if not con.existe_equipo(equipo_id):

				con.insertarEquipo(equipo_id)

			if not con.existe_equipo_jugador(jugador_id, equipo_id):

				con.insertarEquipoJugador((jugador_id, equipo_id, temporadas, goles, partidos))

			con.actualizarDatosEquipoJugador([temporadas, goles, partidos], jugador_id, equipo_id)

		con.cerrarConexion()

	except Exception:

		con.cerrarConexion()

		raise Exception(f"Error al cargar los datos de los equipos del jugador {jugador_id}")