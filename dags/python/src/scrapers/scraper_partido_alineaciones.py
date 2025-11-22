from bs4 import BeautifulSoup as bs4
import pandas as pd
from typing import Optional, List

from .scraper import Scraper

from .excepciones_scrapers import PartidoAlineacionesAlineacionError, PartidoAlineacionesSuplentesError, PartidoAlineacionesError

from .configscrapers import ENDPOINT_PARTIDO

class ScraperPartidoAlineaciones(Scraper):

    def __init__(self, equipo_local:str, equipo_visitante:str, partido_id:str)->None:

        self.equipo_local=equipo_local
        self.equipo_visitante=equipo_visitante
        self.partido_id=partido_id

        super().__init__(f"{ENDPOINT_PARTIDO}/{self.equipo_local}/{self.equipo_visitante}/{self.partido_id}/alineaciones")

    def __contenido_tabla_alineacion(self, contenido:bs4)->Optional[bs4]:

        try:

            return contenido.find("div", id="mod_lineup").find("div", class_="panel panel-lineup").find("div", class_="panel-body")

        except Exception:

            raise PartidoAlineacionesAlineacionError(f"Error en obtener la alineacion del partido: {self.equipo_local}/{self.equipo_visitante}/{self.partido_id}. No existe")

    def __contenido_tabla_suplentes(self, contenido:bs4)->Optional[bs4]:

        try:

            tabla=contenido.find("div", id="mod_lineupBench").find("div", class_="panel panel-bench").find("div", class_="panel-body pn").find("div", class_="row")

            if "Convocados sin confirmar" in str(tabla):

                raise PartidoAlineacionesSuplentesError(f"Error en obtener los suplentes del partido: {self.equipo_local}/{self.equipo_visitante}/{self.partido_id}. No existe")

            else:

                return tabla

        except Exception:

            raise PartidoAlineacionesSuplentesError(f"Error en obtener los suplentes del partido: {self.equipo_local}/{self.equipo_visitante}/{self.partido_id}. No existe")

    def __obtener_entrenadores(self, tabla_alineacion:bs4)->tuple:

        tabla_entrenador_local=tabla_alineacion.find("div", class_="row jc-sb align-center coach-wrapper")

        tabla_entrenador_visitante=tabla_alineacion.find("div", class_="row jc-sb align-center coach-wrapper second")

        try:

            entrenador_local=tabla_entrenador_local.find("div", class_="coach").find("a", href=True)["href"]

        except Exception:

            entrenador_local=None

        try:

            entrenador_visitante=tabla_entrenador_visitante.find("div", class_="coach").find("a", href=True)["href"]

        except Exception:

            entrenador_visitante=None

        return entrenador_local, entrenador_visitante

    def __obtener_alineaciones(self, tabla_alineacion:bs4)->tuple:

        campo=tabla_alineacion.find("div", class_="field mv10")

        try:

            jugadores_local=campo.find("ul", class_="lineup local").find_all("li")

        except Exception:

            jugadores_local=[]

        try:

            jugadores_visitante=campo.find("ul", class_="lineup visitor").find_all("li")

        except Exception:

            jugadores_visitante=[]

        def obtenerDatosJugador(jugador:bs4, tipo:str, posicion:int)->tuple:

            jugador_url=jugador.find("a", href=True)["href"]

            try:

                numero=jugador.find("div", class_="name num-lineups").text.strip()

            except Exception:

                numero=None

            try:

                puntos=jugador.find("div", class_="match-points").text.strip()

            except Exception:

                puntos=None

            return jugador_url, numero, puntos, "T", tipo, posicion

        datos_jugadores_local=[obtenerDatosJugador(jugador, "L", numero+1) for numero, jugador in enumerate(jugadores_local)]

        datos_jugadores_visitante=[obtenerDatosJugador(jugador, "V", numero+1) for numero, jugador in enumerate(jugadores_visitante)]

        return datos_jugadores_local, datos_jugadores_visitante

    def __obtener_tacticas(self, tabla_alineacion:bs4)->tuple:

        campo=tabla_alineacion.find("div", class_="field mv10")

        tacticas=[tactica.text for tactica in campo.find_all("div", class_="tactic")]

        return tuple(tacticas)

    def __informacion_entrenador(self, tabla_alineacion:bs4)->List[str]:

        try:

            entrenadores=self.__obtener_entrenadores(tabla_alineacion)

            tacticas=self.__obtener_tacticas(tabla_alineacion)

            return list(zip(entrenadores, tacticas))

        except Exception:

            [(None, None)]*2

    def __obtener_suplentes(self, tabla_suplentes:bs4)->tuple:

        columnas=tabla_suplentes.find_all("div", class_="col-6")

        try:

            suplentes_local=columnas[0].find_all("a", href=True)

        except Exception:

            suplentes_local=[]

        try:

            suplentes_visitante=columnas[1].find_all("a", href=True)

        except Exception:

            suplentes_visitante=[]

        def obtenerDatosJugador(jugador:bs4, tipo:str)->tuple:

            jugador_url=jugador["href"]

            numero_posicion_puntos=jugador.find("div", class_="bench-player")

            try:

                numero=numero_posicion_puntos.find("span", class_="number bold mr3").text.strip()

            except Exception:

                numero=None

            try:

                puntos=numero_posicion_puntos.find("div", class_="match-points").text.strip()

            except Exception:

                puntos=None

            return jugador_url, numero, puntos, "S", tipo, -1

        datos_suplentes_local=list(map(lambda suplente: obtenerDatosJugador(suplente, "L"), suplentes_local))

        datos_suplentes_visitante=list(map(lambda suplente: obtenerDatosJugador(suplente, "V"), suplentes_visitante))

        return datos_suplentes_local, datos_suplentes_visitante

    def __obtenerDataLimpia(self, tabla_alineacion:bs4, tabla_suplentes:bs4)->pd.DataFrame:

        info_entrenador_local, info_entrenador_visitante=self.__informacion_entrenador(tabla_alineacion)

        titulares_local, titulares_visitante=self.__obtener_alineaciones(tabla_alineacion)

        if tabla_suplentes:

            suplentes_local, suplentes_visitante=self.__obtener_suplentes(tabla_suplentes)

        else:

            suplentes_local=[]

            suplentes_visitante=[]

        datos_local=[datos+info_entrenador_local for datos in titulares_local+suplentes_local]

        datos_visitante=[datos+info_entrenador_visitante for datos in titulares_visitante+suplentes_visitante]

        fila_datos_unificados=datos_local+datos_visitante

        columnas=["Jugador_URL", "Numero", "Puntos", "Alineacion", "Tipo", "Posicion", "Entrenador_URL", "Tactica"]

        return pd.DataFrame(fila_datos_unificados, columns=columnas)

    def obtenerPartidoAlineaciones(self)->Optional[pd.DataFrame]:

        try:

            contenido=self._Scraper__realizarPeticion()

            tabla_alineacion=self.__contenido_tabla_alineacion(contenido)

            try:

                tabla_suplentes=self.__contenido_tabla_suplentes(contenido)

            except PartidoAlineacionesSuplentesError:

                tabla_suplentes=None

            return self.__obtenerDataLimpia(tabla_alineacion, tabla_suplentes)

        except Exception:

            raise PartidoAlineacionesError(f"Error en obtener las alineaciones del partido: {self.equipo_local}/{self.equipo_visitante}/{self.partido_id}")