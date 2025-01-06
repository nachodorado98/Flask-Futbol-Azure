import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional

from .scraper import Scraper

from .excepciones_scrapers import PaginaError, JugadorEquiposError

from .configscrapers import URL, ENDPOINT_JUGADOR

class ScraperJugadorEquipos(Scraper):

    def __init__(self, jugador:str)->None:

        self.jugador=jugador

        super().__init__(f"{ENDPOINT_JUGADOR}/{self.jugador}")

    def __contenido_contenedor_scroll(self, contenido:bs4)->bs4:

        return contenido.find("div", id="mod_player_teams").find("div", class_="panel-body")

    def __informacion_equipos(self, contenedor:bs4)->List:

        boxes=contenedor.find("div", class_="scroll-boxes").find_all("div", "scroll-box circle")

        def obtenerEquipoStats(box:bs4)->tuple:

            equipo_url=box.find("a", href=True)["href"]

            info=box.find("a")

            def infoEquipo(info:bs4)->str:

                info_equipo=info.find("div", class_="info-wrapper").find("div", class_="name")

                return info_equipo.find("div", class_="other-line").text

            def infoStats(info:bs4)->tuple:

                info_stats=info.find("div", class_="event-wrapper").find_all("div", class_="side-col")

                return (stat.text.strip() for stat in info_stats)

            temporadas=infoEquipo(info)

            goles, partidos=infoStats(info)

            return equipo_url, temporadas, goles, partidos

        return list(map(lambda box: obtenerEquipoStats(box), boxes)) 

    def __obtenerDataLimpia(self, contenedor:bs4)->pd.DataFrame:

        filas_datos=self.__informacion_equipos(contenedor)

        columnas=["Equipo_URL", "Temporadas", "Goles", "Partidos"]

        return pd.DataFrame(filas_datos, columns=columnas)

    def obtenerJugadorEquipos(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            contenedor=self.__contenido_contenedor_scroll(contenido)

            return self.__obtenerDataLimpia(contenedor)

        except Exception:

            raise JugadorEquiposError(f"Error en obtener los equipos del jugador: {self.jugador}")