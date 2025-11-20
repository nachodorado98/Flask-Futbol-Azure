import time

from utils import crearArchivoLog
from config import ENTORNO, MAX_ERRORES
from config import EQUIPO_ID, TEMPORADA_INICIO, MES_FIN_TEMPORADA, EQUIPO_ID_REAL

from python.src.etls import ETL_Equipos_Liga, ETL_Detalle_Equipo, ETL_Escudo_Equipo
from python.src.etls import ETL_Entrenador_Equipo, ETL_Estadio_Equipo, ETL_Partidos_Equipo
from python.src.etls import ETL_Partido_Estadio, ETL_Competicion, ETL_Campeones_Competicion
from python.src.etls import ETL_Partido_Competicion, ETL_Jugadores_Equipo, ETL_Jugador
from python.src.etls import ETL_Partido_Goleadores, ETL_Estadio, ETL_Proximos_Partidos_Equipo
from python.src.etls import ETL_Entrenador, ETL_Jugador_Equipos, ETL_Jugador_Seleccion
from python.src.etls import ETL_Palmares_Equipo, ETL_Entrenador_Equipos, ETL_Palmares_Entrenador

from python.src.database.conexion import Conexion

from python.src.utils import generarTemporadas, obtenerCoordenadasEstadio, obtenerCiudadMasAcertada


def Pipeline_Base(obtener_funcion_procesar, entidad, categoria):

	def decorador(funcion):

		def wrapper():

			con=Conexion(ENTORNO)

			valores=obtener_funcion_procesar(con)

			for valor in valores:

				numero_errores=con.obtenerNumeroErrores(entidad, categoria, valor)

				if numero_errores<MAX_ERRORES:

					print("-"*70)

					try:

						funcion(valor)

					except Exception as e:

						mensaje=f"{entidad}: {valor} - Motivo: {e}"

						crearArchivoLog(mensaje)

						if not con.existe_error(entidad, categoria, valor):

							con.insertarError(entidad, categoria, valor)

							print(f"Error NUEVO en la tabla de errores - {entidad} {categoria}")

						else:

							con.actualizarNumeroErrores(entidad, categoria, valor)

							print(f"Error ACTUALIZADO en la tabla de errores - {entidad} {categoria}")

					time.sleep(0.25)

			con.cerrarConexion()

		return wrapper

	return decorador

@Pipeline_Base(lambda con: con.obtenerLigas(), "Liga", "Equipos")
def Pipeline_Equipos_Ligas(equipo):
    ETL_Equipos_Liga(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquipos(), "Equipo", "Detalle")
def Pipeline_Detalle_Equipos(equipo):
    ETL_Detalle_Equipo(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquipos(), "Equipo", "Escudo")
def Pipeline_Escudo_Equipos(equipo):
    ETL_Escudo_Equipo(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquipos(), "Equipo", "Entrenador")
def Pipeline_Entrenador_Equipos(equipo):
    ETL_Entrenador_Equipo(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquipos(), "Equipo", "Estadio")
def Pipeline_Estadio_Equipos(equipo):
    ETL_Estadio_Equipo(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquipos(), "Equipo", "Palmares")
def Pipeline_Palmares_Equipos(equipo):
    ETL_Palmares_Equipo(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquiposNombreVacio(), "Equipo", "Detalle")
def Pipeline_Detalle_Equipos_Faltantes(equipo):
    ETL_Detalle_Equipo(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquiposEscudoVacio(), "Equipo", "Escudo")
def Pipeline_Escudo_Equipos_Faltantes(equipo):
    ETL_Escudo_Equipo(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquiposEntrenadorVacio(), "Equipo", "Entrenador")
def Pipeline_Entrenador_Equipos_Faltantes(equipo):
    ETL_Entrenador_Equipo(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquiposEstadioVacio(), "Equipo", "Estadio")
def Pipeline_Estadio_Equipos_Faltantes(equipo):
    ETL_Estadio_Equipo(equipo, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEquiposPalmaresVacio(), "Equipo", "Palmares")
