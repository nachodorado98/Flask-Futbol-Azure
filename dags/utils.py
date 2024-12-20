from datetime import datetime
import os
from python.src.database.conexion import Conexion
from python.src.utils import obtenerBoolCadena

def existe_entorno()->str:

	return "entorno.entorno_creado" if os.path.exists(os.path.join(os.getcwd(), "dags", "entorno")) else "entorno.carpeta_logs"

def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			os.remove(os.path.join(ruta, archivo))

def crearArchivoLog(motivo:str)->None:

	archivo_log=f"log_{datetime.now().strftime('%Y%m%d_%H%M%S.%f')}.txt"

	ruta_log=os.path.join(os.getcwd(), "dags", "entorno", "logs", archivo_log)

	with open(ruta_log, "w") as archivo:

		archivo.write(f"Error!!! {motivo}")

def actualizarVariable(variable:str, valor:str)->None:

	con=Conexion()

	con.actualizarValorVariable(variable, valor)

	con.cerrarConexion()

def obtenerValorVariable(variable:str)->str:

	con=Conexion()

	valor=con.obtenerValorVariable(variable)

	con.cerrarConexion()

	return valor

def ejecutarDagPartidos()->None:

	valor=obtenerValorVariable("DAG_EQUIPOS_EJECUTADO")

	if not obtenerBoolCadena(valor):

		raise Exception("Debes iniciar al menos una vez el DAG de los equipos")

def ejecutarDagCompeticiones()->None:

	valor=obtenerValorVariable("DAG_PARTIDOS_EJECUTADO")

	if not obtenerBoolCadena(valor):

		raise Exception("Debes iniciar al menos una vez el DAG de los partidos")

def ejecutarDagJugadores()->None:

	valor=obtenerValorVariable("DAG_COMPETICIONES_EJECUTADO")

	if not obtenerBoolCadena(valor):

		raise Exception("Debes iniciar al menos una vez el DAG de las competiciones")

def ejecutarDagEstadios()->None:

	valor=obtenerValorVariable("DAG_JUGADORES_EJECUTADO")

	if not obtenerBoolCadena(valor):

		raise Exception("Debes iniciar al menos una vez el DAG de los jugadores")

def ejecutarDagEntrenadores()->None:

	valor=obtenerValorVariable("DAG_ESTADIOS_EJECUTADO")

	if not obtenerBoolCadena(valor):

		raise Exception("Debes iniciar al menos una vez el DAG de los estadios")

def ejecutarDagBackUp()->None:

	valores_dags=[obtenerValorVariable("DAG_EQUIPOS_EJECUTADO"),
					obtenerValorVariable("DAG_PARTIDOS_EJECUTADO"),
					obtenerValorVariable("DAG_COMPETICIONES_EJECUTADO"),
					obtenerValorVariable("DAG_JUGADORES_EJECUTADO"),
					obtenerValorVariable("DAG_ESTADIOS_EJECUTADO"),
					obtenerValorVariable("DAG_ENTRENADORES_EJECUTADO")]

	if not all(map(obtenerBoolCadena, valores_dags)):

		raise Exception("Debes iniciar al menos una vez el DAG de los equipos, partidos, competiciones, jugadores, estadios y entrenadores")