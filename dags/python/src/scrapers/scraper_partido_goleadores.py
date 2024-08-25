from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List

from .scraper import Scraper

from .excepciones_scrapers import PartidoGoleadoresError

from .configscrapers import ENDPOINT_PARTIDO

class ScraperPartidoGoleadores(Scraper):

    def __init__(self, equipo_local:str, equipo_visitante:str, partido_id:str)->None:

        self.equipo_local=equipo_local
        self.equipo_visitante=equipo_visitante
        self.partido_id=partido_id

        super().__init__(f"{ENDPOINT_PARTIDO}/{self.equipo_local}/{self.equipo_visitante}/{self.partido_id}")

    def __contenido_eventos_partido(self, contenido:bs4)->Optional[bs4]:

        try:

            return contenido.find("section", class_="match-events").find("div", id="orderEvent")

        except Exception:

            raise PartidoGoleadoresError(f"Error en obtener los goleadores del partido: {self.equipo_local}/{self.equipo_visitante}/{self.partido_id}. No existen eventos")

    def __contenido_goleadores_partido(self, eventos_partido:bs4)->Optional[bs4]:

        paneles=eventos_partido.find_all("div", class_="panel")

        def filtrarPanel(panel_fitrar:List[bs4], tipo_panel:str)->bool:

            titulo_panel=panel_fitrar.find("h2")

            if not titulo_panel:

                return False

            return True if titulo_panel.text==tipo_panel else False

        panel_goleadores=list(filter(lambda panel: filtrarPanel(panel, "Goles"), paneles))

        if not panel_goleadores:

            raise PartidoGoleadoresError(f"Error en obtener los goleadores del partido: {self.equipo_local}/{self.equipo_visitante}/{self.partido_id}. No existen goles")

        else:

            return panel_goleadores[0].find("div", class_="table-body")

    def __obtener_lista_goleadores(self, contenido_goleadores:bs4)->List[tuple]:

        filas=contenido_goleadores.find_all("div", class_="table-played-match")

        def obtenerGoleadorMinuto(fila:bs4)->tuple:

            minuto=fila.find("div", class_="col-mid-rows").text.strip()

            columnas=fila.find_all("div", class_="col-side")

            goleador_local=columnas[0].find("a", href=True)

            goleador_visitante=columnas[1].find("a", href=True)

            return (goleador_visitante["href"], minuto, 2) if not goleador_local else (goleador_local["href"], minuto, 1)

        return list(map(obtenerGoleadorMinuto, filas))

    def __goleadores(self, eventos_partido:bs4)->Optional[List[tuple]]:

        contenido_goleadores=self.__contenido_goleadores_partido(eventos_partido)

        return self.__obtener_lista_goleadores(contenido_goleadores)

    def __obtenerDataLimpia(self, eventos_partido:bs4)->pd.DataFrame:

        goleadores=self.__goleadores(eventos_partido)

        columnas=["Jugador_URL", "Minuto", "Equipo"]

        return pd.DataFrame(goleadores, columns=columnas)

    def obtenerPartidoGoleadores(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            contenido_eventos=self.__contenido_eventos_partido(contenido)

            return self.__obtenerDataLimpia(contenido_eventos)

        except Exception:

            raise PartidoGoleadoresError(f"Error en obtener los goleadores del partido: {self.equipo_local}/{self.equipo_visitante}/{self.partido_id}")