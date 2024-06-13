import os

from utils import vaciarCarpeta, crearArchivoLog
from config import URL_ESCUDO, URL_ENTRENADOR, ESCUDOS, ENTRENADORES

from python.src.database.conexion import Conexion
from python.src.datalake.conexion_data_lake import ConexionDataLake
from python.src.utils import entorno_creado, crearEntornoDataLake, descargarImagen, subirArchivosDataLake

def data_lake_disponible()->str:

	try:

		con=ConexionDataLake()

		con.cerrarConexion()

		return "datalake.entorno_data_lake_creado"

	except Exception:

		return "log_data_lake"

def entorno_data_lake_creado():

	if not entorno_creado("contenedorequipos"):

		return "datalake.crear_entorno_data_lake"

	return "datalake.no_crear_entorno_data_lake"

def creacion_entorno_data_lake()->None:

	crearEntornoDataLake("contenedorequipos", [ESCUDOS, ENTRENADORES])

	print("Entorno Data Lake creado")

def subirEscudosDataLake()->None:

	con=Conexion()

	codigo_escudos=con.obtenerCodigoEscudos()

	con.cerrarConexion()

	ruta_escudos=os.path.join(os.getcwd(), "dags", "entorno", "imagenes", ESCUDOS)

	for codigo in codigo_escudos:

		print(f"Descargando escudo {codigo}...")

		try:

			descargarImagen(URL_ESCUDO, codigo, ruta_escudos)

		except Exception as e:

			mensaje=f"Escudo: {codigo} - Motivo: {e}"

			print(f"Error en escudo con codigo {codigo}")

			crearArchivoLog(mensaje)

	print("Descarga de escudos finalizada")

	try:

		subirArchivosDataLake("contenedorequipos", ESCUDOS, ruta_escudos)

	except Exception as e:

			mensaje=f"Motivo: {e}"

			print(f"Error al subir los escudos al data lake")

			crearArchivoLog(mensaje)

	vaciarCarpeta(ruta_escudos)

def subirEntrenadoresDataLake()->None:

	con=Conexion()

	codigo_entrenadores=con.obtenerCodigoEntrenadores()

	con.cerrarConexion()

	ruta_entrenadores=os.path.join(os.getcwd(), "dags", "entorno", "imagenes", ENTRENADORES)

	for codigo in codigo_entrenadores:

		print(f"Descargando entrenador {codigo}...")

		try:

			descargarImagen(URL_ENTRENADOR, codigo, ruta_entrenadores)

		except Exception as e:

			mensaje=f"Entrenador: {codigo} - Motivo: {e}"

			print(f"Error en entrenador con codigo {codigo}")

			crearArchivoLog(mensaje)

	print("Descarga de entrenadores finalizada")

	try:

		subirArchivosDataLake("contenedorequipos", ENTRENADORES, ruta_entrenadores)

	except Exception as e:

			mensaje=f"Motivo: {e}"

			print(f"Error al subir los entrenadores al data lake")

			crearArchivoLog(mensaje)

	vaciarCarpeta(ruta_entrenadores)