from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List
import itertools

from .scraper import Scraper

from .excepciones_scrapers import EquipoEntrenadorError

from .configscrapers import ENDPOINT_EQUIPO

class ScraperEquipoEntrenador(Scraper):

    def __init__(self, equipo:str)->None:

        self.equipo=equipo

        super().__init__(f"{ENDPOINT_EQUIPO}/{self.equipo}")

    def __contenido_tabla_entrenador(self, contenido:bs4)->Optional[bs4]:

        try:

            return contenido.find("div", id="mod_coachStats").find("div", class_="panel team-coach-stats").find("div", class_="item-column-list align-center")

        except Exception:

            raise EquipoEntrenadorError(f"Error en obtener el entrenador del equipo: {self.equipo}. No existe")

    def __obtener_entrenador(self, tabla_entrenador:bs4)->List[str]:

        info_entrenador=tabla_entrenador.find("a").find("div")

        info_imagenes=info_entrenador.find("div", class_="posr mb5").find_all("img", src=True)

        def obtenerImagen(fila:bs4)->str:

            return fila["src"].split("?")[0].strip()

        imagenes=list(map(obtenerImagen, info_imagenes))

        info_personal_entrenador=info_entrenador.find("div", class_="text-box").find_all("p")

        datos_personales=[info.text.strip() for info in info_personal_entrenador]

        return datos_personales+imagenes

    def __obtener_estadisticas(self, tabla_entrenador:bs4)->List[str]:

        info_estadisticas=tabla_entrenador.find_all("div", class_="item-col")

        def obtenerContenido(columna:bs4)->List[str]:

            return [col.text for col in columna.find_all("div")]

        columnas=[obtenerContenido(info)[1:] for info in info_estadisticas]

        return list(itertools.chain(*columnas))

    def __obtenerDataLimpia(self, tabla_entrenador:bs4)->pd.DataFrame:

        datos_entrenador=self.__obtener_entrenador(tabla_entrenador)

        datos_estadisticas=self.__obtener_estadisticas(tabla_entrenador)

        fila_datos_unificados=datos_entrenador+datos_estadisticas

        columnas=["Nombre", "Fecha", "Edad", "Pais_URL", "Entrenador_URL", "Estadistica Partidos", "Partidos",
                    "Categoria Partido", "Estadistica Ganados", "Ganados","Porcentaje Ganados", "Estadistica Empatados",
                    "Empatados","Porcentaje Empatados", "Estadistica Perdidos", "Perdidos","Porcentaje Perdidos"]

        return pd.DataFrame([fila_datos_unificados], columns=columnas)

    def obtenerEntrenadorEquipo(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            tabla_entrenador=self.__contenido_tabla_entrenador(contenido)

            return self.__obtenerDataLimpia(tabla_entrenador)

        except Exception:

            raise EquipoEntrenadorError(f"Error en obtener el entrenador del equipo: {self.equipo}")