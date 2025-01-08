import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional

from .scraper import Scraper

from .excepciones_scrapers import PaginaError, JugadorSeleccionError

from .configscrapers import URL, ENDPOINT_JUGADOR

class ScraperJugadorSeleccion(Scraper):

	def __init__(self, jugador:str)->None:

		self.jugador=jugador

		super().__init__(f"{ENDPOINT_JUGADOR}/{self.jugador}")

	def __contenido_contenedor_seleccion(self, contenido:bs4)->bs4:

		return contenido.find("div", id="mod_player_sel_info").find("div", class_="panel player-sel")

	def __informacion_basica(self, contenedor:bs4)->tuple:

		contenedor_info=contenedor.find("div", class_="panel-body")

		contenido_seleccion=contenedor_info.find("div", class_="box-content")

		imagen_seleccion=contenido_seleccion.find("div", class_="img-box").find("img", src=True)["src"]

		convocatorias=contenido_seleccion.find("div", class_="mb5 main-text").text.strip()

		return imagen_seleccion, convocatorias

	def __informacion_stats(self, contenedor:bs4)->List[int]:

   		columnas_stats=contenedor.find("div", class_="panel-body item-column-list").find_all("div", class_="item-col")

   		def obtenerStat(columna:bs4)->int:

   			try:

   				return columna.find("div", class_="main-line").text.strip()

   			except Exception:

   				return None

   		return list(map(lambda columna: obtenerStat(columna), columnas_stats))

	def __obtenerDataLimpia(self, contenedor:bs4)->pd.DataFrame:

	    imagen, convocatorias=self.__informacion_basica(contenedor)

	    goles, media, asistencias, amarillas, rojas=self.__informacion_stats(contenedor)

	    fila_datos_unificados=[imagen, convocatorias, goles, media, asistencias, amarillas, rojas]

	    columnas=["Codigo_Seleccion", "Convocatorias", "Goles", "Media", "Asistencias", "Amarillas", "Rojas"]

	    return pd.DataFrame([fila_datos_unificados], columns=columnas)

	def obtenerJugadorSeleccion(self)->Optional[pd.DataFrame]:

	    try:

	        contenido=self._Scraper__realizarPeticion()

	        contenedor=self.__contenido_contenedor_seleccion(contenido)

	        return self.__obtenerDataLimpia(contenedor)

	    except Exception:

	        raise JugadorSeleccionError(f"Error en obtener la seleccion del jugador: {self.jugador}")