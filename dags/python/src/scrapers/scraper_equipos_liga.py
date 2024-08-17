from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List

from .scraper import Scraper

from .excepciones_scrapers import EquiposLigaError

from .configscrapers import ENDPOINT_COMPETICION

class ScraperEquiposLiga(Scraper):

    def __init__(self, nombre_liga:str)->None:

        self.nombre_liga=nombre_liga

        super().__init__(f"{ENDPOINT_COMPETICION}/{self.nombre_liga}")

    def __contenido_a_tabla_general(self, contenido:bs4)->bs4:

        return contenido.find("div", id="classificationTables")

    def __tabla_general_tabla_total(self, tabla:bs4)->bs4:

        return tabla.find("div", id="tab_total0").find("table").find("tbody")

    def __contenido_a_tabla(self, contenido:bs4)->bs4:

        tabla_general=self.__contenido_a_tabla_general(contenido)

        return self.__tabla_general_tabla_total(tabla_general)

    def __obtenerColumnasSemiVacias(self, tabla:bs4)->List[str]:

        cabecera=tabla.find("tr", class_="row-head").find_all("th")

        return [columna.text for columna in cabecera]

    def __obtenerColumnas(self, tabla:bs4)->List[str]:

        columnas_semi_vacias=self.__obtenerColumnasSemiVacias(tabla)

        columnas_llenas=[columna for columna in columnas_semi_vacias if columna!=""]

        return ["Posicion", "Escudo", "Nombre"]+columnas_llenas

    def __obtenerFilas(self, tabla:bs4)->List[bs4]:

        return tabla.find_all("tr", class_="row-body")

    def __obtenerContenidoFilas(self, filas:List[bs4])->List[tuple]:

        celdas_filas=[fila.find_all("td") for fila in filas]

        def posicion(celda:bs4)->int:

            return int(celda.find("div").text)

        def escudo(celda:bs4)->str:

            return celda.find("div").find("img", src=True)["src"].split("?")[0]

        def nombre(celda:bs4)->str:

            return celda.find("a").find("span").text

        def nombre_url(celda:bs4)->str:

            return celda.find("a", href=True)["href"].split("/")[-1]

        def stat(celda:bs4)->int:

            try:

                return int(celda.text.strip(""))

            except Exception:

                return None

        def obtenerFilaLimpia(fila:bs4)->tuple:

            return (posicion(fila[0]),
                    escudo(fila[1]),
                    nombre(fila[2]),
                    stat(fila[3]),
                    stat(fila[4]),
                    stat(fila[5]),
                    stat(fila[6]),
                    stat(fila[7]),
                    stat(fila[8]),
                    stat(fila[9]),
                    stat(fila[10]),
                    nombre_url(fila[2]))

        return [obtenerFilaLimpia(fila) for fila in celdas_filas]

    def __obtenerDataLimpia(self, tabla:bs4)->pd.DataFrame:

        columnas=self.__obtenerColumnas(tabla)

        filas=self.__obtenerFilas(tabla)

        contenido_filas=self.__obtenerContenidoFilas(filas)

        return pd.DataFrame(contenido_filas, columns=columnas+["Nombre_URL"])

    def obtenerClasificacionLiga(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            tabla=self.__contenido_a_tabla(contenido)

            return self.__obtenerDataLimpia(tabla)

        except Exception:

            raise EquiposLigaError(f"Error en obtener los equipos de la liga: {self.nombre_liga}")