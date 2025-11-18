import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional

from .scraper import Scraper

from .excepciones_scrapers import PaginaError, EntrenadorPalmaresError

from .configscrapers import URL, ENDPOINT_ENTRENADOR

class ScraperEntrenadorPalmares(Scraper):

	def __init__(self, entrenador:str)->None:

		self.entrenador=entrenador

		super().__init__(f"{ENDPOINT_ENTRENADOR}/{self.entrenador}")

	def __contenido_tabla_palmares(self, contenido:bs4)->Optional[bs4]:

		try:

			return contenido.find("div", id="mod_coach_title").find("div", class_="panel-body pn")

		except Exception:

			raise EntrenadorPalmaresError(f"Error en obtener el palmares del entrenador: {self.entrenador}. No existe")

	def __obtener_tablas_titulos(self, tabla_palmares:bs4)->List[bs4]:

		tabla=tabla_palmares.find("table", class_="table")

		def datos_titulo(datos:bs4)->List[str]:

			imagen=datos.find("td", class_="td-medal").find("img", src=True)["src"].split("?")[0].strip()

			contenedor_titulo=datos.find("td", class_="ta-l medals")

			nombre=contenedor_titulo.find("p").text

			datos_annos=contenedor_titulo.find_all("a", href=True)

			annos=[dato.text.strip() for dato in datos_annos]

			annos_unidos=";".join(annos)

			competicion=[dato["href"].split("info/")[-1].split("/")[0].strip() for dato in datos_annos][0]

			return (nombre, competicion, imagen, annos_unidos)

		filas=tabla.find_all("tr")[1:]

		return list(map(lambda fila: datos_titulo(fila), filas))

	def __obtenerDataLimpia(self, tabla_palmares:bs4)->pd.DataFrame:

		fila_datos=self.__obtener_tablas_titulos(tabla_palmares)

		columnas=["Nombre", "Competicion", "Imagen_Titulo", "Annos"]

		return pd.DataFrame(fila_datos, columns=columnas)

	def obtenerEntrenadorPalmares(self)->Optional[pd.DataFrame]:

		try:

			contenido=self._Scraper__realizarPeticion()

			tabla_palmares=self.__contenido_tabla_palmares(contenido)

			return self.__obtenerDataLimpia(tabla_palmares)

		except Exception:

			raise EntrenadorPalmaresError(f"Error en obtener el palmares del entrenador: {self.entrenador}")