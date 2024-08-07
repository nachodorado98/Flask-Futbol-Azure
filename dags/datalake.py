import os

from utils import vaciarCarpeta, crearArchivoLog
from config import URL_ESCUDO, URL_ESCUDO_ALTERNATIVA, URL_ENTRENADOR, URL_PRESIDENTE, URL_ESTADIO
from config import ESCUDOS, ENTRENADORES, PRESIDENTES, ESTADIOS, CONTENEDOR, COMPETICIONES
from config import TABLA_EQUIPOS, TABLA_ESTADIOS, TABLA_EQUIPO_ESTADIO, TABLA_PARTIDOS, TABLA_PARTIDO_ESTADIO
from config import TABLA_COMPETICIONES

from python.src.database.conexion import Conexion
from python.src.datalake.conexion_data_lake import ConexionDataLake
from python.src.utils import entorno_creado, crearEntornoDataLake, descargarImagen, subirArchivosDataLake
from python.src.utils import subirTablaDataLake

def data_lake_disponible()->str:

	try:

		con=ConexionDataLake()

		con.cerrarConexion()

		return "datalake.entorno_data_lake_creado"

	except Exception:

		return "log_data_lake"

def entorno_data_lake_creado():

	if not entorno_creado(CONTENEDOR):

		return "datalake.crear_entorno_data_lake"

	return "datalake.no_crear_entorno_data_lake"

def creacion_entorno_data_lake()->None:

	carpetas=[ESCUDOS, ENTRENADORES, PRESIDENTES, ESTADIOS, COMPETICIONES, TABLA_EQUIPOS, TABLA_ESTADIOS,
				TABLA_EQUIPO_ESTADIO, TABLA_PARTIDOS, TABLA_PARTIDO_ESTADIO, TABLA_COMPETICIONES]

	crearEntornoDataLake(CONTENEDOR, carpetas)

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

		except Exception as e1:

			print(f"Error en escudo con codigo {codigo} en la primera URL: {URL_ESCUDO}")

			try:

				descargarImagen(URL_ESCUDO_ALTERNATIVA, codigo, ruta_escudos)

			except Exception as e2:

				mensaje=f"Escudo: {codigo} - Motivo: {e2}"

				print(f"Error en escudo con codigo {codigo} en la segunda URL: {URL_ESCUDO_ALTERNATIVA}")

				crearArchivoLog(mensaje)

	print("Descarga de escudos finalizada")

	try:

		subirArchivosDataLake(CONTENEDOR, ESCUDOS, ruta_escudos)

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

		subirArchivosDataLake(CONTENEDOR, ENTRENADORES, ruta_entrenadores)

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

		subirArchivosDataLake(CONTENEDOR, PRESIDENTES, ruta_presidentes)

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

		subirArchivosDataLake(CONTENEDOR, ESTADIOS, ruta_estadios)

	except Exception as e:

			mensaje=f"Motivo: {e}"

			print(f"Error al subir los estadios al data lake")

			crearArchivoLog(mensaje)

	vaciarCarpeta(ruta_estadios)

def subirBackUpTablasDataLake()->None:

	tabla_carpetas=[("equipos", TABLA_EQUIPOS), ("estadios", TABLA_ESTADIOS), ("equipo_estadio", TABLA_EQUIPO_ESTADIO),
					("partidos", TABLA_PARTIDOS), ("partido_estadio", TABLA_PARTIDO_ESTADIO), ("competiciones", TABLA_COMPETICIONES)]

	for tabla, carpeta in tabla_carpetas:

		print(f"Back Up de la tabla {tabla}")

		try:

			subirTablaDataLake(tabla, CONTENEDOR, carpeta)

		except Exception as e:

			mensaje=f"Tabla: {tabla} - Motivo: {e}"

			print(f"Error al subir la tabla {tabla} al data lake")

			crearArchivoLog(mensaje)

	print("Back Up de las tablas en el data lake finalizada")