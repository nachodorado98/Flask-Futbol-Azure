import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional

from .scraper import Scraper

from .excepciones_scrapers import PaginaError, EntrenadorEquiposError

from .configscrapers import URL, ENDPOINT_ENTRENADOR

class ScraperEntrenadorEquipos(Scraper):

    def __init__(self, entrenador:str)->None:

        self.entrenador=entrenador

        super().__init__(f"{ENDPOINT_ENTRENADOR}/{self.entrenador}")

    def __contenido_contenedor_entrenados(self, contenido:bs4)->bs4:

        return contenido.find("div", id="mod_coach_trained_teams").find("div", class_="panel-body table-list team-result").find("table")

    def __informacion_equipos(self, contenedor:bs4)->List:

        filas_equipos=contenedor.find("tbody").find_all("tr", class_="row-body")[:-1]

        def obtenerEquipoStats(fila:bs4)->tuple:

            equipo_url=fila.find("a", href=True)["href"]

            return tuple([equipo_url]+[valor.text for valor in fila.find_all("td")[2:9]])

        return list(map(lambda fila: obtenerEquipoStats(fila), filas_equipos)) 

    def __obtenerDataLimpia(self, contenedor:bs4)->pd.DataFrame:

        filas_datos=self.__informacion_equipos(contenedor)

        columnas=["Equipo_URL", "Partidos_Totales", "Desde", "Hasta", "Ganados", "Empatados", "Perdidos", "Tactica"]

        return pd.DataFrame(filas_datos, columns=columnas)

    def obtenerEntrenadorEquipos(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            contenedor=self.__contenido_contenedor_entrenados(contenido)

            return self.__obtenerDataLimpia(contenedor)

        except Exception:

            raise EntrenadorEquiposError(f"Error en obtener los equipos del entrenador: {self.entrenador}")