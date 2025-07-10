from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List
import requests

from .scraper import Scraper

from .excepciones_scrapers import CompeticionError, PaginaError

from .configscrapers import ENDPOINT_COMPETICION_INFO, ENDPOINT_COMPETICION_RESULTADOS

class ScraperCompeticion(Scraper):

    def __init__(self, competicion:str)->None:

        self.competicion=competicion

        super().__init__(f"{ENDPOINT_COMPETICION_INFO}/{self.competicion}")

    def _Scraper__realizarPeticion(self)->bs4:

        peticion=requests.get(self.url_scrapear)

        url_peticion=peticion.url

        urls_validas=[ENDPOINT_COMPETICION_INFO, ENDPOINT_COMPETICION_RESULTADOS]

        if peticion.status_code!=200 or not any(url in url_peticion for url in urls_validas):

            print(f"Codigo de estado de la peticion: {peticion.status_code}")

            print(f"URL de la peticion: {peticion.url}")
            
            raise PaginaError("Error en la pagina")

        return bs4(peticion.text,"html.parser")

    def __contenido_cabecera(self, contenido:bs4)->bs4:

        return contenido.find("div", class_="head-info fixed-w-scroll")

    def __informacion_nombre(self, cabecera:bs4)->str:

        try:

            titulo_nombre=cabecera.find("div", class_="head-content").find("div", class_="head-title")

            return titulo_nombre.text.strip()

        except Exception:

            return ""

    def __informacion_logo_pais(self, cabecera:bs4)->tuple:

        fila_cabecera=cabecera.find("div", class_="bottom-row")

        def obtenerLogo(fila_cabecera:bs4)->str:

            imagen=fila_cabecera.find("div", class_="img-container")

            return imagen.find("img", src=True)["src"].split("?")[0].strip()

        def obtenerPais(fila_cabecera:bs4)->str:

            imagen=fila_cabecera.find("div", class_="data-boxes")

            return imagen.find("img", src=True)["src"].split("?")[0].strip()

        try:

            return obtenerLogo(fila_cabecera), obtenerPais(fila_cabecera)

        except Exception:

            return "", ""

    def __obtenerDataLimpia(self, cabecera:bs4)->pd.DataFrame:

        nombre=self.__informacion_nombre(cabecera)

        logo, pais=self.__informacion_logo_pais(cabecera)

        fila_datos_unificados=[nombre, logo, pais]

        columnas=["Nombre", "Logo_URL", "Pais_URL"]

        return pd.DataFrame([fila_datos_unificados], columns=columnas)

    def obtenerCompeticion(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            cabecera=self.__contenido_cabecera(contenido)

            return self.__obtenerDataLimpia(cabecera)

        except Exception:

            raise CompeticionError(f"Error en obtener los datos de la competicion: {self.competicion}")