def Pipeline_Palmares_Equipos_Faltantes(equipo):
    ETL_Palmares_Equipo(equipo, ENTORNO)

def ETL_Partidos_Temporadas_Equipo(temporada:int=TEMPORADA_INICIO, equipo:int=EQUIPO_ID)->None:

	temporadas=generarTemporadas(temporada, MES_FIN_TEMPORADA)

	for temporada in temporadas:

		try:
			
			ETL_Partidos_Equipo(equipo, temporada, ENTORNO)

		except Exception as e:

			mensaje=f"Partidos Equipo: {equipo} Temporada: {temporada} - Motivo: {e}"
		
			print(f"Error en partido de equipo {equipo} en temporada {temporada}")

			crearArchivoLog(mensaje)

def Pipeline_Partidos_Equipo()->None:

	con=Conexion(ENTORNO)

	if con.tabla_vacia("partidos"):

		print(f"Obtencion total de los partidos desde {TEMPORADA_INICIO}")

		con.cerrarConexion()

		ETL_Partidos_Temporadas_Equipo()

	else:

		ano_mas_reciente=con.ultimo_ano(EQUIPO_ID_REAL)

		print(f"Obtencion de los datos desde {ano_mas_reciente}")

		con.cerrarConexion()

		ETL_Partidos_Temporadas_Equipo(temporada=ano_mas_reciente)

def Pipeline_Partidos_Equipo_Total(equipo:int, temporada:int=TEMPORADA_INICIO)->None:

	print(f"Obtencion total de los partidos desde {temporada}")

	ETL_Partidos_Temporadas_Equipo(temporada, equipo)

def Pipeline_Partidos_Estadio()->None:

	con=Conexion(ENTORNO)

	partidos=con.obtenerPartidosSinEstadio()

	for partido_id, equipo_local, equipo_visitante in partidos:

		entidad="Partido"

		categoria="Estadio"

		numero_errores=con.obtenerNumeroErrores(entidad, categoria, partido_id)

		if numero_errores<MAX_ERRORES:

			print("-"*70)

			try:
				
				ETL_Partido_Estadio(equipo_local, equipo_visitante, partido_id, ENTORNO)

			except Exception as e:

				if con.existe_estadio_equipo(equipo_local):

					estadio_equipo_local=con.obtenerEstadioEquipo(equipo_local)

					con.insertarPartidoEstadio((partido_id, estadio_equipo_local))

					print(f"Estadio {estadio_equipo_local} del partido {partido_id} del equipo local {equipo_local} agregado correctamente")

				else:

					mensaje=f"Estadio Partido_Id: {partido_id} - Motivo: {e}"

					crearArchivoLog(mensaje)

					if not con.existe_error(entidad, categoria, partido_id):

						con.insertarError(entidad, categoria, partido_id)

						print(f"Error NUEVO en la tabla de errores - {entidad} {categoria}")

					else:

						con.actualizarNumeroErrores(entidad, categoria, partido_id)

						print(f"Error ACTUALIZADO en la tabla de errores - {entidad} {categoria}")

			time.sleep(0.25)

	con.cerrarConexion()

def Pipeline_Partidos_Competicion()->None:

	con=Conexion(ENTORNO)

	partidos=con.obtenerPartidosSinCompeticion()

	for partido_id, equipo_local, equipo_visitante in partidos:

		entidad="Partido"

		categoria="Competicion"

		numero_errores=con.obtenerNumeroErrores(entidad, categoria, partido_id)

		if numero_errores<MAX_ERRORES:

			print("-"*70)

			try:
				
				ETL_Partido_Competicion(equipo_local, equipo_visitante, partido_id, ENTORNO)

			except Exception as e:

				mensaje=f"Competicion Partido_Id: {partido_id} - Motivo: {e}"

				crearArchivoLog(mensaje)

				if not con.existe_error(entidad, categoria, partido_id):

					con.insertarError(entidad, categoria, partido_id)

					print(f"Error NUEVO en la tabla de errores - {entidad} {categoria}")

				else:

					con.actualizarNumeroErrores(entidad, categoria, partido_id)

					print(f"Error ACTUALIZADO en la tabla de errores - {entidad} {categoria}")

			time.sleep(0.25)

	con.cerrarConexion()

