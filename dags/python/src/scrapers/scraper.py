from bs4 import BeautifulSoup as bs4
import urllib.request
import json
import time
import random

from .configscrapers import URL, HEADERS

from .excepciones_scrapers import PaginaError

class Scraper:

    def __init__(self, endpoint:str)->None:

        self.url_scrapear=URL+endpoint

    def __realizarPeticion(self)->bs4:

        tiempo_sleep_random=0.5+random.random()*2.1

        time.sleep(tiempo_sleep_random)

        req=urllib.request.Request(self.url_scrapear, headers=HEADERS)

        try:

            with urllib.request.urlopen(req, timeout=15) as response:

                status_code=response.status

                final_url=response.geturl()

                text=response.read().decode("utf-8")

        except Exception as e:

            raise PaginaError(f"Error en la pagina: {e}")

        if status_code!=200 or not final_url.startswith(self.url_scrapear):

            print(f"Codigo de estado de la peticion: {status_code}")

            print(f"URL de la peticion: {final_url}")

            raise PaginaError("Error en la pagina")

        return bs4(text,"html.parser")