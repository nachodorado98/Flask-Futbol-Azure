from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List

from .scraper import Scraper

from .excepciones_scrapers import PartidoCompeticionError

from .configscrapers import ENDPOINT_PARTIDO

class ScraperPartidoCompeticion(Scraper):

    def __init__(self, equipo_local:str, equipo_visitante:str, partido_id:str)->None:

        self.equipo_local=equipo_local
        self.equipo_visitante=equipo_visitante
        self.partido_id=partido_id

        super().__init__(f"{ENDPOINT_PARTIDO}/{self.equipo_local}/{self.equipo_visitante}/{self.partido_id}")

    def __contenido_competicion(self, contenido:bs4)->bs4:

        return contenido.find("h3", class_="competition")

    def __competicion_partido(self, competicion:bs4)->str:

        return competicion.find("a", href=True)["href"]

    def __obtenerDataLimpia(self, competicion:bs4)->pd.DataFrame:

        competicion_partido=self.__competicion_partido(competicion)

        columnas=["Competicion_URL"]

        return pd.DataFrame([competicion_partido], columns=columnas)

    def obtenerPartidoCompeticion(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            competicion=self.__contenido_competicion(contenido)

            return self.__obtenerDataLimpia(competicion)

        except Exception:

            raise PartidoCompeticionError(f"Error en obtener la competicion del partido: {self.equipo_local}/{self.equipo_visitante}/{self.partido_id}")