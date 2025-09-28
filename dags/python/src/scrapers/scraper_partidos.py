from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional
import itertools
import urllib.request
import json
import time
import random

from .excepciones_scrapers import PaginaError, PartidosEquipoError

from .configscrapers import URL, ENDPOINT_PARTIDOS, HEADERS

class ScraperPartidos:

    def __init__(self, equipo_id:int, ano:int)->None:

        self.equipo_id=equipo_id
        self.ano=ano

        self.url_scrapear=URL+f"{ENDPOINT_PARTIDOS}teamId={self.equipo_id}&season={self.ano}"

    def __realizarPeticion(self)->bs4:

        tiempo_sleep_random=0.5+random.random()*2.1

        time.sleep(tiempo_sleep_random)

        req=urllib.request.Request(self.url_scrapear, headers=HEADERS)

        try:

            with urllib.request.urlopen(req, timeout=10) as response:

                status_code=response.status

                final_url=response.geturl()

                text=response.read().decode("utf-8")

        except Exception as e:

            raise PaginaError(f"Error en la pagina: {e}")

        if status_code!=200 or not final_url.startswith(self.url_scrapear):

            print(f"Codigo de estado de la peticion: {status_code}")

            print(f"URL de la peticion: {final_url}")

            raise PaginaError("Error en la pagina")

        try:

            contenido_json=json.loads(text)["matches"]

        except Exception:

            raise PaginaError(f"Error en obtener el JSON {final_url}")

        if contenido_json and str(contenido_json).replace("\n", "").strip()=="":

            raise PaginaError(f"URL sin contenido JSON {final_url}")

        return bs4(str(contenido_json), "html.parser")

    def __obtenerPaneles(self, tabla_partidos:bs4)->List[bs4]:

        paneles=tabla_partidos.find_all("div", class_="panel")

        return [panel.find("div", class_="panel-body") for panel in paneles]

    def __obtenerPartidosPanel(self, panel:bs4)->List[List[str]]:

        partidos=panel.find_all("a")

        def limpiarPartido(partido:bs4)->List[str]:

            partido_id=partido["id"]

            link=partido["href"]

            estado=partido["data-status"]

            fecha_inicio=partido["starttime"]

            info=partido.find("div", class_="info-head").find("div", class_="middle-info").text

            equipos=[equipo.text.strip() for equipo in partido.find_all("div", class_="team-info")]

            marcador=partido.find("div", class_="marker").text.strip()

            fecha_str=partido.find("div", class_="date").text.strip()

            return [partido_id, link, estado, fecha_inicio, info]+equipos+[marcador, fecha_str]

        return list(map(limpiarPartido, partidos))

    def __obtenerPartidos(self, paneles:List[bs4])->None:

        partidos=list(map(self.__obtenerPartidosPanel, paneles))

        return list(itertools.chain.from_iterable(partidos))

    def __obtenerDataLimpia(self, paneles:List[bs4])->pd.DataFrame:

        partidos=self.__obtenerPartidos(paneles)

        columnas=["Partido_Id", "Link", "Estado", "Fecha_Inicio", "Competicion",
                    "Local", "Visitante", "Marcador", "Fecha_Str"]

        return pd.DataFrame(partidos, columns=columnas)

    def obtenerPartidosEquipo(self)->Optional[pd.DataFrame]:

        try:

            contenido=self.__realizarPeticion()

            paneles=self.__obtenerPaneles(contenido)

            return self.__obtenerDataLimpia(paneles)

        except Exception:

            raise PartidosEquipoError(f"Error en obtener los partidos del equipo: {self.equipo_id} del anno {self.ano}")