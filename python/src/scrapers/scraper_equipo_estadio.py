from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List

from .scraper import Scraper

from .excepciones_scrapers import EquipoEstadioError

from .configscrapers import ENDPOINT_EQUIPO

class ScraperEquipoEstadio(Scraper):

    def __init__(self, equipo:str)->None:

        self.equipo=equipo

        super().__init__(f"{ENDPOINT_EQUIPO}/{self.equipo}")

    def __contenido_tabla_estadio(self, contenido:bs4)->Optional[bs4]:

        try:

            return contenido.find("div", id="mod_stadium").find("div", class_="panel stadiums")

        except Exception:

            raise EquipoEstadioError(f"Error en obtener el estadio del equipo: {self.equipo}. No existe")

    def __imagen_estadio(self, tabla_estadio:bs4)->str:

        imagen_estadio=tabla_estadio.find("div", class_="panel-body").find("div", class_="image-box")

        return imagen_estadio.find("img", src=True)["src"].split("?")[0].strip()

    def __informacion_datos_estadio(self, tabla_estadio:bs4)->bs4:

        return tabla_estadio.find("div", class_="panel-body table-list").find("div", class_="table-body")

    def __tabla_nombre_ubicacion(self, tabla_datos:bs4)->tuple:

        tabla_nombre_ubicacion=tabla_datos.find("div", class_="head-wrapper ta-c")

        nombre=tabla_nombre_ubicacion.find("div", class_="name").text.strip()

        ciudad=tabla_nombre_ubicacion.find("div", class_="city mv5").text.strip()

        direccion=tabla_nombre_ubicacion.find("div", class_="address color-grey2").text.strip()

        return nombre, ciudad, direccion

    def __informacion_nombre_ubicacion(self, tabla_estadio:bs4)->tuple:

        try:

            tabla_datos=self.__informacion_datos_estadio(tabla_estadio)

            return self.__tabla_nombre_ubicacion(tabla_datos)

        except Exception:

            ("","","")

    def __tabla_datos_tecnicos(self, tabla_datos:bs4)->tuple:

        filas=tabla_datos.find_all("div", class_="table-row")

        def obtenerContenidoFila(fila:bs4)->List[tuple]:

            celdas=fila.find_all("div")

            return celdas[0].text, celdas[1].text

        filas_limpias=[obtenerContenidoFila(fila) for fila in filas]

        def comprobarCampo(filas:str, campo:str)->bool:

            return False if not list(filter(lambda fila: fila[0]==campo, filas)) else True

        for campo in ["Fecha construcción", "Capacidad", "Tamaño", "Tipo de césped", "Teléfono", "Fax"]:

            condicion_campo=comprobarCampo(filas_limpias, campo)

            if not condicion_campo:

                filas_limpias.append((campo, ""))

        filas_ordenadas=sorted(filas_limpias)

        return list(map(lambda fila: fila[1], filas_ordenadas))

    def __informacion_datos_tecnicos(self, tabla_estadio:bs4)->List[str]:

        try:

            tabla_datos=self.__informacion_datos_estadio(tabla_estadio)

            return self.__tabla_datos_tecnicos(tabla_datos)

        except Exception:

            [""]*6

    def __obtenerDataLimpia(self, tabla_estadio:bs4)->pd.DataFrame:

        nombre, ciudad, direccion=self.__informacion_nombre_ubicacion(tabla_estadio)

        datos_tecnicos=self.__informacion_datos_tecnicos(tabla_estadio)

        fila_datos_unificados=[nombre, ciudad, direccion]+datos_tecnicos

        columnas=["Nombre", "Ciudad", "Direccion", "Capacidad", "Fax", "Fecha construccion", "Tamaño",
                    "Telefono", "Cesped"]

        return pd.DataFrame([fila_datos_unificados], columns=columnas)

    def obtenerEstadioEquipo(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            tabla_estadio=self.__contenido_tabla_estadio(contenido)

            return self.__obtenerDataLimpia(tabla_estadio)

        except Exception:

            raise EquipoEstadioError(f"Error en obtener el estadio del equipo: {self.equipo}")