import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional

from .scraper import Scraper

from .excepciones_scrapers import PaginaError, EstadioError

from .configscrapers import URL, ENDPOINT_ESTADIO

class ScraperEstadio(Scraper):

    def __init__(self, estadio:str)->None:

        self.estadio=estadio

        super().__init__(f"{ENDPOINT_ESTADIO}/{self.estadio}")

    def __contenido_tabla_estadio(self, contenido:bs4)->Optional[bs4]:

        try:

            return contenido.find("div", id="mod_stadium_stats").find("div", class_="panel team-stats")

        except Exception:

            raise EstadioError("Error en obtener los datos del estadio")

    def __imagen_estadio(self, tabla_estadio:bs4)->str:

        imagen_estadio=tabla_estadio.find("div", class_="panel-body pn")

        try:

            return imagen_estadio.find("img", src=True)["src"].split("?")[0].strip()

        except Exception:

            return "https://cdn.resfu.com/img_data/estadios/original_new/estadio_nofoto.png"

    def __informacion_datos_estadio(self, tabla_estadio:bs4)->bs4:

        return tabla_estadio.find("div", class_="panel-body table-list").find("div", class_="table-body")

    def __tabla_ubicacion_pais(self, tabla_datos:bs4)->tuple:

        filas=tabla_datos.find_all("div", class_="table-row")

        def obtenerContenedorFila(fila:bs4)->List[tuple]:

            celdas=fila.find_all("div")

            return celdas[1]

        filas_contenedores=[obtenerContenedorFila(fila) for fila in filas]

        ubicacion=filas_contenedores[0].text.strip()

        pais=filas_contenedores[1].text.strip()

        pais_url=filas_contenedores[1].find("img", src=True)["src"].split("?")[0].strip()

        return ubicacion, pais, pais_url

    def __informacion_ubicacion_pais(self, tabla_estadio:bs4)->tuple:

        try:

            tabla_datos=self.__informacion_datos_estadio(tabla_estadio)

            return self.__tabla_ubicacion_pais(tabla_datos)

        except Exception:

            ("","","")
    
    def __obtenerDataLimpia(self, tabla_estadio:bs4)->pd.DataFrame:

        codigo_estadio=self.__imagen_estadio(tabla_estadio)

        direccion, pais, pais_url=self.__informacion_ubicacion_pais(tabla_estadio)

        fila_datos_unificados=[codigo_estadio, direccion, pais, pais_url]

        columnas=["Codigo_Estadio", "Direccion", "Pais", "Pais_URL"]

        return pd.DataFrame([fila_datos_unificados], columns=columnas)

    def obtenerEstadio(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            tabla_estadio=self.__contenido_tabla_estadio(contenido)

            return self.__obtenerDataLimpia(tabla_estadio)

        except Exception:

            raise EstadioError(f"Error en obtener el estadio: {self.estadio}")