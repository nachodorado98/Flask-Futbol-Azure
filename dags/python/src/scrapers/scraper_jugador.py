import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import List, Optional
import itertools

from .scraper import Scraper

from .excepciones_scrapers import PaginaError, JugadorError

from .configscrapers import URL, ENDPOINT_JUGADOR

class ScraperJugador(Scraper):

    def __init__(self, jugador:str)->None:

        self.jugador=jugador

        super().__init__(f"{ENDPOINT_JUGADOR}/{self.jugador}")

    def __contenido_cabecera(self, contenido:bs4)->bs4:

        return contenido.find("div", class_="head-info fixed-w-scroll")

    def __informacion_nombre(self, cabecera:bs4)->str:

        try:

            titulo_nombre=cabecera.find("div", class_="head-content").find("div", class_="head-title").find("p", class_="title")

            return titulo_nombre.text.strip()

        except Exception:

            return ""

    def __informacion_general(self, cabecera:bs4)->List:

        fila_cabecera=cabecera.find("div", class_="bottom-row")

        def obtenerEquipo(fila_cabecera:bs4)->str:

            try:

                url=fila_cabecera.find("div", class_="team-info")

                return url.find("a", href=True)["href"]

            except Exception:

                return ""

        def obtenerPaisCara(fila_cabecera:bs4)->List:

            contenedor_imagenes=fila_cabecera.find("div", class_="img-container").find("div", class_="ib")

            try:

                imagen_pais=contenedor_imagenes.find("img", src=True)["src"].split("?")[0].strip()

                imagen_cara=contenedor_imagenes.find("div", class_="img-wrapper").find("img", src=True)["src"].split("?")[0].strip()

                return imagen_pais, imagen_cara

            except Exception:

                return ["", ""]

        def obtenerPuntuacion(fila_cabecera:bs4)->str:

            try:

                puntuacion=fila_cabecera.find("div", class_="data-boxes ta-c").find("div", class_="elo-box")

                return puntuacion.text.strip()

            except Exception:

                return "0"

        def obtenerDataEspecifica(fila_cabecera:bs4)->List:

            try:

                contenedores_datos=fila_cabecera.find("div", class_="data-boxes ta-c").find_all("div", class_="data-box")

                def obtenerDatos(contenedor_datos:bs4)->List:

                    try:

                        numero=contenedor_datos.find("p", class_="number").text

                        etiqueta=contenedor_datos.find("div").text

                        return [numero, etiqueta]

                    except:

                        return ["", ""]

                data_especifica=list(map(obtenerDatos, contenedores_datos))

                return list(itertools.chain(*data_especifica))
            
            except Exception:

                return [""]*4

        try:

            equipo=obtenerEquipo(fila_cabecera)

            pais, cara=obtenerPaisCara(fila_cabecera)

            puntuacion=obtenerPuntuacion(fila_cabecera)

            valor, dorsal, edad, posicion=obtenerDataEspecifica(fila_cabecera)

            return [equipo, pais, cara, puntuacion, valor, dorsal, edad, posicion]

        except Exception:

            return [""]*8

    def __obtenerDataLimpia(self, cabecera:bs4)->pd.DataFrame:

        nombre=self.__informacion_nombre(cabecera)

        datos_generales=self.__informacion_general(cabecera)

        fila_datos_unificados=[nombre]+datos_generales

        columnas=["Nombre", "Equipo_URL", "Pais_URL", "Cara_URL", "Puntuacion", "Valor", "Dorsal", "Edad", "Posicion"]

        return pd.DataFrame([fila_datos_unificados], columns=columnas)

    def obtenerJugador(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            cabecera=self.__contenido_cabecera(contenido)

            return self.__obtenerDataLimpia(cabecera)

        except Exception:

            raise JugadorError(f"Error en obtener los datos del jugador: {self.jugador}")