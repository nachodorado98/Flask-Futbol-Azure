from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List
import itertools

from .scraper import Scraper

from .excepciones_scrapers import EquipoEscudoError

from .configscrapers import ENDPOINT_EQUIPO

class ScraperEquipoEscudo(Scraper):

    def __init__(self, equipo:str)->None:

        self.equipo=equipo

        super().__init__(f"{ENDPOINT_EQUIPO}/{self.equipo}")

    def __contenido_tabla_cabecera(self, contenido:bs4)->Optional[bs4]:

        return contenido.find("div", class_="head-content fws-hide player-head text-center").find("div", class_="bottom-row")

    def __obtener_escudo(self, tabla_cabecera:bs4)->List[str]:

        info_imagenes=tabla_cabecera.find("div", class_="img-container").find_all("img", src=True)

        def obtenerImagen(fila:bs4)->str:

            return fila["src"].split("?")[0].strip()

        return list(map(obtenerImagen, info_imagenes))[-1]

    def __obtener_puntuacion(self, tabla_cabecera:bs4)->List[str]:

        puntuacion=tabla_cabecera.find("div", class_="data-boxes ta-c").find("span")

        return "0" if not puntuacion else puntuacion.text

    def __obtenerDataLimpia(self, tabla_cabecera:bs4)->pd.DataFrame:

        escudo=self.__obtener_escudo(tabla_cabecera)

        puntuacion=self.__obtener_puntuacion(tabla_cabecera)

        fila_datos_unificados=[escudo, puntuacion]

        columnas=["Escudo", "Puntuacion"]

        return pd.DataFrame([fila_datos_unificados], columns=columnas)

    def obtenerEscudoEquipo(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            tabla_cabecera=self.__contenido_tabla_cabecera(contenido)

            return self.__obtenerDataLimpia(tabla_cabecera)

        except Exception:

            raise EquipoEscudoError(f"Error en obtener el escudo del equipo: {self.equipo}")