def Pipeline_Partidos_Goleadores()->None:

	con=Conexion(ENTORNO)

	partidos=con.obtenerPartidosSinGoleadores()

	for partido_id, equipo_local, equipo_visitante in partidos:

		entidad="Partido"

		categoria="Goleadores"

		numero_errores=con.obtenerNumeroErrores(entidad, categoria, partido_id)

		if numero_errores<MAX_ERRORES:

			print("-"*70)

			try:
				
				ETL_Partido_Goleadores(equipo_local, equipo_visitante, partido_id, ENTORNO)

			except Exception as e:

				mensaje=f"Goleadores Partido_Id: {partido_id} - Motivo: {e}"

				crearArchivoLog(mensaje)

				if not con.existe_error(entidad, categoria, partido_id):

					con.insertarError(entidad, categoria, partido_id)

					print(f"Error NUEVO en la tabla de errores - {entidad} {categoria}")

				else:

					con.actualizarNumeroErrores(entidad, categoria, partido_id)

					print(f"Error ACTUALIZADO en la tabla de errores - {entidad} {categoria}")

			time.sleep(0.25)

	con.cerrarConexion()

def Pipeline_Competiciones_Equipos()->None:

	con=Conexion(ENTORNO)

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

@Pipeline_Base(lambda con: con.obtenerCompeticiones(), "Competicion", "Detalle")
def Pipeline_Competiciones(competicion):
	ETL_Competicion(competicion, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerCompeticiones(), "Competicion", "Campeones")
def Pipeline_Campeones_Competiciones(competicion):
	ETL_Campeones_Competicion(competicion, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerCompeticionesNombreVacio(), "Competicion", "Detalle")
def Pipeline_Competiciones_Faltantes(competicion):
    ETL_Competicion(competicion, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerCompeticionesCampeonesVacio(), "Competicion", "Campeones")
def Pipeline_Campeones_Competiciones_Faltantes(competicion):
    ETL_Campeones_Competicion(competicion, ENTORNO)

