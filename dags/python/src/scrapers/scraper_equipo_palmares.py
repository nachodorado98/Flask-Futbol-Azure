from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List

from .scraper import Scraper

from .excepciones_scrapers import EquipoPalmaresError

from .configscrapers import ENDPOINT_EQUIPO

class ScraperEquipoPalmares(Scraper):

    def __init__(self, equipo:str)->None:

        self.equipo=equipo

        super().__init__(f"{ENDPOINT_EQUIPO}/palmares/{self.equipo}")

    def __contenido_tabla_palmares(self, contenido:bs4)->Optional[bs4]:

        try:

            return contenido.find("div", id="mod_honours").find("div", class_="panel")

        except Exception:

            raise EquipoPalmaresError(f"Error en obtener el palmares del equipo: {self.equipo}. No existe")

    def __obtener_tablas_titulos(self, tabla_palmares:bs4)->List[bs4]:

        tablas=tabla_palmares.find_all("table", class_="table")

        def datos_genericos_titulo(datos:bs4)->List[str]:

            numero=datos.find("td", class_="t-up w-60").text

            nombre=datos.find("td", class_="ta-l t-up").text

            imagen=datos.find("img", src=True)["src"].split("?")[0].strip()

            return [numero, nombre, imagen]

        def datos_especificos_titulo(datos:bs4)->List[str]:

            imagen_titulo=datos.find("img", src=True)["src"].split("?")[0].strip()

            datos_annos=datos.find("div", class_="season-wrapper").find_all("a")

            annos=[dato.text.strip() for dato in datos_annos]

            annos_unidos=";".join(annos)

            return [imagen_titulo, annos_unidos]

        def obtenerDatosTitulo(tabla:bs4)->tuple:

            filas=tabla.find_all("tr")

            datos_genericos=datos_genericos_titulo(filas[0])

            datos_especificos=datos_especificos_titulo(filas[1])

            return tuple(datos_genericos+datos_especificos)

        return list(map(lambda tabla: obtenerDatosTitulo(tabla), tablas))

    def __obtenerDataLimpia(self, tabla_palmares:bs4)->pd.DataFrame:

        fila_datos=self.__obtener_tablas_titulos(tabla_palmares)

        columnas=["Numero", "Nombre", "Imagen_Competicion", "Imagen_Titulo", "Annos"]

        return pd.DataFrame(fila_datos, columns=columnas)

    def obtenerEstadioPalmares(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            tabla_palmares=self.__contenido_tabla_palmares(contenido)

            return self.__obtenerDataLimpia(tabla_palmares)

        except Exception:

            raise EquipoPalmaresError(f"Error en obtener el palmares del equipo: {self.equipo}")