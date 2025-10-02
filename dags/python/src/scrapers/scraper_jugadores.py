from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional, Dict
import urllib.request
import json
import time
import random

from .excepciones_scrapers import PaginaError, JugadoresEquipoError

from .configscrapers import URL, ENDPOINT_JUGADORES, HEADERS, TIEMPO_BASE, MULTIPLICADOR

class ScraperJugadores:

    def __init__(self, equipo_id:int, ano:int)->None:

        self.equipo_id=equipo_id
        self.ano=ano

        self.url_scrapear=URL+f"{ENDPOINT_JUGADORES}teamId={self.equipo_id}&season={self.ano}"

    def __realizarPeticion(self)->List[Dict]:

        tiempo_sleep_random=TIEMPO_BASE+random.random()*MULTIPLICADOR

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

            contenido_json=json.loads(text)["data"]["players"]

        except Exception:

            raise PaginaError(f"Error en obtener el JSON {final_url}")

        if not contenido_json:

            print(f"URL sin contenido JSON {final_url}")

            raise PaginaError(f"URL sin contenido JSON {final_url}")

        return contenido_json

    def __obtenerDataLimpia(self, contenido:List[Dict])->pd.DataFrame:

        return pd.DataFrame(contenido)

    def obtenerJugadoresEquipo(self)->Optional[pd.DataFrame]:

        try:

            contenido=self.__realizarPeticion()

            return self.__obtenerDataLimpia(contenido)

        except Exception:

            raise JugadoresEquipoError(f"Error en obtener los jugadores del equipo: {self.equipo_id} del anno {self.ano}")