def ETL_Jugadores_Temporadas_Equipo(temporada:int=TEMPORADA_INICIO, equipo:int=EQUIPO_ID)->None:

	con=Conexion(ENTORNO)

	temporadas=generarTemporadas(temporada, MES_FIN_TEMPORADA)

	for temporada_jugadores in temporadas:

		try:

			ETL_Jugadores_Equipo(equipo, temporada_jugadores, ENTORNO)

			con.actualizarTemporadaJugadores(temporada_jugadores)

		except Exception as e:

			mensaje=f"Jugadores Equipo: {equipo} Temporada: {temporada_jugadores} - Motivo: {e}"

			print(f"Error en jugadores de equipo {equipo} en temporada {temporada_jugadores}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline_Jugadores_Equipo()->None:

	con=Conexion(ENTORNO)

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

def Pipeline_Jugadores_Equipo_Total(equipo:int, temporada:int=TEMPORADA_INICIO)->None:

	print(f"Obtencion total de los jugadores desde {temporada}")

	ETL_Jugadores_Temporadas_Equipo(temporada, equipo)

@Pipeline_Base(lambda con: con.obtenerJugadores(), "Jugador", "Detalle")
def Pipeline_Jugadores(jugador):
	ETL_Jugador(jugador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerJugadores(), "Jugador", "Equipos")
def Pipeline_Jugadores_Equipos(jugador):
	ETL_Jugador_Equipos(jugador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerJugadores(), "Jugador", "Seleccion")
def Pipeline_Jugadores_Seleccion(jugador):
	ETL_Jugador_Seleccion(jugador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerJugadoresNombreVacio(), "Jugador", "Detalle")
def Pipeline_Jugadores_Faltantes(jugador):
    ETL_Jugador(jugador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerJugadoresEquiposVacio(), "Jugador", "Equipos")
def Pipeline_Jugadores_Equipos_Faltantes(jugador):
    ETL_Jugador_Equipos(jugador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerJugadoresSeleccionVacio(), "Jugador", "Seleccion")
def Pipeline_Jugadores_Seleccion_Faltantes(jugador):
    ETL_Jugador_Seleccion(jugador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEstadios(), "Estadio", "Pais")
def Pipeline_Estadios_Pais(estadio):
    ETL_Estadio(estadio, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEstadiosPaisVacio(), "Estadio", "Pais")
def Pipeline_Estadios_Pais_Faltantes(estadio):
    ETL_Estadio(estadio, ENTORNO)

def Pipeline_Estadios_Coordenadas()->None:

	con=Conexion(ENTORNO)

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

def Pipeline_Estadios_Ciudades()->None:

	con=Conexion(ENTORNO)

	estadios=con.obtenerEstadiosSinCiudad()

	for estadio, latitud, longitud, direccion in estadios:

		print(f"Estadio {estadio}")

		try:

			ciudad=obtenerCiudadMasAcertada(latitud, longitud, direccion, ENTORNO)

			con.actualizarCiudadEstadio(ciudad, estadio)

		except Exception as e:

			mensaje=f"Ciudad Estadio: {estadio} - Motivo: {e}"

			print(f"Error en ciudad del estadio {estadio}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline_Proximos_Partidos_Equipo(equipo_id:int=EQUIPO_ID, equipo_id_real:str=EQUIPO_ID_REAL)->None:

	con=Conexion(ENTORNO)

	# Permite actualizar los proximos partidos (elimina los que ya se han jugado y actualiza si hay horas definidas)
	con.vaciar_proximos_partidos(equipo_id_real)

	ano_mas_reciente=con.ultimo_ano(equipo_id_real)

	temporadas=generarTemporadas(ano_mas_reciente, MES_FIN_TEMPORADA)

	temporada=temporadas[-1]

	print(f"Obtencion de los proximos partidos de {temporada}")

	try:
		
		ETL_Proximos_Partidos_Equipo(equipo_id, temporada, ENTORNO)

	except Exception as e:

		mensaje=f"Proximos Partidos Equipo: {equipo_id} Temporada: {temporada} - Motivo: {e}"
	
		print(f"Error en proximo partido de equipo {equipo_id} en temporada {temporada}")

		crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline_Entrenadores_Equipos()->None:

	con=Conexion(ENTORNO)

	entrenadores=con.obtenerEntrenadoresEquipos()

	for entrenador in entrenadores:

		try:

			if not con.existe_entrenador(entrenador):

				con.insertarEntrenador(entrenador)

				print(f"Entrenador {entrenador} insertado")

		except Exception as e:

			mensaje=f"Entrenador Equipo: {entrenador} - Motivo: {e}"
		
			print(f"Error en entrenador equipo {entrenador}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

@Pipeline_Base(lambda con: con.obtenerEntrenadores(), "Entrenador", "Detalle")
def Pipeline_Entrenadores(entrenador):
	ETL_Entrenador(entrenador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEntrenadores(), "Entrenador", "Equipos")
def Pipeline_Entrenadores_Equipo(entrenador):
	ETL_Entrenador_Equipos(entrenador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEntrenadores(), "Entrenador", "Palmares")
def Pipeline_Palmares_Entrenadores(entrenador):
	ETL_Palmares_Entrenador(entrenador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEntrenadoresNombreVacio(), "Entrenador", "Detalle")
def Pipeline_Entrenadores_Faltantes(entrenador):
    ETL_Entrenador(entrenador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEntrenadoresEquiposVacio(), "Entrenador", "Equipos")
def Pipeline_Entrenadores_Equipo_Faltantes(entrenador):
    ETL_Entrenador_Equipos(entrenador, ENTORNO)

@Pipeline_Base(lambda con: con.obtenerEntrenadoresPalmaresVacio(), "Entrenador", "Palmares")
def Pipeline_Palmares_Entrenadores_Faltantes(entrenador):
	ETL_Palmares_Entrenador(entrenador, ENTORNO)