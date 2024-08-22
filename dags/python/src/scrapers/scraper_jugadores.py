import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional, Dict
import itertools

from .excepciones_scrapers import PaginaError, JugadoresEquipoError

from .configscrapers import URL, ENDPOINT_JUGADORES

class ScraperJugadores:

    def __init__(self, equipo_id:int, ano:int)->None:

        self.equipo_id=equipo_id
        self.ano=ano

        self.url_scrapear=URL+f"{ENDPOINT_JUGADORES}teamId={self.equipo_id}&season={self.ano}"

    def __realizarPeticion(self)->bs4:

        peticion=requests.get(self.url_scrapear)

        if peticion.status_code!=200 or not peticion.url.startswith(self.url_scrapear):

            print(f"Codigo de estado de la peticion: {peticion.status_code}")

            print(f"URL de la peticion: {peticion.url}")
            
            raise PaginaError("Error en la pagina")

        try:

            contenido_json=peticion.json()["data"]["players"]

        except Exception:

            print(f"Error en obtener el JSON {peticion.url}")

            raise PaginaError("Error en la pagina")

        if not contenido_json:

            print(f"URL sin contenido JSON {peticion.url}")

            raise PaginaError("Error en la pagina")

        return contenido_json

    def __obtenerDataLimpia(self, contenido:List[Dict])->pd.DataFrame:

        return pd.DataFrame(contenido)

    def obtenerJugadoresEquipo(self)->Optional[pd.DataFrame]:

        try:

            contenido=self.__realizarPeticion()

            return self.__obtenerDataLimpia(contenido)

        except Exception:

            raise JugadoresEquipoError(f"Error en obtener los jugadores del equipo: {self.equipo_id} del anno {self.ano}")