from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List
import itertools

from .scraper import Scraper

from .excepciones_scrapers import EquipoError

from .configscrapers import ENDPOINT_EQUIPO

class ScraperEquipo(Scraper):

    def __init__(self, equipo:str)->None:

        self.equipo=equipo

        super().__init__(f"{ENDPOINT_EQUIPO}/{self.equipo}")

    def __contenido_tabla_info(self, contenido:bs4)->bs4:

        return contenido.find("div", id="mod_basicInfo").find("div", class_="panel team-stats")

    def __informacion_nombre(self, tabla_info:bs4)->tuple:

        info_nombre=tabla_info.find("div", class_="panel-stats")

        def obtenerNombre(info_nombre:bs4)->str:

            try:

                return info_nombre.find("h2").text.strip()

            except Exception:

                return ""

        def obtenerAliasSiglas(info_nombre:bs4)->tuple:

            try:

                cadena_alias_siglas=info_nombre.find("div", class_="subtitlte").text.strip()

                alias=cadena_alias_siglas.split("(")[0].strip()

                siglas=cadena_alias_siglas.split("(")[1].split(")")[0].strip()

                return alias, siglas

            except Exception:

                return "", ""

        nombre=obtenerNombre(info_nombre)

        alias, siglas=obtenerAliasSiglas(info_nombre)

        return nombre, alias, siglas 

    def __informacion_datos(self, tabla_info:bs4)->bs4:

        return tabla_info.find("div", class_="panel table-list")

    def __tabla_general(self, datos:bs4)->List[str]:

        tabla_general=datos.find("div", class_="table-body")

        filas=tabla_general.find_all("div", class_="table-row")

        def limpiarFilaPais(fila:bs4)->List[str]:

            try:

                cadena=fila.find("div").text

                contenido=fila.find("a").text.strip()

                imagen_contenido=fila.find("a").find("img", src=True)["src"].split("?")[0].strip()

                return [contenido, imagen_contenido]

            except Exception:

                return ["", ""]

        def limpiarFilaLiga(fila:bs4)->List[str]:

            try:

                cadena=fila.find("div").text

                contenido=fila.find("a").text.strip()

                url_contenido=fila.find("a", href=True)["href"]

                return [contenido, url_contenido]

            except Exception:

                return ["", ""]

        def limpiarTemporadas(fila:bs4)->List[str]:

            try:

                contenedores=fila.find_all("div")                

                cadena=contenedores[0].text

                contenido=contenedores[1].text.strip()

                return [contenido]

            except Exception:

                return [""]

        return limpiarFilaPais(filas[0])+limpiarFilaLiga(filas[1])+limpiarTemporadas(filas[2])

    def __informacion_general(self, tabla_info:bs4)->List[str]:

        try:

            datos=self.__informacion_datos(tabla_info)

            return self.__tabla_general(datos)

        except Exception:

            return [""]*5

    def __informacion_lista(self, tabla_info:bs4)->bs4:

        return tabla_info.find("div", class_="panel-body table-list")

    def __tabla_presidente(self, tabla_lista:bs4)->List[str]:

        presidente=tabla_lista.find("div", class_="table-head").text

        if presidente!="Presidente":

            return [""]*9

        tabla_presidente=tabla_lista.find("div", class_="table-body pl0").find("div", class_="table-row")

        def limpiarPresidenteNombre(tabla_presidente:bs4)->List[str]:

            tabla_presidente_nombre=tabla_presidente.find("div", class_="align-center ta-c flex-1 br-right")

            try:

                imagen_presidente=tabla_presidente_nombre.find("a").find("img", src=True)["src"].split("?")[0].strip()

            except Exception:

                imagen_presidente=""

            nombres_presidente=[nombre.text.strip() for nombre in tabla_presidente_nombre.find_all("p")]

            return nombres_presidente+[imagen_presidente]

        datos_nombre_presidente=limpiarPresidenteNombre(tabla_presidente)

        def limpiarPresidenteInformacion(tabla_presidente:bs4)->List[List[str]]:

            tabla_presidente_informacion=tabla_presidente.find("div", class_="row align-center flex-1 jc-sa")

            filas=tabla_presidente_informacion.find_all("div", class_="ta-c")

            filas_limpias=[[fila.find("div", class_="mt10 pb5").text, fila.find("div", class_="fs13").text] for fila in filas]

            if len(filas_limpias)==2:

                filas_limpias.insert(1, ("", ""))

            return list(itertools.chain(*filas_limpias))

        datos_informacion_presidente=limpiarPresidenteInformacion(tabla_presidente)            

        return datos_nombre_presidente+datos_informacion_presidente

    def __informacion_presidente(self, tabla_info:bs4)->List[str]:

        try:

            lista=self.__informacion_lista(tabla_info)

            return self.__tabla_presidente(lista)

        except Exception:

            return [""]*9

    def __tabla_datos_tecnicos(self, tabla_lista:bs4)->List[str]:

        tabla_datos_tecnicos=tabla_lista.find("div", class_="panel-body table-list").find("div", class_="table-body")

        filas=tabla_datos_tecnicos.find_all("div", class_="table-row")

        def obtenerContenidoFila(fila:bs4)->List[tuple]:

            celdas=fila.find_all("div")

            return celdas[0].text, celdas[1].text.strip()

        filas_limpias=[obtenerContenidoFila(fila) for fila in filas]

        def comprobarCampo(filas:str, campo:str)->bool:

            return False if not list(filter(lambda fila: fila[0]==campo, filas)) else True

        for campo in ["Ciudad", "Fecha fundación", "Estadio"]:

            condicion_campo=comprobarCampo(filas_limpias, campo)

            if not condicion_campo:

                filas_limpias.append((campo, ""))

        filas_ordenadas=sorted(filas_limpias)

        return list(map(lambda fila: fila[1], filas_ordenadas))

    def __informacion_datos_tecnicos(self, tabla_info:bs4)->List[str]:

        try:

            lista=self.__informacion_lista(tabla_info)

            return self.__tabla_datos_tecnicos(lista)

        except Exception:

            return [""]*3

    def __obtenerDataLimpia(self, tabla_info:bs4)->pd.DataFrame:

        nombre, alias, siglas=self.__informacion_nombre(tabla_info)

        general=self.__informacion_general(tabla_info)

        presidente=self.__informacion_presidente(tabla_info)

        datos_tecnicos=self.__informacion_datos_tecnicos(tabla_info)

        fila_datos_unificados=[nombre, alias, siglas]+general+presidente+datos_tecnicos

        columnas=["Nombre", "Alias", "Siglas", "Pais", "Pais_URL", "Categoria", "Categoria_URL", "Temporadas",
                    "Presidente", "Presidente_Nombre", "Presidente_URL", "Presidente_Pais", "Presidente_Ciudad",
                    "Presidente_Edad", "Presidente_Fecha", "Presidente_Cargo_Anos", "Presidente_Cargo_Meses",
                    "Ciudad", "Estadio", "Fundacion"]

        return pd.DataFrame([fila_datos_unificados], columns=columnas)

    def obtenerDetalleEquipo(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            tabla_info=self.__contenido_tabla_info(contenido)

            return self.__obtenerDataLimpia(tabla_info)

        except Exception:

            raise EquipoError(f"Error en obtener los datos del equipo: {self.equipo}")