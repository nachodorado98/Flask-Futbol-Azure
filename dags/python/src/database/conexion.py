import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from datetime import datetime

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:

			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para confirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	#Metodo para insertar un equipo
	def insertarEquipo(self, equipo:str)->None:

		self.c.execute("""INSERT INTO equipos (Equipo_Id)
							VALUES(%s)""",
							(equipo,))

		self.confirmar()

	# Metodo para saber si existe el equipo
	def existe_equipo(self, equipo_id:str)->bool:

		self.c.execute("""SELECT *
							FROM equipos
							WHERE Equipo_Id=%s""",
							(equipo_id,))

		return False if self.c.fetchone() is None else True

	# Metodo para obtener las ligas
	def obtenerLigas(self)->List[tuple]:

		self.c.execute("""SELECT Nombre
						FROM ligas_scrapear""")

		ligas=self.c.fetchall()

		return list(map(lambda liga: liga["nombre"], ligas))

	# Metodo para actualizar los datos de un equipo
	def actualizarDatosEquipo(self, datos_equipo:List[str], equipo_id:str)->None:

		datos_equipo.append(equipo_id)

		self.c.execute("""UPDATE equipos
							SET Nombre_Completo=%s, Nombre=%s, Siglas=%s, Pais=%s, Codigo_Pais=%s, 
								Ciudad=%s, Competicion=%s, Codigo_Competicion=%s, Temporadas=%s,
								Estadio=%s, Fundacion=%s, Presidente=%s, Presidente_URL=%s,
								Codigo_Presidente=%s
							WHERE Equipo_Id=%s""",
							tuple(datos_equipo))

		self.confirmar()

	# Metodo para obtener los equipos
	def obtenerEquipos(self)->List[tuple]:

		self.c.execute("""SELECT Equipo_Id
						FROM equipos
						ORDER BY Equipo_Id""")

		equipos=self.c.fetchall()

		return list(map(lambda equipo: equipo["equipo_id"], equipos))

	# Metodo para actualizar el escudo de un equipo
	def actualizarEscudoEquipo(self, datos_escudo:List[int], equipo_id:str)->None:

		datos_escudo.append(equipo_id)

		self.c.execute("""UPDATE equipos
							SET Escudo=%s, Puntuacion=%s
							WHERE Equipo_Id=%s""",
							tuple(datos_escudo))

		self.confirmar()

	# Metodo para actualizar el entrenador de un equipo
	def actualizarEntrenadorEquipo(self, datos_entrenador:List[str], equipo_id:str)->None:

		datos_entrenador.append(equipo_id)

		self.c.execute("""UPDATE equipos
							SET Entrenador=%s, Entrenador_URL=%s, Codigo_Entrenador=%s, Partidos=%s
							WHERE Equipo_Id=%s""",
							tuple(datos_entrenador))

		self.confirmar()

	#Metodo para insertar un estadio
	def insertarEstadio(self, estadio:List[str])->None:

		self.c.execute("""INSERT INTO estadios (Estadio_Id, Codigo_Estadio, Nombre, Direccion, Latitud, Longitud, Ciudad,
												Capacidad, Fecha, Largo, Ancho, Telefono, Cesped)
							VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
							tuple(estadio))

		self.confirmar()

	# Metodo para saber si existe el estadio
	def existe_estadio(self, estadio_id:str)->bool:

		self.c.execute("""SELECT *
							FROM estadios
							WHERE Estadio_Id=%s""",
							(estadio_id,))

		return False if self.c.fetchone() is None else True

	#Metodo para insertar un equipo estadio
	def insertarEquipoEstadio(self, equipo_estadio:tuple)->None:

		self.c.execute("""INSERT INTO equipo_estadio
							VALUES(%s, %s)""",
							equipo_estadio)

		self.confirmar()

	# Metodo para saber si existe el equipo estadio
	def existe_equipo_estadio(self, equipo_id:str, estadio_id:str)->bool:

		self.c.execute("""SELECT *
							FROM equipo_estadio
							WHERE Equipo_Id=%s
							AND Estadio_Id=%s""",
							(equipo_id, estadio_id))

		return False if self.c.fetchone() is None else True

	# Metodo para obtener los codigos de los escudos
	def obtenerCodigoEscudos(self)->List[int]:

		self.c.execute("""SELECT Escudo
							FROM equipos
							WHERE Escudo IS NOT NULL
							ORDER BY Escudo""")

		escudos=self.c.fetchall()

		return list(map(lambda escudo: escudo["escudo"], escudos))

	# Metodo para obtener los codigos de los entrenadores
	def obtenerCodigoEntrenadores(self)->List[int]:

		self.c.execute("""SELECT Codigo_Entrenador
							FROM equipos
							WHERE Codigo_Entrenador IS NOT NULL
							ORDER BY Codigo_Entrenador""")

		codigo_entrenadores=self.c.fetchall()

		return list(map(lambda codigo_entrenador: codigo_entrenador["codigo_entrenador"], codigo_entrenadores))

	# Metodo para obtener los codigos de los presidentes
	def obtenerCodigoPresidentes(self)->List[int]:

		self.c.execute("""SELECT Codigo_Presidente
							FROM equipos
							WHERE Codigo_Presidente IS NOT NULL
							ORDER BY Codigo_Presidente""")

		codigo_presidentes=self.c.fetchall()

		return list(map(lambda codigo_presidente: codigo_presidente["codigo_presidente"], codigo_presidentes))

	# Metodo para obtener los codigos de los estadios
	def obtenerCodigoEstadios(self)->List[int]:

		self.c.execute("""SELECT Codigo_Estadio
							FROM estadios
							WHERE Codigo_Estadio IS NOT NULL
							ORDER BY Codigo_Estadio""")

		codigo_estadios=self.c.fetchall()

		return list(map(lambda codigo_estadio: codigo_estadio["codigo_estadio"], codigo_estadios))

	#Metodo para insertar un partido
	def insertarPartido(self, partido:List[str])->None:

		self.c.execute("""INSERT INTO partidos
							VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
							tuple(partido))

		self.confirmar()

	# Metodo para saber si existe el partido
	def existe_partido(self, partido_id:str)->bool:

		self.c.execute("""SELECT *
							FROM partidos
							WHERE Partido_Id=%s""",
							(partido_id,))

		return False if self.c.fetchone() is None else True

	# Metodo para saber si una tabla esta vacia
	def tabla_vacia(self, tabla:str)->bool:

		try:

			self.c.execute(f"SELECT * FROM {tabla}")

			return True if not self.c.fetchall() else False

		except Exception:

			raise Exception("Tabla no existente")

	# Metodo para obtener la fecha mas reciente de los partidos
	def fecha_mas_reciente(self)->Optional[datetime]:

		self.c.execute("""SELECT MAX(fecha) AS fecha_mas_reciente
							FROM partidos""")

		return self.c.fetchone()["fecha_mas_reciente"]

	# Metodo para obtener el ultimo ano de los partidos
	def ultimo_ano(self)->Optional[int]:

		fecha=self.fecha_mas_reciente()

		return None if fecha is None else fecha.year

	#Metodo para insertar un partido estadio
	def insertarPartidoEstadio(self, partido_estadio:tuple)->None:

		self.c.execute("""INSERT INTO partido_estadio
							VALUES(%s, %s)""",
							partido_estadio)

		self.confirmar()

	# Metodo para saber si existe el partido estadio
	def existe_partido_estadio(self, partido_id:str, estadio_id:str)->bool:

		self.c.execute("""SELECT *
							FROM partido_estadio
							WHERE Partido_Id=%s
							AND Estadio_Id=%s""",
							(partido_id, estadio_id))

		return False if self.c.fetchone() is None else True

	# Metodo para obtener los partidos que no tienen estadio
	def obtenerPartidosSinEstadio(self)->List[tuple]:

		self.c.execute("""SELECT p.Partido_Id, p.Equipo_Id_Local, p.Equipo_Id_Visitante
						FROM partidos p
						LEFT JOIN partido_estadio pe
						USING (Partido_Id)
						WHERE pe.Partido_Id IS NULL
						ORDER BY Fecha""")

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
										partido["equipo_id_local"],
										partido["equipo_id_visitante"]), partidos))

	# Metodo para obtener el valor de una variable
	def obtenerValorVariable(self, nombre_variable:str)->Optional[str]:

		self.c.execute("""SELECT Valor
							FROM variables
							WHERE Nombre=%s""",
							(nombre_variable,))

		valor=self.c.fetchone()

		return None if valor is None else valor["valor"]

	# Metodo para actualizar el valor de una variable
	def actualizarValorVariable(self, nombre_variable:str, valor_variable:str)->None:

		self.c.execute("""UPDATE variables
							SET Valor=%s
							WHERE Nombre=%s""",
							(valor_variable, nombre_variable))

		self.confirmar()

	# Metodo para saber si existe el estadio de un equipo
	def existe_estadio_equipo(self, equipo_id:str)->bool:

		self.c.execute("""SELECT *
							FROM equipo_estadio
							WHERE Equipo_Id=%s""",
							(equipo_id,))

		return False if self.c.fetchone() is None else True

	# Metodo para obtener el estadio del equipo
	def obtenerEstadioEquipo(self, equipo_id:str)->Optional[str]:

		self.c.execute("""SELECT Estadio_Id
							FROM equipo_estadio
							WHERE Equipo_Id=%s""",
							(equipo_id,))

		estadio=self.c.fetchone()

		return None if estadio is None else estadio["estadio_id"]

	#Metodo para insertar una competicion
	def insertarCompeticion(self, competicion:str)->None:

		self.c.execute("""INSERT INTO competiciones (Competicion_Id)
							VALUES(%s)""",
							(competicion,))

		self.confirmar()

	# Metodo para saber si existe la competicion
	def existe_competicion(self, competicion_id:str)->bool:

		self.c.execute("""SELECT *
							FROM competiciones
							WHERE Competicion_Id=%s""",
							(competicion_id,))

		return False if self.c.fetchone() is None else True

	# Metodo para actualizar los datos de una competicion
	def actualizarDatosCompeticion(self, datos_competicion:List[str], competicion_id:str)->None:

		datos_competicion.append(competicion_id)

		self.c.execute("""UPDATE competiciones
							SET Nombre=%s, Codigo_Logo=%s, Codigo_Pais=%s
							WHERE Competicion_Id=%s""",
							tuple(datos_competicion))

		self.confirmar()

	# Metodo para obtener las competiciones
	def obtenerCompeticiones(self)->List[tuple]:

		self.c.execute("""SELECT Competicion_Id
							FROM competiciones
							ORDER BY Competicion_Id""")

		competiciones=self.c.fetchall()

		return list(map(lambda competicion: competicion["competicion_id"], competiciones))

	# Metodo para obtener las competiciones unicas de los equipos
	def obtenerCompeticionesEquipos(self)->List[tuple]:

		self.c.execute("""SELECT DISTINCT(Codigo_Competicion) AS Competicion
							FROM equipos
							WHERE Codigo_Competicion IS NOT NULL
							ORDER BY Codigo_Competicion""")

		competiciones=self.c.fetchall()

		return list(map(lambda competicion: competicion["competicion"], competiciones))

	# Metodo para obtener los codigos de los logos de las competiciones
	def obtenerCodigoLogoCompeticiones(self)->List[str]:

		self.c.execute("""SELECT Codigo_Logo
							FROM competiciones
							WHERE Codigo_Logo IS NOT NULL
							ORDER BY Codigo_Logo""")

		logos_competiciones=self.c.fetchall()

		return list(map(lambda logo_competicion: logo_competicion["codigo_logo"], logos_competiciones))

	# Metodo para obtener los codigos de los paises
	def obtenerCodigoPaises(self)->List[str]:

		self.c.execute("""SELECT DISTINCT(Codigo_Pais)
							FROM competiciones
							WHERE Codigo_Pais IS NOT NULL
							ORDER BY Codigo_Pais""")

		paises=self.c.fetchall()

		return list(map(lambda pais: pais["codigo_pais"], paises))

	#Metodo para insertar un campeon de competicion
	def insertarCampeonCompeticion(self, datos_campeon:List[str])->None:

		self.c.execute("""INSERT INTO competiciones_campeones
							VALUES(%s, %s, %s)""",
							tuple(datos_campeon))

		self.confirmar()

	# Metodo para saber si existe un campeon de competicion
	def existe_campeon_competicion(self, competicion_id:str, temporada:int, equipo_id:str)->bool:

		self.c.execute("""SELECT *
							FROM competiciones_campeones
							WHERE Competicion_Id=%s
							AND Temporada=%s
							AND Equipo_Id=%s""",
							(competicion_id, temporada, equipo_id))

		return False if self.c.fetchone() is None else True

	#Metodo para insertar un partido competicion
	def insertarPartidoCompeticion(self, partido_competicion:tuple)->None:

		self.c.execute("""INSERT INTO partido_competicion
							VALUES(%s, %s)""",
							partido_competicion)

		self.confirmar()

	# Metodo para saber si existe el partido competicion
	def existe_partido_competicion(self, partido_id:str, competicion_id:str)->bool:

		self.c.execute("""SELECT *
							FROM partido_competicion
							WHERE Partido_Id=%s
							AND Competicion_Id=%s""",
							(partido_id, competicion_id))

		return False if self.c.fetchone() is None else True

	# Metodo para obtener los partidos que no tienen competicion
	def obtenerPartidosSinCompeticion(self)->List[tuple]:

		self.c.execute("""SELECT p.Partido_Id, p.Equipo_Id_Local, p.Equipo_Id_Visitante
						FROM partidos p
						LEFT JOIN partido_competicion pc
						USING (Partido_Id)
						WHERE pc.Partido_Id IS NULL
						ORDER BY Fecha""")

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
										partido["equipo_id_local"],
										partido["equipo_id_visitante"]), partidos))

	#Metodo para insertar un jugador
	def insertarJugador(self, jugador:str)->None:

		self.c.execute("""INSERT INTO jugadores (Jugador_Id)
							VALUES(%s)""",
							(jugador,))

		self.confirmar()

	# Metodo para saber si existe el jugador
	def existe_jugador(self, jugador_id:str)->bool:

		self.c.execute("""SELECT *
							FROM jugadores
							WHERE Jugador_Id=%s""",
							(jugador_id,))

		return False if self.c.fetchone() is None else True

	#Metodo para insertar una temporada jugadores
	def insertarTemporadaJugadores(self, temporada:int)->None:

		self.c.execute("""INSERT INTO temporada_jugadores
							VALUES(%s)""",
							(temporada,))

		self.confirmar()

	# Metodo para obtener el ultimo ano de los jugadores
	def ultimo_ano_jugadores(self)->Optional[int]:

		self.c.execute("""SELECT temporada
							FROM temporada_jugadores""")

		temporada=self.c.fetchone()

		return None if temporada is None else temporada["temporada"]

	# Metodo para actualizar el valor de la temporada de la temporada de los jugadores
	def actualizarTemporadaJugadores(self, temporada:int)->None:

		self.c.execute("""UPDATE temporada_jugadores
							SET Temporada=%s""",
							(temporada,))

		self.confirmar()

	# Metodo para actualizar los datos de un jugador
	def actualizarDatosJugador(self, datos_jugador:List[str], jugador_id:str)->None:

		datos_jugador.append(jugador_id)

		self.c.execute("""UPDATE jugadores
							SET Nombre=%s, Equipo_Id=%s, Codigo_Pais=%s, Codigo_Jugador=%s,
							Puntuacion=%s, Valor=%s, Dorsal=%s, Posicion=%s
							WHERE Jugador_Id=%s""",
							tuple(datos_jugador))

		self.confirmar()

	# Metodo para obtener los jugadores
	def obtenerJugadores(self)->List[str]:

		self.c.execute("""SELECT Jugador_Id
						FROM jugadores
						ORDER BY Jugador_Id""")

		jugadores=self.c.fetchall()

		return list(map(lambda jugador: jugador["jugador_id"], jugadores))

	# Metodo para obtener los codigos de los jugadores
	def obtenerCodigoJugadores(self)->List[str]:

		self.c.execute("""SELECT Codigo_Jugador
							FROM jugadores
							WHERE Codigo_Jugador IS NOT NULL
							ORDER BY Codigo_Jugador""")

		jugadores=self.c.fetchall()

		return list(map(lambda jugador: jugador["codigo_jugador"], jugadores))

	# Metodo para obtener los codigos de los paises de los jugadores
	def obtenerCodigoPaisesJugadores(self)->List[str]:

		self.c.execute("""SELECT DISTINCT(Codigo_Pais)
							FROM jugadores
							WHERE Codigo_Pais IS NOT NULL
							ORDER BY Codigo_Pais""")

		paises=self.c.fetchall()

		return list(map(lambda pais: pais["codigo_pais"], paises))

	# Metodo para insertar un partido goleador
	def insertarPartidoGoleador(self, partido_goleador:tuple)->None:

		self.c.execute("""INSERT INTO partido_goleador
							VALUES(%s, %s, %s, %s, %s)""",
							partido_goleador)

		self.confirmar()

	# Metodo para saber si existe el partido goleador
	def existe_partido_goleador(self, partido_id:str, jugador_id:str, minuto:int, anadido:int)->bool:

		self.c.execute("""SELECT *
							FROM partido_goleador
							WHERE Partido_Id=%s
							AND Jugador_Id=%s
							AND Minuto=%s
							AND Anadido=%s""",
							(partido_id, jugador_id, minuto, anadido))

		return False if self.c.fetchone() is None else True

	# Metodo para obtener los partidos que no tienen goleadores
	def obtenerPartidosSinGoleadores(self)->List[tuple]:

		self.c.execute("""SELECT p.Partido_Id, p.Equipo_Id_Local, p.Equipo_Id_Visitante
						FROM partidos p
						LEFT JOIN partido_goleador pg
						USING (Partido_Id)
						WHERE pg.Partido_Id IS NULL
						AND p.Marcador!='0-0'
						ORDER BY p.Fecha""")

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
										partido["equipo_id_local"],
										partido["equipo_id_visitante"]), partidos))

	# Metodo para actualizar los datos de un estadio
	def actualizarDatosEstadio(self, datos_estadio:List[str], estadio_id:str)->None:

		datos_estadio.append(estadio_id)

		self.c.execute("""UPDATE estadios
							SET Pais=%s, Codigo_Pais=%s
							WHERE Estadio_Id=%s""",
							tuple(datos_estadio))

		self.confirmar()

	# Metodo para obtener los estadios
	def obtenerEstadios(self)->List[str]:

		self.c.execute("""SELECT Estadio_Id
						FROM estadios
						ORDER BY Estadio_Id""")

		estadios=self.c.fetchall()

		return list(map(lambda estadio: estadio["estadio_id"], estadios))

	# Metodo para obtener los codigos de los paises de los estadios
	def obtenerCodigoPaisesEstadios(self)->List[str]:

		self.c.execute("""SELECT DISTINCT(Codigo_Pais)
							FROM estadios
							WHERE Codigo_Pais IS NOT NULL
							ORDER BY Codigo_Pais""")

		paises=self.c.fetchall()

		return list(map(lambda pais: pais["codigo_pais"], paises))

	# Metodo para obtener los codigos de los paises de los equipos
	def obtenerCodigoPaisesEquipos(self)->List[str]:

		self.c.execute("""SELECT DISTINCT(Codigo_Pais)
							FROM equipos
							WHERE Codigo_Pais IS NOT NULL
							ORDER BY Codigo_Pais""")

		paises=self.c.fetchall()

		return list(map(lambda pais: pais["codigo_pais"], paises))

	#Metodo para insertar un proximo partido
	def insertarProximoPartido(self, proximo_partido:List[str])->None:

		self.c.execute("""INSERT INTO proximos_partidos
							VALUES(%s, %s, %s, %s, %s, %s)""",
							tuple(proximo_partido))

		self.confirmar()

	# Metodo para saber si existe el proximo partido
	def existe_proximo_partido(self, partido_id:str)->bool:

		self.c.execute("""SELECT *
							FROM proximos_partidos
							WHERE Partido_Id=%s""",
							(partido_id,))

		return False if self.c.fetchone() is None else True

	# Metodo para vaciar la tabla de proximos partidos
	def vaciar_proximos_partidos(self)->None:

		self.c.execute("""DELETE FROM proximos_partidos""")

		self.confirmar()

	# Metodo para obtener las direcciones de los estadios sin coordenadas
	def obtenerEstadiosSinCoordenadas(self)->List[tuple]:

		self.c.execute("""SELECT Estadio_Id, Nombre, Direccion
							FROM estadios
							WHERE Latitud IS NULL
							OR Longitud IS NULL
							ORDER BY Estadio_Id""")

		estadios=self.c.fetchall()

		return list(map(lambda estadio: (estadio["estadio_id"],
										estadio["nombre"],
										estadio["direccion"]), estadios))

	# Metodo para actualizar las coordenadas de un estadio
	def actualizarCoordenadasEstadio(self, datos_estadio:List[float], estadio_id:str)->None:

		datos_estadio.append(estadio_id)

		self.c.execute("""UPDATE estadios
							SET Latitud=%s, Longitud=%s
							WHERE Estadio_Id=%s""",
							tuple(datos_estadio))

		self.confirmar()

	#Metodo para insertar un entrenador
	def insertarEntrenador(self, entrenador:str)->None:

		self.c.execute("""INSERT INTO entrenadores (Entrenador_Id)
							VALUES(%s)""",
							(entrenador,))

		self.confirmar()

	# Metodo para saber si existe el entrenador
	def existe_entrenador(self, entrenador_id:str)->bool:

		self.c.execute("""SELECT *
							FROM entrenadores
							WHERE Entrenador_Id=%s""",
							(entrenador_id,))

		return False if self.c.fetchone() is None else True

	# Metodo para actualizar los datos de un entrenador
	def actualizarDatosEntrenador(self, datos_entrenador:List[str], entrenador_id:str)->None:

		datos_entrenador.append(entrenador_id)

		self.c.execute("""UPDATE entrenadores
							SET Nombre=%s, Equipo_Id=%s, Codigo_Pais=%s, Codigo_Entrenador=%s, Puntuacion=%s
							WHERE Entrenador_Id=%s""",
							tuple(datos_entrenador))
		self.confirmar()

	# Metodo para obtener los entrenadores
	def obtenerEntrenadores(self)->List[tuple]:

		self.c.execute("""SELECT Entrenador_Id
						FROM entrenadores
						ORDER BY Entrenador_Id""")

		entrenadores=self.c.fetchall()

		return list(map(lambda entrenador: entrenador["entrenador_id"], entrenadores))

	# Metodo para obtener los entrenadores unicos de los equipos
	def obtenerEntrenadoresEquipos(self)->List[tuple]:

		self.c.execute("""SELECT DISTINCT(Entrenador_URL) AS Entrenador
							FROM equipos
							WHERE Entrenador_URL IS NOT NULL
							ORDER BY Entrenador_URL""")

		entrenadores=self.c.fetchall()

		return list(map(lambda entrenador: entrenador["entrenador"], entrenadores))

	# Metodo para obtener los codigos de los paises de los entrenadores
	def obtenerCodigoPaisesEntrenadores(self)->List[str]:

		self.c.execute("""SELECT DISTINCT(Codigo_Pais)
							FROM entrenadores
							WHERE Codigo_Pais IS NOT NULL
							ORDER BY Codigo_Pais""")

		paises=self.c.fetchall()

		return list(map(lambda pais: pais["codigo_pais"], paises))

	# Metodo para insertar un equipo de un jugador
	def insertarEquipoJugador(self, equipo_jugador:tuple)->None:

		self.c.execute("""INSERT INTO jugadores_equipo
							VALUES(%s, %s, %s, %s, %s)""",
							equipo_jugador)

		self.confirmar()

	# Metodo para saber si existe el equipo de un jugador
	def existe_equipo_jugador(self, jugador_id:str, equipo_id:str)->bool:

		self.c.execute("""SELECT *
							FROM jugadores_equipo
							WHERE Jugador_Id=%s
							AND Equipo_Id=%s""",
							(jugador_id, equipo_id))

		return False if self.c.fetchone() is None else True

	# Metodo para actualizar los datos del equipo de un jugador
	def actualizarDatosEquipoJugador(self, datos_equipo_jugador:List[str], jugador_id:str, equipo_id:str)->None:

		datos_equipo_jugador.append(jugador_id)

		datos_equipo_jugador.append(equipo_id)

		self.c.execute("""UPDATE jugadores_equipo
							SET Temporadas=%s, Goles=%s, Partidos=%s
							WHERE Jugador_Id=%s
							AND Equipo_Id=%s""",
							tuple(datos_equipo_jugador))
		self.confirmar()