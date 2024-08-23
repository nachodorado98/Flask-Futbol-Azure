import pandas as pd
from typing import Optional

from .scrapers.scraper_jugadores import ScraperJugadores

from .database.conexion import Conexion

def extraerDataJugadoresEquipo(equipo_id:int, ano:int)->Optional[pd.DataFrame]:

	scraper=ScraperJugadores(equipo_id, ano)

	return scraper.obtenerJugadoresEquipo()

def limpiarDataJugadoresEquipo(tabla:pd.DataFrame)->Optional[pd.DataFrame]:

	columnas=["alias"]

	return tabla[columnas]

def cargarDataJugadoresEquipo(tabla:pd.DataFrame)->None:

	jugadores=[jugador[0] for jugador in tabla.values.tolist()]

	con=Conexion()

	for jugador in jugadores:

		if not con.existe_jugador(jugador):

			con.insertarJugador(jugador)

	con.cerrarConexion()