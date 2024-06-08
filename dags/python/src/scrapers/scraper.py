import requests
from bs4 import BeautifulSoup as bs4

from .configscrapers import URL

from .excepciones_scrapers import PaginaError

class Scraper:

    def __init__(self, endpoint:str)->None:

        self.url_scrapear=URL+endpoint

    def __realizarPeticion(self)->bs4:

        peticion=requests.get(self.url_scrapear)

        if peticion.status_code!=200 or not peticion.url.startswith(self.url_scrapear):

            print(f"Codigo de estado de la peticion: {peticion.status_code}")

            print(f"URL de la peticion: {peticion.url}")
            
            raise PaginaError("Error en la pagina")

        return bs4(peticion.text,"html.parser")