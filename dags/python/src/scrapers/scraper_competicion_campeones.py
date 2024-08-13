from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List

from .scraper import Scraper

from .excepciones_scrapers import CompeticionCampeonesError

from .configscrapers import ENDPOINT_COMPETICION_CAMPEONES

class ScraperCompeticionCampeones(Scraper):

    def __init__(self, competicion:str)->None:

        self.competicion=competicion

        super().__init__(f"{ENDPOINT_COMPETICION_CAMPEONES}/{self.competicion}")

    def __contenido_campeones(self, contenido:bs4)->bs4:

        return contenido.find("div", id="mod_last_champions").find("div", class_="panel last-champions")

    def __obtener_campeones(self, contenido_campeones:bs4)->List[List[str]]:

        tabla=contenido_campeones.find("div", class_="panel-body pn")

        filas=tabla.find_all("li")

        def limpiarFila(fila:bs4)->List[str]:

            div_izquierda=fila.find("div", class_="left-content")

            try:

                ano=div_izquierda.find("div", class_="desc-boxes color-grey2").text.strip()

                equipo=div_izquierda.find("a", href=True)["href"]

                return [ano, equipo]

            except Exception:

                return [None, None]

        return list(map(lambda fila: limpiarFila(fila), filas))

    def __obtenerDataLimpia(self, contenido_campeones:bs4)->pd.DataFrame:

        campeones=self.__obtener_campeones(contenido_campeones)

        columnas=["Ano", "Equipo_URL"]

        return pd.DataFrame(campeones, columns=columnas)

    def obtenerCampeonesCompeticion(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            campeones=self.__contenido_campeones(contenido)

            return self.__obtenerDataLimpia(campeones)

        except Exception:

            raise CompeticionCampeonesError(f"Error en obtener los datos de los campeones de la competicion: {self.competicion}")