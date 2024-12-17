import time

from utils import crearArchivoLog
from config import EQUIPO_ID, TEMPORADA_INICIO, MES_FIN_TEMPORADA

from python.src.etls import ETL_Equipos_Liga, ETL_Detalle_Equipo, ETL_Escudo_Equipo
from python.src.etls import ETL_Entrenador_Equipo, ETL_Estadio_Equipo, ETL_Partidos_Equipo
from python.src.etls import ETL_Partido_Estadio, ETL_Competicion, ETL_Campeones_Competicion
from python.src.etls import ETL_Partido_Competicion, ETL_Jugadores_Equipo, ETL_Jugador
from python.src.etls import ETL_Partido_Goleadores, ETL_Estadio, ETL_Proximos_Partidos_Equipo
from python.src.database.conexion import Conexion
from python.src.utils import generarTemporadas, obtenerCoordenadasEstadio

def Pipeline_Equipos_Ligas()->None:

	con=Conexion()

	ligas=con.obtenerLigas()

	for liga in ligas:

		try:
			
			ETL_Equipos_Liga(liga)

		except Exception as e:

			mensaje=f"Liga: {liga} - Motivo: {e}"
		
			print(f"Error en liga {liga}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline(funcion):

	def wrapper():

		con=Conexion()

		equipos=con.obtenerEquipos()

		for equipo in equipos:

			try:

				funcion(equipo)

			except Exception as e:

				mensaje=f"Equipo: {equipo} - Motivo: {e}"

				print(f"Error en equipo {equipo}")

				crearArchivoLog(mensaje)

			time.sleep(0.25)

		con.cerrarConexion()

	return wrapper

@Pipeline
def Pipeline_Detalle_Equipos(equipo):
	ETL_Detalle_Equipo(equipo)

@Pipeline
def Pipeline_Escudo_Equipos(equipo):
	ETL_Escudo_Equipo(equipo)

@Pipeline
def Pipeline_Entrenador_Equipos(equipo):
	ETL_Entrenador_Equipo(equipo)

@Pipeline
def Pipeline_Estadio_Equipos(equipo):
	ETL_Estadio_Equipo(equipo)

def ETL_Partidos_Temporadas_Equipo(temporada:int=TEMPORADA_INICIO, equipo:int=EQUIPO_ID)->None:

	temporadas=generarTemporadas(temporada, MES_FIN_TEMPORADA)

	for temporada in temporadas:

		try:
			
			ETL_Partidos_Equipo(equipo, temporada)

		except Exception as e:

			mensaje=f"Partidos Equipo: {equipo} Temporada: {temporada} - Motivo: {e}"
		
			print(f"Error en partido de equipo {equipo} en temporada {temporada}")

			crearArchivoLog(mensaje)

def Pipeline_Partidos_Equipo()->None:

	con=Conexion()

	if con.tabla_vacia("partidos"):

		print(f"Obtencion total de los partidos desde {TEMPORADA_INICIO}")

		con.cerrarConexion()

		ETL_Partidos_Temporadas_Equipo()

	else:

		ano_mas_reciente=con.ultimo_ano()

		print(f"Obtencion de los datos desde {ano_mas_reciente}")

		con.cerrarConexion()

		ETL_Partidos_Temporadas_Equipo(temporada=ano_mas_reciente)

def Pipeline_Partidos_Estadio()->None:

	con=Conexion()

	partidos=con.obtenerPartidosSinEstadio()

	for partido_id, equipo_local, equipo_visitante in partidos:

		try:
			
			ETL_Partido_Estadio(equipo_local, equipo_visitante, partido_id)

		except Exception as e:

			if con.existe_estadio_equipo(equipo_local):

				estadio_equipo_local=con.obtenerEstadioEquipo(equipo_local)

				con.insertarPartidoEstadio((partido_id, estadio_equipo_local))

				print(f"Estadio {estadio_equipo_local} del partido {partido_id} del equipo local {equipo_local} agregado correctamente")

			else:

				mensaje=f"Estadio Partido_Id: {partido_id} - Motivo: {e}"

				print(f"Error en estadio del partido {partido_id} - {equipo_local} vs {equipo_visitante}")

				crearArchivoLog(mensaje)

		time.sleep(0.25)

	con.cerrarConexion()

def Pipeline_Partidos_Competicion()->None:

	con=Conexion()

	partidos=con.obtenerPartidosSinCompeticion()

	for partido_id, equipo_local, equipo_visitante in partidos:

		try:
			
			ETL_Partido_Competicion(equipo_local, equipo_visitante, partido_id)

		except Exception as e:

			mensaje=f"Competicion Partido_Id: {partido_id} - Motivo: {e}"

			print(f"Error en competicion del partido {partido_id} - {equipo_local} vs {equipo_visitante}")

			crearArchivoLog(mensaje)

		time.sleep(0.25)

	con.cerrarConexion()

def Pipeline_Partidos_Goleadores()->None:

	con=Conexion()

	partidos=con.obtenerPartidosSinGoleadores()

	for partido_id, equipo_local, equipo_visitante in partidos:

		try:
			
			ETL_Partido_Goleadores(equipo_local, equipo_visitante, partido_id)

		except Exception as e:

			mensaje=f"Goleadores Partido_Id: {partido_id} - Motivo: {e}"

			print(f"Error en los goleadores del partido {partido_id} - {equipo_local} vs {equipo_visitante}")

			crearArchivoLog(mensaje)

		time.sleep(0.25)

	con.cerrarConexion()

def Pipeline_Competiciones_Equipos()->None:

	con=Conexion()

	competiciones=con.obtenerCompeticionesEquipos()

	for competicion in competiciones:

		try:

			if not con.existe_competicion(competicion):

				con.insertarCompeticion(competicion)

				print(f"Competicion {competicion} insertada")

		except Exception as e:

			mensaje=f"Competicion Equipo: {competicion} - Motivo: {e}"
		
			print(f"Error en competicion equipo {competicion}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline_Competiciones()->None:

	con=Conexion()

	competiciones=con.obtenerCompeticiones()

	for competicion in competiciones:

		try:
			
			ETL_Competicion(competicion)

		except Exception as e:

			mensaje=f"Competicion: {competicion} - Motivo: {e}"
		
			print(f"Error en competicion {competicion}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline_Campeones_Competiciones()->None:

	con=Conexion()

	competiciones=con.obtenerCompeticiones()

	for competicion in competiciones:

		try:
			
			ETL_Campeones_Competicion(competicion)

		except Exception as e:

			mensaje=f"Campeones Competicion: {competicion} - Motivo: {e}"
		
			print(f"Error en los campeones de la competicion {competicion}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def ETL_Jugadores_Temporadas_Equipo(temporada:int=TEMPORADA_INICIO, equipo:int=EQUIPO_ID)->None:

	con=Conexion()

	temporadas=generarTemporadas(temporada, MES_FIN_TEMPORADA)

	for temporada_jugadores in temporadas:

		try:

			ETL_Jugadores_Equipo(equipo, temporada_jugadores)

			con.actualizarTemporadaJugadores(temporada_jugadores)

		except Exception as e:

			mensaje=f"Jugadores Equipo: {equipo} Temporada: {temporada_jugadores} - Motivo: {e}"

			print(f"Error en jugadores de equipo {equipo} en temporada {temporada_jugadores}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline_Jugadores_Equipo()->None:

	con=Conexion()

	if con.tabla_vacia("temporada_jugadores"):

		print(f"Obtencion total de los jugadores desde {TEMPORADA_INICIO}")

		con.insertarTemporadaJugadores(TEMPORADA_INICIO)

		con.cerrarConexion()

		ETL_Jugadores_Temporadas_Equipo()

	else:

		ano_mas_reciente=con.ultimo_ano_jugadores()

		print(f"Obtencion de los datos desde {ano_mas_reciente}")

		con.cerrarConexion()

		ETL_Jugadores_Temporadas_Equipo(temporada=ano_mas_reciente)

def Pipeline_Jugadores()->None:

	con=Conexion()

	jugadores=con.obtenerJugadores()

	for jugador in jugadores:

		try:

			ETL_Jugador(jugador)

		except Exception as e:

			mensaje=f"Jugador: {jugador} - Motivo: {e}"

			print(f"Error en jugador {jugador}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline_Estadios_Pais()->None:

	con=Conexion()

	estadios=con.obtenerEstadios()

	for estadio in estadios:

		try:

			ETL_Estadio(estadio)

		except Exception as e:

			mensaje=f"Pais Estadio: {estadio} - Motivo: {e}"

			print(f"Error en pais del estadio {estadio}")

			crearArchivoLog(mensaje)

def Pipeline_Estadios_Coordenadas()->None:

	con=Conexion()

	estadios=con.obtenerEstadiosSinCoordenadas()

	for estadio, nombre, direccion in estadios:

		print(f"Estadio {estadio}")

		try:

			latitud, longitud=obtenerCoordenadasEstadio(nombre)

			if latitud and longitud:

				con.actualizarCoordenadasEstadio([latitud, longitud], estadio)

			else:

				latitud_2, longitud_2=obtenerCoordenadasEstadio(direccion)

				if latitud_2 and longitud_2:

					con.actualizarCoordenadasEstadio([latitud_2, longitud_2], estadio)

				else:

					print(f"No se han podido obtener las coordenadas del estadio {estadio}")

		except Exception as e:

			mensaje=f"Coordenadas Estadio: {estadio} - Motivo: {e}"

			print(f"Error en coordenadas del estadio {estadio}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline_Proximos_Partidos_Equipo()->None:

	con=Conexion()

	# Permite actualizar los proximos partidos (elimina los que ya se han jugado y actualiza si hay horas definidas)
	con.vaciar_proximos_partidos()

	ano_mas_reciente=con.ultimo_ano()

	temporadas=generarTemporadas(ano_mas_reciente, MES_FIN_TEMPORADA)

	temporada=temporadas[-1]

	print(f"Obtencion de los proximos partidos de {temporada}")

	try:
		
		ETL_Proximos_Partidos_Equipo(EQUIPO_ID, temporada)

	except Exception as e:

		mensaje=f"Proximos Partidos Equipo: {equipo} Temporada: {temporada} - Motivo: {e}"
	
		print(f"Error en proximo partido de equipo {equipo} en temporada {temporada}")

		crearArchivoLog(mensaje)

	con.cerrarConexion()