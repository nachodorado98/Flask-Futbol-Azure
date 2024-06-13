import os

from utils import vaciarCarpeta, crearArchivoLog
from config import URL_ESCUDO, URL_ENTRENADOR, URL_PRESIDENTE, URL_ESTADIO, ESCUDOS, ENTRENADORES, PRESIDENTES, ESTADIOS

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

	crearEntornoDataLake("contenedorequipos", [ESCUDOS, ENTRENADORES, PRESIDENTES, ESTADIOS])

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

def subirPresidentesDataLake()->None:

	con=Conexion()

	codigo_presidentes=con.obtenerCodigoPresidentes()

	con.cerrarConexion()

	ruta_presidentes=os.path.join(os.getcwd(), "dags", "entorno", "imagenes", PRESIDENTES)

	for codigo in codigo_presidentes:

		print(f"Descargando presidente {codigo}...")

		try:

			descargarImagen(URL_PRESIDENTE, codigo, ruta_presidentes)

		except Exception as e:

			mensaje=f"Presidente: {codigo} - Motivo: {e}"

			print(f"Error en presidente con codigo {codigo}")

			crearArchivoLog(mensaje)

	print("Descarga de presidentes finalizada")

	try:

		subirArchivosDataLake("contenedorequipos", PRESIDENTES, ruta_presidentes)

	except Exception as e:

			mensaje=f"Motivo: {e}"

			print(f"Error al subir los presidentes al data lake")

			crearArchivoLog(mensaje)

	vaciarCarpeta(ruta_presidentes)

def subirEstadiosDataLake()->None:

	con=Conexion()

	codigo_estadios=con.obtenerCodigoEstadios()

	con.cerrarConexion()

	ruta_estadios=os.path.join(os.getcwd(), "dags", "entorno", "imagenes", ESTADIOS)

	for codigo in codigo_estadios:

		print(f"Descargando estadios {codigo}...")

		try:

			descargarImagen(URL_ESTADIO, codigo, ruta_estadios)

		except Exception as e:

			mensaje=f"Estadio: {codigo} - Motivo: {e}"

			print(f"Error en estadio con codigo {codigo}")

			crearArchivoLog(mensaje)

	print("Descarga de estadios finalizada")

	try:

		subirArchivosDataLake("contenedorequipos", ESTADIOS, ruta_estadios)

	except Exception as e:

			mensaje=f"Motivo: {e}"

			print(f"Error al subir los estadios al data lake")

			crearArchivoLog(mensaje)

	vaciarCarpeta(ruta_estadios)