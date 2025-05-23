import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List
import pandas as pd

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:

			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para confirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	# Metodo para vaciar la BBDD
	def vaciarBBDD(self)->None:

		self.c.execute("DELETE FROM equipos")

		self.c.execute("DELETE FROM estadios")

		self.c.execute("DELETE FROM partidos")

		self.c.execute("DELETE FROM competiciones")

		self.c.execute("DELETE FROM jugadores")

		self.c.execute("DELETE FROM entrenadores")

		self.c.execute("DELETE FROM temporada_jugadores")

		self.c.execute("DELETE FROM usuarios")

		self.c.execute("DELETE FROM partidos_asistidos")

		self.c.execute("DELETE FROM proximos_partidos")

		self.c.execute("DELETE FROM trayecto_partido_asistido")

		self.confirmar()

	# Metodo para insertar un usuario
	def insertarUsuario(self, usuario:str, correo:str, contrasena:str, nombre:str,
						apellido:str, fecha_nacimiento:str, codciudad:int, equipo_id:str)->None:

		self.c.execute("""INSERT INTO usuarios
							VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
							(usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, codciudad, equipo_id))

		self.confirmar()

	# Metodo para comprobar si ya existe un usuario
	def existe_usuario(self, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		return False if not self.c.fetchone() else True

	# Metodo para comprobar si ya existe un equipo
	def existe_equipo(self, equipo_id:str)->bool:

		self.c.execute("""SELECT *
						FROM equipos
						WHERE equipo_id=%s""",
						(equipo_id,))

		return False if not self.c.fetchone() else True

	# Metodo para obtener la contrasena de un usuario
	def obtenerContrasenaUsuario(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT contrasena
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		contrasena=self.c.fetchone()

		return None if not contrasena else contrasena["contrasena"]

	# Metodo para obtener el nombre del usuario
	def obtenerNombre(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT nombre
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		nombre=self.c.fetchone()

		return None if not nombre else nombre["nombre"]

	# Metodo para obtener el equipo del usuario
	def obtenerEquipo(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT equipo_id
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		equipo=self.c.fetchone()

		return None if not equipo else equipo["equipo_id"]

	# Metodo para obtener el nombre del equipo
	def obtenerNombreEquipo(self, equipo_id:str)->Optional[str]:

		self.c.execute("""SELECT nombre_completo
						FROM equipos
						WHERE equipo_id=%s""",
						(equipo_id,))

		nombre_equipo=self.c.fetchone()

		return None if not nombre_equipo else nombre_equipo["nombre_completo"]

	# Metodo para obtener el estadio de un equipo
	def estadio_equipo(self, equipo_id:str)->Optional[tuple]:

		self.c.execute("""SELECT estadio_id
							FROM equipo_estadio
							WHERE equipo_id=%s""",
							(equipo_id,))

		estadio=self.c.fetchone()

		return None if not estadio else estadio["estadio_id"]

	# Metodo para obtener los partidos de un equipo
	def obtenerPartidosEquipo(self, equipo_id:str)->List[tuple]:

		self.c.execute("""SELECT p.partido_id, p.marcador, p.fecha,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								p.competicion,
								pe.estadio_id as estadio_partido,
								CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_ganado,
						       CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_perdido,
   						       CASE WHEN p.resultado LIKE %s
							            THEN 1
							            ELSE 0
						       END as partido_empatado
						FROM partidos p
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						LEFT JOIN partido_estadio pe
						ON p.partido_id=pe.partido_id
						WHERE p.equipo_id_local=%s
						OR p.equipo_id_visitante=%s
						ORDER BY fecha DESC""",
						(r'%Local%', equipo_id, r'%Visitante%', equipo_id, 
						r'%Visitante%', equipo_id, r'%Local%', equipo_id, 
						r'%Empate%', equipo_id, equipo_id))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["marcador"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["cod_local"],
											partido["local"],
											partido["escudo_local"],
											partido["cod_visitante"],
											partido["visitante"],
											partido["escudo_visitante"],
											partido["competicion"],
											partido["estadio_partido"],
											partido["partido_ganado"],
											partido["partido_perdido"],
											partido["partido_empatado"]), partidos))

	# Metodo para obtener los partidos de un equipo de local
	def obtenerPartidosEquipoLocal(self, equipo_id:str)->List[tuple]:

		partidos=self.obtenerPartidosEquipo(equipo_id)

		return list(filter(lambda partido: partido[3]==equipo_id, partidos))

	# Metodo para obtener los partidos de un equipo de visitante
	def obtenerPartidosEquipoVisitante(self, equipo_id:str)->List[tuple]:

		partidos=self.obtenerPartidosEquipo(equipo_id)

		return list(filter(lambda partido: partido[6]==equipo_id, partidos))

	# Metodo para obtener los partidos de un equipo en casa
	def obtenerPartidosCasa(self, equipo_id:str)->List[tuple]:

		estadio=self.estadio_equipo(equipo_id)

		if not estadio:

			return self.obtenerPartidosEquipoLocal(equipo_id)

		partidos=self.obtenerPartidosEquipo(equipo_id)

		def filtrarPartidoCasa(partido:List[str], estadio:str, equipo_id:str)->bool:

			if partido[10]==estadio:

				return True

			return True if not partido[10] and partido[3]==equipo_id else False

		return list(filter(lambda partido: filtrarPartidoCasa(partido, estadio, equipo_id), partidos))

	# Metodo para obtener los partidos de un equipo fuera de casa
	def obtenerPartidosFuera(self, equipo_id:str)->List[tuple]:

		estadio=self.estadio_equipo(equipo_id)

		if not estadio:

			return self.obtenerPartidosEquipoVisitante(equipo_id)

		partidos=self.obtenerPartidosEquipo(equipo_id)

		def filtrarPartidoFuera(partido:List[str], estadio:str, equipo_id:str)->bool:

			if partido[10]!=estadio and partido[10]:

				return True

			return True if not partido[10] and partido[6]==equipo_id else False

		return list(filter(lambda partido: filtrarPartidoFuera(partido, estadio, equipo_id), partidos))

	# Metodo para obtener las temporadas de los partidos
	def obtenerTemporadasEquipo(self, equipo_id:str)->List[tuple]:

		self.c.execute("""SELECT DISTINCT CAST(LEFT(partido_id, 4) AS INTEGER) AS temporada
						FROM partidos
						WHERE equipo_id_local=%s
						OR equipo_id_visitante=%s
						ORDER BY temporada DESC""",
						(equipo_id, equipo_id))

		temporadas=self.c.fetchall()

		return list(map(lambda temporada: temporada["temporada"], temporadas))

	# Metodo para saber si existe el partido
	def existe_partido(self, partido_id:str)->bool:

		self.c.execute("""SELECT *
							FROM partidos
							WHERE Partido_Id=%s""",
							(partido_id,))

		return False if not self.c.fetchone() else True

	# Metodo para obtener la informacion de un partido
	def obtenerPartido(self, partido_id:str)->Optional[tuple]:

		self.c.execute("""SELECT p.marcador, p.fecha, p.hora, p.competicion,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								pe.estadio_id as cod_estadio, e.nombre as nombre_estadio,
								CASE WHEN pe.estadio_id IS NULL
										THEN False
										ELSE True
								END as estadio_existe,
								CASE WHEN e.codigo_estadio IS NULL
										THEN -1
										ELSE e.codigo_estadio
								END as estadio_partido,
								CAST(LEFT(p.partido_id, 4) as INT) as temporada,
								pc.competicion_id,
								CASE WHEN pc.competicion_id IS NULL
										THEN False
										ELSE True
								END as competicion_existe
						FROM partidos p
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						LEFT JOIN partido_estadio pe
						ON p.partido_id=pe.partido_id
						LEFT JOIN estadios e
						ON pe.estadio_id=e.estadio_id
						LEFT JOIN partido_competicion pc
						ON p.partido_id=pc.partido_id
						WHERE p.partido_id=%s""",
						(partido_id,))

		partido=self.c.fetchone()

		return None if not partido else (partido["marcador"],
											partido["fecha"].strftime("%d-%m-%Y"),
											partido["hora"],
											partido["competicion"],
											partido["cod_local"],
											partido["local"],
											partido["escudo_local"],
											partido["cod_visitante"],
											partido["visitante"],
											partido["escudo_visitante"],
											partido["cod_estadio"],
											partido["nombre_estadio"],
											partido["estadio_existe"],
											partido["estadio_partido"],
											partido["temporada"],
											partido["competicion_id"],
											partido["competicion_existe"])

	# Metodo para saber si un equipo esta en un partido
	def equipo_partido(self, equipo_id:str, partido_id:str)->bool:

		partido=self.obtenerPartido(partido_id)

		return partido is not None and (partido[4]==equipo_id or partido[7]==equipo_id)

	# Metodo para obtener los datos de un equipo
	def obtenerDatosEquipo(self, equipo_id:str)->Optional[tuple]:

		self.c.execute("""SELECT e.equipo_id, e.nombre_completo, e.nombre, e.siglas,
								CASE WHEN e.escudo IS NULL
										THEN -1
										ELSE e.escudo
								END as escudo,
								e.puntuacion, e.pais, e.ciudad, e.competicion, e.temporadas, e.fundacion, e.entrenador,
								CASE WHEN e.codigo_entrenador IS NULL
										THEN -1
										ELSE e.codigo_entrenador
								END as codigo_entrenador,
								CASE WHEN e.entrenador IS NULL
										THEN False
										ELSE True
								END as entrenador_existe,
								e.presidente,
								CASE WHEN e.codigo_presidente IS NULL
										THEN -1
										ELSE e.codigo_presidente
								END as codigo_presidente,
								CASE WHEN e.presidente IS NULL
										THEN False
										ELSE True
								END as presidente_existe,
								ee.estadio_id as cod_estadio, es.nombre as nombre_estadio,
								CASE WHEN ee.estadio_id IS NULL
										THEN False
										ELSE True
								END as estadio_existe,
								CASE WHEN es.codigo_estadio IS NULL
										THEN -1
										ELSE es.codigo_estadio
								END as estadio_equipo,
								CASE WHEN e.codigo_pais IS NULL
										THEN '-1'
										ELSE e.codigo_pais
								END as equipo_pais,
								e.codigo_competicion,
								CASE WHEN c.competicion_id IS NULL
										THEN False
										ELSE True
								END as competicion_existe,
								e.entrenador_url as entrenador_id
						FROM equipos e
						LEFT JOIN equipo_estadio ee
						ON e.equipo_id=ee.equipo_id
						LEFT JOIN estadios es
						ON ee.estadio_id=es.estadio_id
						LEFT JOIN competiciones c
						ON e.codigo_competicion=c.competicion_id
						WHERE e.equipo_id=%s""",
						(equipo_id,))

		equipo=self.c.fetchone()

		return None if not equipo else (equipo["equipo_id"],
										equipo["nombre_completo"],
										equipo["nombre"],
										equipo["siglas"],
										equipo["escudo"],
										equipo["puntuacion"],
										equipo["pais"],
										equipo["ciudad"],
										equipo["competicion"],
										equipo["temporadas"],
										equipo["fundacion"],
										equipo["entrenador"],
										equipo["codigo_entrenador"],
										equipo["entrenador_existe"],
										equipo["presidente"],
										equipo["codigo_presidente"],
										equipo["presidente_existe"],
										equipo["cod_estadio"],
										equipo["nombre_estadio"],
										equipo["estadio_existe"],
										equipo["estadio_equipo"],
										equipo["codigo_competicion"],
										equipo["competicion_existe"],
										equipo["equipo_pais"],
										equipo["entrenador_id"])

	# Metodo para obtener el partido siguiente de un partido
	def obtenerPartidoSiguiente(self, partido_id:str, equipo_id:str)->Optional[str]:

		self.c.execute("""SELECT partido_id
						FROM partidos
						WHERE fecha>(SELECT fecha
						    		FROM partidos
						    		WHERE partido_id=%s
						    		AND (equipo_id_local=%s
									OR equipo_id_visitante=%s))
						ORDER BY fecha ASC
						LIMIT 1""",
						(partido_id,  equipo_id, equipo_id))

		partido=self.c.fetchone()

		return None if not partido else partido["partido_id"]

	# Metodo para obtener el partido anterior de un partido
	def obtenerPartidoAnterior(self, partido_id:str, equipo_id:str)->Optional[str]:

		self.c.execute("""SELECT partido_id
						FROM partidos
						WHERE fecha<(SELECT fecha
						    		FROM partidos
						    		WHERE partido_id=%s
						    		AND (equipo_id_local=%s
									OR equipo_id_visitante=%s))
						ORDER BY fecha DESC
						LIMIT 1""",
						(partido_id,  equipo_id, equipo_id))

		partido=self.c.fetchone()

		return None if not partido else partido["partido_id"]

	# Metodo para comprobar si existe un estadio
	def existe_estadio(self, estadio_id:str)->bool:

		self.c.execute("""SELECT *
						FROM estadios
						WHERE estadio_id=%s""",
						(estadio_id,))

		return False if not self.c.fetchone() else True

	# Metodo para obtener la informacion de un estadio
	def obtenerEstadio(self, estadio_id:str)->Optional[tuple]:

		self.c.execute("""SELECT e.nombre,
								CASE WHEN e.codigo_estadio IS NULL
										THEN -1
										ELSE e.codigo_estadio
								END as imagen_estadio,
								e.direccion, e.latitud, e.longitud, e.ciudad, e.pais,
								CAST(e.capacidad AS TEXT) AS espectadores, e.fecha, e.largo, e.ancho,
								(CASE WHEN e.codigo_pais IS NULL
					                THEN 
					                	CASE WHEN eq.codigo_pais IS NULL
					                		THEN '-1'
					                		ELSE eq.codigo_pais
					           			END
					                ELSE e.codigo_pais
					           	END) as bandera_pais
						FROM estadios e
	                    LEFT JOIN equipo_estadio ee
						ON e.estadio_id=ee.estadio_id
						LEFT JOIN equipos eq
						ON ee.equipo_id=eq.equipo_id
						WHERE e.estadio_id=%s""",
						(estadio_id,))

		estadio=self.c.fetchone()

		return None if not estadio else (estadio["nombre"],
										estadio["imagen_estadio"],
										estadio["direccion"],
										estadio["latitud"],
										estadio["longitud"],
										estadio["ciudad"],
										estadio["espectadores"],
										estadio["fecha"],
										estadio["largo"],
										estadio["ancho"],
										estadio["pais"],
										estadio["bandera_pais"])

	# Metodo para obtener el equipo de un estadio
	def obtenerEquipoEstadio(self, estadio_id:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.equipo_id, e.nombre,
								CASE WHEN e.escudo IS NULL
										THEN -1
										ELSE e.escudo
								END as escudo_equipo
							FROM equipo_estadio ee
							JOIN equipos e
							ON ee.equipo_id=e.equipo_id
							WHERE ee.estadio_id=%s""",
							(estadio_id,))

		equipos=self.c.fetchall()

		return list(map(lambda equipo: (equipo["equipo_id"],
										equipo["nombre"],
										equipo["escudo_equipo"]), equipos))

	# Metodo para saber si existe la competicion
	def existe_competicion(self, competicion_id:str)->bool:

		self.c.execute("""SELECT *
							FROM competiciones
							WHERE Competicion_Id=%s""",
							(competicion_id,))

		return False if not self.c.fetchone() else True

	# Metodo para obtener los datos de una competicion
	def obtenerDatosCompeticion(self, competicion_id:str)->Optional[tuple]:

		self.c.execute("""SELECT competicion_id, nombre,
								CASE WHEN codigo_logo IS NULL
										THEN '-1'
										ELSE codigo_logo
								END as logo,
								CASE WHEN codigo_pais IS NULL
										THEN '-1'
										ELSE codigo_pais
								END as pais
						FROM competiciones
						WHERE competicion_id=%s""",
						(competicion_id,))

		competicion=self.c.fetchone()

		return None if not competicion else (competicion["competicion_id"],
											competicion["nombre"],
											competicion["logo"],
											competicion["pais"])

	# Metodo para obtener los equipos de una competicion
	def obtenerEquiposCompeticion(self, competicion_id:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT equipo_id, nombre, escudo
						FROM equipos
						WHERE codigo_competicion=%s
						ORDER BY equipo_id""",
						(competicion_id,))

		equipos=self.c.fetchall()

		return list(map(lambda equipo: (equipo["equipo_id"],
										equipo["nombre"],
										equipo["escudo"]), equipos))

	# Metodo para obtener los campeones de una competicion
	def obtenerCampeonesCompeticion(self, competicion_id:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT cc.competicion_id, cc.temporada, e.equipo_id, e.nombre,
								CASE WHEN e.escudo IS NULL
										THEN -1
										ELSE e.escudo
								END as escudo_equipo
						FROM competiciones_campeones cc
						LEFT JOIN equipos e
						ON cc.equipo_id=e.equipo_id
						WHERE competicion_id=%s
						ORDER BY cc.temporada DESC
						LIMIT 4""",
						(competicion_id,))

		campeones=self.c.fetchall()

		return list(map(lambda campeon: (campeon["competicion_id"],
										campeon["temporada"],
										campeon["equipo_id"],
										campeon["nombre"],
										campeon["escudo_equipo"]), campeones))

	# Metodo para obtener los partidos de una competicion
	def obtenerPartidosCompeticion(self, competicion_id:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT pc.competicion_id, pc.partido_id, p.marcador, p.fecha,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante
						FROM partido_competicion pc
						LEFT JOIN partidos p
						ON pc.partido_id=p.partido_id
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						WHERE pc.competicion_id=%s
						ORDER BY p.fecha DESC
						LIMIT 2""",
						(competicion_id,))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["competicion_id"],
										partido["partido_id"],
										partido["marcador"],
										partido["fecha"].strftime("%d/%m/%Y"),
										partido["cod_local"],
										partido["local"],
										partido["escudo_local"],
										partido["cod_visitante"],
										partido["visitante"],
										partido["escudo_visitante"]), partidos))

	# Metodo para obtener los datos de los equipos
	def obtenerDatosEquipos(self)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.equipo_id, e.nombre,
								CASE WHEN e.escudo IS NULL
										THEN -1
										ELSE e.escudo
								END as escudo,
								CASE WHEN e.codigo_pais IS NULL
										THEN '-1'
										ELSE e.codigo_pais
								END as equipo_pais,
								c.codigo_logo
						FROM equipos e
						LEFT JOIN competiciones c
						ON e.codigo_competicion=c.competicion_id
						WHERE e.puntuacion IS NOT NULL
						AND e.puntuacion>55
						ORDER BY e.equipo_id""")

		equipos=self.c.fetchall()

		return list(map(lambda equipo: (equipo["equipo_id"],
										equipo["nombre"],
										equipo["escudo"],
										equipo["equipo_pais"],
										equipo["codigo_logo"]), equipos))

	# Metodo para obtener los datos de las competiciones
	def obtenerDatosCompeticiones(self)->List[Optional[tuple]]:

		self.c.execute("""SELECT competicion_id, nombre,
								CASE WHEN codigo_logo IS NULL
										THEN '-1'
										ELSE codigo_logo
								END as logo,
								CASE WHEN codigo_pais IS NULL
										THEN '-1'
										ELSE codigo_pais
								END as pais
						FROM competiciones
						ORDER BY competicion_id""")

		competiciones=self.c.fetchall()

		return list(map(lambda competicion: (competicion["competicion_id"],
											competicion["nombre"],
											competicion["logo"],
											competicion["pais"]), competiciones))

	# Metodo para comprobar si ya existe un jugador
	def existe_jugador(self, jugador_id:str)->bool:

		self.c.execute("""SELECT *
						FROM jugadores
						WHERE jugador_id=%s""",
						(jugador_id,))

		return False if not self.c.fetchone() else True

	# Metodo para obtener los datos de un jugador
	def obtenerDatosJugador(self, jugador_id:str)->Optional[tuple]:

		self.c.execute("""SELECT j.jugador_id, j.nombre,
								CASE WHEN j.codigo_pais IS NULL
										THEN '-1'
										ELSE j.codigo_pais
								END as pais,
								CASE WHEN j.codigo_jugador IS NULL
										THEN '-1'
										ELSE j.codigo_jugador
								END as jugador,
								j.puntuacion, j.dorsal, j.valor, j.posicion, e.equipo_id, e.nombre as nombre_equipo,
								CASE WHEN e.escudo IS NULL
										THEN -1
										ELSE e.escudo
								END as escudo_equipo,
								CASE WHEN j.equipo_id IS NULL
										THEN False
										ELSE True
								END as equipo_existe
						FROM jugadores j
						LEFT JOIN equipos e
						ON j.equipo_id=e.equipo_id
						WHERE j.jugador_id=%s""",
						(jugador_id,))

		jugador=self.c.fetchone()

		return None if not jugador else (jugador["jugador_id"],
										jugador["nombre"],
										jugador["pais"],
										jugador["jugador"],
										jugador["puntuacion"],
										jugador["dorsal"],
										jugador["valor"],
										jugador["posicion"],
										jugador["equipo_id"],
										jugador["nombre_equipo"],
										jugador["escudo_equipo"],
										jugador["equipo_existe"])

	# Metodo para obtener los datos de los jugadores
	def obtenerDatosJugadores(self)->List[Optional[tuple]]:

		self.c.execute("""SELECT j.jugador_id, j.nombre,
								CASE WHEN j.codigo_pais IS NULL
										THEN '-1'
										ELSE j.codigo_pais
								END as pais,
								CASE WHEN j.codigo_jugador IS NULL
										THEN '-1'
										ELSE j.codigo_jugador
								END as jugador,
								CASE WHEN e.escudo IS NULL
										THEN -1
										ELSE e.escudo
								END as escudo_equipo
						FROM jugadores j
						LEFT JOIN equipos e
						ON j.equipo_id=e.equipo_id
						WHERE j.puntuacion IS NOT NULL
						AND j.puntuacion>75
						ORDER BY j.jugador_id""")

		jugadores=self.c.fetchall()

		return list(map(lambda jugador: (jugador["jugador_id"],
										jugador["nombre"],
										jugador["pais"],
										jugador["jugador"],
										jugador["escudo_equipo"]), jugadores))

	# Metodo para obtener los datos del jugador de un equipo con mayor valoracion
	def obtenerDatosJugadorEquipoValoracion(self, equipo_id:str)->Optional[tuple]:

		self.c.execute("""SELECT jugador_id, nombre,
								CASE WHEN codigo_jugador IS NULL
										THEN '-1'
										ELSE codigo_jugador
								END as jugador
						FROM jugadores
						WHERE equipo_id=%s
						ORDER BY puntuacion DESC
						LIMIT 1""",
						(equipo_id,))

		jugador=self.c.fetchone()

		return None if not jugador else (jugador["jugador_id"],
										jugador["nombre"],
										jugador["jugador"])

	# Metodo para obtener los goleadores de un partido
	def obtenerGoleadoresPartido(self, partido_id:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT pg.partido_id, pg.minuto, pg.anadido, pg.local, j.jugador_id, j.nombre,
								CASE WHEN j.codigo_jugador IS NULL
										THEN '-1'
										ELSE j.codigo_jugador
								END as jugador
						FROM partido_goleador pg
						LEFT JOIN jugadores j
						ON pg.jugador_id=j.jugador_id
						WHERE pg.partido_id=%s
						ORDER BY pg.minuto, pg.anadido""",
						(partido_id,))

		goleadores=self.c.fetchall()

		def formato_minuto_anadido(minuto:int, anadido:int)->str:

			minuto_str=f"{minuto}'"

			return minuto_str if anadido==0 else f"{minuto_str}+{anadido}"
			
		return list(map(lambda goleador: (goleador["partido_id"],
											formato_minuto_anadido(goleador["minuto"], goleador["anadido"]),
											goleador["local"],
											goleador["jugador_id"],
											goleador["nombre"],
											goleador["jugador"]), goleadores))

	# Metodo para obtener el ultimo partido de un equipo
	def ultimoPartidoEquipo(self, equipo_id:str)->Optional[tuple]:

		self.c.execute("""SELECT p.partido_id, 
								CASE WHEN p.equipo_id_local=%s
									THEN p.equipo_id_visitante
									ELSE p.equipo_id_local
								END as equipo,
								CASE 
									WHEN p.equipo_id_local=%s AND e2.escudo IS NULL THEN -1
									WHEN p.equipo_id_visitante=%s AND e1.escudo IS NULL THEN -1
									WHEN p.equipo_id_local=%s AND e2.escudo IS NOT NULL THEN e2.escudo
									WHEN p.equipo_id_visitante=%s AND e1.escudo IS NOT NULL THEN e1.escudo
								END as escudo,
								p.marcador, p.fecha,
								CASE
									WHEN p.resultado LIKE %s AND p.equipo_id_local=%s THEN 1
									WHEN p.resultado LIKE %s AND p.equipo_id_visitante=%s THEN 1
									WHEN p.resultado LIKE %s AND p.equipo_id_local=%s THEN 0
									WHEN p.resultado LIKE %s AND p.equipo_id_visitante=%s THEN 0
									WHEN p.resultado LIKE %s THEN 2
						       END as resultado,
								CASE WHEN c.codigo_logo IS NULL
										THEN '-1'
										ELSE codigo_logo
								END as logo
						FROM partidos p
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						LEFT JOIN partido_competicion pc
						ON p.partido_id=pc.partido_id
						LEFT JOIN competiciones c
						ON pc.competicion_id=c.competicion_id
						WHERE p.equipo_id_local=%s
						OR p.equipo_id_visitante=%s
						ORDER BY p.fecha DESC
						LIMIT 1""",
						(equipo_id, equipo_id, equipo_id, equipo_id, equipo_id, r'%Local%', equipo_id, r'%Visitante%', equipo_id,
						r'%Visitante%', equipo_id, r'%Local%', equipo_id, r'%Empate%', equipo_id, equipo_id))

		partido=self.c.fetchone()

		return None if not partido else (partido["partido_id"],
										partido["equipo"],
										partido["escudo"],
										partido["marcador"],
										partido["fecha"].strftime("%d/%m/%Y"),
										partido["resultado"],
										partido["logo"])

	# Metodo para obtener los datos de los estadios
	def obtenerDatosEstadios(self)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.estadio_id, e.nombre,
						       CASE WHEN e.codigo_estadio IS NULL
						            THEN -1
						            ELSE e.codigo_estadio
						       END as estadio,
						       MAX(CASE WHEN eq.escudo IS NULL
						                THEN -1
						                ELSE eq.escudo
						           END) as escudo_equipo,
						       MAX(CASE WHEN e.codigo_pais IS NULL
						                THEN 
						                	CASE WHEN eq.codigo_pais IS NULL
						                		THEN '-1'
						                		ELSE eq.codigo_pais
						           			END
						                ELSE e.codigo_pais
						           END) as pais
						FROM estadios e
						LEFT JOIN equipo_estadio ee
						ON e.estadio_id=ee.estadio_id
						LEFT JOIN equipos eq
						ON ee.equipo_id=eq.equipo_id
						WHERE e.capacidad IS NOT NULL
						AND e.capacidad>10000
						GROUP BY e.estadio_id, e.nombre, e.codigo_estadio
						ORDER BY e.estadio_id""")

		estadios=self.c.fetchall()

		return list(map(lambda estadio: (estadio["estadio_id"],
										estadio["nombre"],
										estadio["estadio"],
										estadio["escudo_equipo"],
										estadio["pais"]), estadios))

	# Metodo para obtener los datos de los equipos mas top
	def obtenerDatosEquiposTop(self, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.equipo_id, e.nombre, e.puntuacion,
								CASE WHEN e.escudo IS NULL
										THEN -1
										ELSE e.escudo
								END as escudo,
								CASE WHEN e.codigo_pais IS NULL
										THEN '-1'
										ELSE e.codigo_pais
								END as equipo_pais,
								c.codigo_logo
						FROM equipos e
						LEFT JOIN competiciones c
						ON e.codigo_competicion=c.competicion_id
						WHERE e.puntuacion IS NOT NULL
						ORDER BY e.puntuacion DESC, e.equipo_id
						LIMIT %s""",
						(numero,))

		equipos=self.c.fetchall()

		return list(map(lambda equipo: (equipo["equipo_id"],
										equipo["nombre"],
										equipo["puntuacion"],
										equipo["escudo"],
										equipo["equipo_pais"],
										equipo["codigo_logo"]), equipos))

	# Metodo para obtener los datos de los jugadores mas top
	def obtenerDatosJugadoresTop(self, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT j.jugador_id, j.nombre, j.puntuacion,
								CASE WHEN j.codigo_pais IS NULL
										THEN '-1'
										ELSE j.codigo_pais
								END as pais,
								CASE WHEN j.codigo_jugador IS NULL
										THEN '-1'
										ELSE j.codigo_jugador
								END as jugador,
								CASE WHEN e.escudo IS NULL
										THEN -1
										ELSE e.escudo
								END as escudo_equipo
						FROM jugadores j
						LEFT JOIN equipos e
						ON j.equipo_id=e.equipo_id
						WHERE j.puntuacion IS NOT NULL
						AND j.equipo_id IS NOT NULL
						ORDER BY j.puntuacion DESC, j.jugador_id
						LIMIT %s""",
						(numero,))

		jugadores=self.c.fetchall()

		return list(map(lambda jugador: (jugador["jugador_id"],
										jugador["nombre"],
										jugador["puntuacion"],
										jugador["pais"],
										jugador["jugador"],
										jugador["escudo_equipo"]), jugadores))

	# Metodo para obtener los datos de los estadios mas top
	def obtenerDatosEstadiosTop(self, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.estadio_id, e.nombre, e.capacidad,
						       CASE WHEN e.codigo_estadio IS NULL
						            THEN -1
						            ELSE e.codigo_estadio
						       END as estadio,
						       MAX(CASE WHEN eq.escudo IS NULL
						                THEN -1
						                ELSE eq.escudo
						           END) as escudo_equipo,
						       MAX(CASE WHEN e.codigo_pais IS NULL
						                THEN 
						                	CASE WHEN eq.codigo_pais IS NULL
						                		THEN '-1'
						                		ELSE eq.codigo_pais
						           			END
						                ELSE e.codigo_pais
						           END) as pais
						FROM estadios e
						LEFT JOIN equipo_estadio ee
						ON e.estadio_id=ee.estadio_id
						LEFT JOIN equipos eq
						ON ee.equipo_id=eq.equipo_id
						WHERE e.capacidad IS NOT NULL
						AND e.capacidad<=200000
						GROUP BY e.estadio_id, e.nombre, e.codigo_estadio
						ORDER BY e.capacidad DESC, e.estadio_id
						LIMIT %s""",
						(numero,))

		estadios=self.c.fetchall()

		return list(map(lambda estadio: (estadio["estadio_id"],
										estadio["nombre"],
										estadio["capacidad"],
										estadio["estadio"],
										estadio["escudo_equipo"],
										estadio["pais"]), estadios))

	# Metodo para obtener los datos de las competiciones mas top
	def obtenerDatosCompeticionesTop(self, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT c.competicion_id, c.nombre,
								CASE WHEN c.codigo_logo IS NULL
										THEN '-1'
										ELSE c.codigo_logo
								END as logo,
								CASE WHEN c.codigo_pais IS NULL
										THEN '-1'
										ELSE c.codigo_pais
								END as pais,
								COALESCE(SUM(e.puntuacion), 0) as suma_puntuacion,
								COALESCE(COUNT(e.codigo_competicion), 0) as numero_equipos
						FROM competiciones c
						LEFT JOIN equipos e
						ON c.competicion_id=e.codigo_competicion
						WHERE e.puntuacion IS NOT NULL
						GROUP BY c.competicion_id, c.nombre, logo, pais
						HAVING COUNT(e.codigo_competicion)<=20
						ORDER BY suma_puntuacion DESC, c.competicion_id
						LIMIT %s""",
						(numero,))

		competiciones=self.c.fetchall()

		return list(map(lambda competicion: (competicion["competicion_id"],
											competicion["nombre"],
											competicion["logo"],
											competicion["pais"],
											competicion["suma_puntuacion"],
											competicion["numero_equipos"]), competiciones))

	# Metodo para obtener los jugadores de un equipo
	def obtenerJugadoresEquipo(self, equipo_id:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT jugador_id, nombre,
								CASE WHEN codigo_jugador IS NULL
										THEN '-1'
										ELSE codigo_jugador
								END as jugador
						FROM jugadores
						WHERE equipo_id=%s
						ORDER BY puntuacion DESC""",
						(equipo_id,))

		jugadores=self.c.fetchall()

		return list(map(lambda jugador: (jugador["jugador_id"],
										jugador["nombre"],
										jugador["jugador"]), jugadores))

	# Metodo para obtener los partidos entre equipos
	def obtenerPartidosEntreEquipos(self, equipo_id_1:str, equipo_id_2:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT p.partido_id, p.marcador, p.fecha,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								p.competicion
						FROM partidos p
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						WHERE (p.equipo_id_local=%s AND p.equipo_id_visitante=%s)
						OR (p.equipo_id_visitante=%s AND p.equipo_id_local=%s)
						ORDER BY p.fecha DESC
						LIMIT %s""",
						(equipo_id_1, equipo_id_2, equipo_id_1, equipo_id_2, numero))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["marcador"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["cod_local"],
											partido["local"],
											partido["escudo_local"],
											partido["cod_visitante"],
											partido["visitante"],
											partido["escudo_visitante"],
											partido["competicion"]), partidos))

	# Metodo para obtener las victorias de los partidos entre equipos de un equipo
	def obtenerVictoriasEntreEquipos(self, equipo_id_1:str, equipo_id_2:str, equipo_victorias:str)->tuple:

		self.c.execute("""SELECT %s as equipo, COUNT(1) as numero
						FROM partidos
						WHERE (equipo_id_local=%s AND equipo_id_visitante=%s AND resultado LIKE %s)
						OR (equipo_id_visitante=%s AND equipo_id_local=%s AND resultado LIKE %s)""",
						(equipo_victorias,
						equipo_id_1, equipo_id_2, r'%Local%', 
						equipo_id_1, equipo_id_2, r'%Visitante%'))

		resultado=self.c.fetchone()

		return resultado["equipo"], resultado["numero"]

	# Metodo para obtener los empates de los partidos entre equipos
	def obtenerEmpatesEntreEquipos(self, equipo_id_1:str, equipo_id_2:str)->tuple:

		self.c.execute("""SELECT COUNT(1) as numero
						FROM partidos
						WHERE ((equipo_id_local=%s AND equipo_id_visitante=%s)
						OR (equipo_id_visitante=%s AND equipo_id_local=%s))
						AND resultado LIKE %s""",
						(equipo_id_1, equipo_id_2, equipo_id_1, equipo_id_2, r'%Empate%'))

		resultado=self.c.fetchone()

		return "empate", resultado["numero"]

	# Metodo para obtener el historial de los partidos entre equipos
	def obtenerPartidosHistorialEntreEquipos(self, equipo_id_1:str, equipo_id_2:str)->List[tuple]:

		victorias_1=self.obtenerVictoriasEntreEquipos(equipo_id_1, equipo_id_2, equipo_id_1)

		victorias_2=self.obtenerVictoriasEntreEquipos(equipo_id_2, equipo_id_1, equipo_id_2)

		empates=self.obtenerEmpatesEntreEquipos(equipo_id_1, equipo_id_2)

		return [victorias_1, empates, victorias_2]

	# Metodo para insertar un partido asistido
	def insertarPartidoAsistido(self, partido_id:str, usuario:str, comentario:str)->None:

		codigo_partido_asistido=f"{partido_id}-{usuario}"

		self.c.execute("""INSERT INTO partidos_asistidos
							VALUES (%s, %s, %s, %s)""",
							(codigo_partido_asistido, partido_id, usuario, comentario))

		self.confirmar()

	# Metodo para comprobar si ya existe un partido asistido de un usuario
	def existe_partido_asistido(self, partido_id:str, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM partidos_asistidos
						WHERE partido_id=%s
						AND usuario=%s""",
						(partido_id, usuario))

		return False if not self.c.fetchone() else True

	# Metodo para obtener los partidos que no ha asistido un usuario de un equipo
	def obtenerPartidosNoAsistidosUsuario(self, usuario:str, equipo_id:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT p.partido_id, e1.nombre as local, e2.nombre as visitante, p.fecha, p.competicion
							FROM partidos p
							LEFT JOIN equipos e1
							ON p.equipo_id_local=e1.equipo_id
							LEFT JOIN equipos e2
							ON p.equipo_id_visitante=e2.equipo_id
							LEFT JOIN (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
							ON p.partido_id=pa.partido_id
							WHERE pa.partido_id IS NULL
							AND (p.equipo_id_local=%s
							OR p.equipo_id_visitante=%s)
							ORDER BY p.fecha DESC""",
							(usuario, equipo_id, equipo_id))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["local"],
											partido["visitante"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["competicion"]), partidos))

	# Metodo para obtener la fecha del ultimo partido asistido
	def ultima_fecha_partido_asistido(self, usuario:str)->Optional[str]:

	    self.c.execute("""SELECT MAX(p.fecha) as fecha_reciente
	                      FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
	                      JOIN partidos p
	                      ON pa.partido_id=p.partido_id""",
	                      (usuario,))

	    fecha_reciente=self.c.fetchone()

	    if not fecha_reciente:

	    	return None

	    return None if not fecha_reciente["fecha_reciente"] else fecha_reciente["fecha_reciente"].strftime("%Y-%m-%d")

	# Metodo para obtener los partidos que no ha asistido un usuario de un equipo recientes
	def obtenerPartidosNoAsistidosUsuarioRecientes(self, usuario:str, equipo_id:str)->List[Optional[tuple]]:

		fecha_mas_reciente=self.ultima_fecha_partido_asistido(usuario)

		if not fecha_mas_reciente:

			return self.obtenerPartidosNoAsistidosUsuario(usuario, equipo_id)

		self.c.execute("""SELECT p.partido_id, e1.nombre as local, e2.nombre as visitante, p.fecha, p.competicion
							FROM partidos p
							LEFT JOIN equipos e1
							ON p.equipo_id_local=e1.equipo_id
							LEFT JOIN equipos e2
							ON p.equipo_id_visitante=e2.equipo_id
							LEFT JOIN (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
							ON p.partido_id=pa.partido_id
							WHERE pa.partido_id IS NULL
							AND (p.equipo_id_local=%s
							OR p.equipo_id_visitante=%s)
							AND p.fecha>%s
							ORDER BY p.fecha DESC""",
							(usuario, equipo_id, equipo_id, fecha_mas_reciente))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["local"],
											partido["visitante"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["competicion"]), partidos))

	# Metodo para obtener los partidos asistidos de un usuario (en relacion a su equipo)
	def obtenerPartidosAsistidosUsuario(self, usuario:str)->List[Optional[tuple]]:

		equipo_id=self.obtenerEquipo(usuario)

		self.c.execute("""SELECT pa.partido_id, p.marcador, p.fecha, p.competicion,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								e1.equipo_id as local, e1.nombre as nombre_local,
								e2.equipo_id as visitante, e2.nombre as nombre_visitante,
								pe.estadio_id,
								CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_ganado,
						       CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_perdido,
   						       CASE WHEN p.resultado LIKE %s
							            THEN 1
							            ELSE 0
						       END as partido_empatado
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN equipos e1
							ON p.equipo_id_local=e1.equipo_id
							LEFT JOIN equipos e2
							ON p.equipo_id_visitante=e2.equipo_id
							LEFT JOIN partido_estadio pe
							ON p.partido_id=pe.partido_id
							ORDER BY p.fecha DESC""",
							(r'%Local%', equipo_id, r'%Visitante%', equipo_id, 
								r'%Visitante%', equipo_id, r'%Local%', equipo_id, 
								r'%Empate%', usuario))

		asistidos=self.c.fetchall()

		return list(map(lambda asistido: (asistido["partido_id"],
											asistido["marcador"],
											asistido["fecha"].strftime("%d/%m/%Y"),
											asistido["competicion"],
											asistido["escudo_local"],
											asistido["escudo_visitante"],
											asistido["nombre_local"],
											asistido["nombre_visitante"],
											asistido["local"],
											asistido["visitante"],
											asistido["estadio_id"],
											asistido["partido_ganado"],
											asistido["partido_perdido"],
											asistido["partido_empatado"]), asistidos))

	# Metodo para obtener los partidos asistidos de un usuario (en relacion a su equipo) de local
	def obtenerPartidosAsistidosUsuarioEquipoLocal(self, usuario:str)->List[tuple]:

		partidos_asistidos=self.obtenerPartidosAsistidosUsuario(usuario)

		equipo_id=self.obtenerEquipo(usuario)

		return list(filter(lambda partido_asistido: partido_asistido[8]==equipo_id, partidos_asistidos))

	# Metodo para obtener los partidos asistidos de un usuario (en relacion a su equipo) de visitante
	def obtenerPartidosAsistidosUsuarioEquipoVisitante(self, usuario:str)->List[tuple]:

		partidos_asistidos=self.obtenerPartidosAsistidosUsuario(usuario)

		equipo_id=self.obtenerEquipo(usuario)

		return list(filter(lambda partido_asistido: partido_asistido[9]==equipo_id, partidos_asistidos))

	# Metodo para obtener los partidos asistidos de un usuario en casa
	def obtenerPartidosAsistidosUsuarioCasa(self, usuario:str)->List[tuple]:

		equipo_id=self.obtenerEquipo(usuario)

		estadio=self.estadio_equipo(equipo_id)

		if not estadio:

			return self.obtenerPartidosAsistidosUsuarioEquipoLocal(usuario)

		partidos_asistidos=self.obtenerPartidosAsistidosUsuario(usuario)

		def filtrarPartidoAsistidoCasa(partido_asistido:List[str], estadio:str, equipo_id:str)->bool:

			if partido_asistido[10]==estadio:

				return True

			return True if not partido_asistido[10] and partido_asistido[8]==equipo_id else False

		return list(filter(lambda partido_asistido: filtrarPartidoAsistidoCasa(partido_asistido, estadio, equipo_id), partidos_asistidos))

	# Metodo para obtener los partidos asistidos de un usuario fuera de casa
	def obtenerPartidosAsistidosUsuarioFuera(self, usuario:str)->List[tuple]:

		equipo_id=self.obtenerEquipo(usuario)

		estadio=self.estadio_equipo(equipo_id)

		if not estadio:

			return self.obtenerPartidosAsistidosUsuarioEquipoVisitante(usuario)

		partidos_asistidos=self.obtenerPartidosAsistidosUsuario(usuario)

		def filtrarPartidoAsistidoFuera(partido_asistido:List[str], estadio:str, equipo_id:str)->bool:

			if partido_asistido[10]!=estadio and partido_asistido[10]:

				return True

			return True if not partido_asistido[10] and partido_asistido[9]==equipo_id else False

		return list(filter(lambda partido_asistido: filtrarPartidoAsistidoFuera(partido_asistido, estadio, equipo_id), partidos_asistidos))

	# Metodo para obtener los estadios de los partidos asistidos de un usuario por fecha
	def obtenerEstadiosPartidosAsistidosUsuarioFecha(self, usuario:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.estadio_id, e.nombre,
						       CASE WHEN e.codigo_estadio IS NULL
						            THEN -1
						            ELSE e.codigo_estadio
						       END as estadio,
						       MAX(CASE WHEN eq.escudo IS NULL
						                THEN -1
						                ELSE eq.escudo
						           END) as escudo_equipo,
						       MAX(CASE WHEN e.codigo_pais IS NULL
						                THEN 
						                	CASE WHEN eq.codigo_pais IS NULL
						                		THEN '-1'
						                		ELSE eq.codigo_pais
						           			END
						                ELSE e.codigo_pais
						           END) as pais,
						       MAX(p.fecha) as ultima_fecha
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_estadio pe
		                    ON p.partido_id=pe.partido_id
		                    LEFT JOIN estadios e
		                    ON pe.estadio_id=e.estadio_id
		                    LEFT JOIN equipo_estadio ee
							ON e.estadio_id=ee.estadio_id
							LEFT JOIN equipos eq
							ON ee.equipo_id=eq.equipo_id
							WHERE e.capacidad IS NOT NULL
							GROUP BY e.estadio_id, e.nombre, e.codigo_estadio
							ORDER BY ultima_fecha DESC
							LIMIT %s""",
							(usuario, numero))

		estadios_asistidos=self.c.fetchall()

		return list(map(lambda estadio: (estadio["estadio_id"],
										estadio["nombre"],
										estadio["estadio"],
										estadio["escudo_equipo"],
										estadio["pais"],
										estadio["ultima_fecha"].strftime("%d/%m/%Y")), estadios_asistidos))

	# Metodo para obtener los estadios de los partidos asistidos de un usuario por cantidad de veces visitado
	def obtenerEstadiosPartidosAsistidosUsuarioCantidad(self, usuario:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.estadio_id, e.nombre,
						       CASE WHEN e.codigo_estadio IS NULL
						            THEN -1
						            ELSE e.codigo_estadio
						       END as estadio,
						       MAX(CASE WHEN eq.escudo IS NULL
						                THEN -1
						                ELSE eq.escudo
						           END) as escudo_equipo,
						       MAX(CASE WHEN e.codigo_pais IS NULL
						                THEN 
						                	CASE WHEN eq.codigo_pais IS NULL
						                		THEN '-1'
						                		ELSE eq.codigo_pais
						           			END
						                ELSE e.codigo_pais
						           END) as pais,
						       COUNT(DISTINCT p.partido_id) as numero_veces
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_estadio pe
		                    ON p.partido_id=pe.partido_id
		                    LEFT JOIN estadios e
		                    ON pe.estadio_id=e.estadio_id
		                    LEFT JOIN equipo_estadio ee
							ON e.estadio_id=ee.estadio_id
							LEFT JOIN equipos eq
							ON ee.equipo_id=eq.equipo_id
							WHERE e.capacidad IS NOT NULL
							GROUP BY e.estadio_id, e.nombre, e.codigo_estadio
							ORDER BY numero_veces DESC
							LIMIT %s""",
							(usuario, numero))

		estadios_asistidos=self.c.fetchall()

		return list(map(lambda estadio: (estadio["estadio_id"],
										estadio["nombre"],
										estadio["estadio"],
										estadio["escudo_equipo"],
										estadio["pais"],
										estadio["numero_veces"]), estadios_asistidos))

	# Metodo para obtener los estadios de los partidos asistidos filtrados de un usuario por cantidad de veces visitado
	def obtenerEstadiosPartidosAsistidosUsuarioCantidadFiltrado(self, usuario:str, partidos_ids:tuple, numero:int)->List[Optional[tuple]]:

		numero_place_holders=", ".join(["%s"]*len(partidos_ids))

		self.c.execute(f"""SELECT e.estadio_id, e.nombre,
						       CASE WHEN e.codigo_estadio IS NULL
						            THEN -1
						            ELSE e.codigo_estadio
						       END as estadio,
						       MAX(CASE WHEN eq.escudo IS NULL
						                THEN -1
						                ELSE eq.escudo
						           END) as escudo_equipo,
						       MAX(CASE WHEN e.codigo_pais IS NULL
						                THEN 
						                	CASE WHEN eq.codigo_pais IS NULL
						                		THEN '-1'
						                		ELSE eq.codigo_pais
						           			END
						                ELSE e.codigo_pais
						           END) as pais,
						       COUNT(DISTINCT p.partido_id) as numero_veces
							FROM (SELECT *
									FROM partidos_asistidos
									WHERE usuario=%s
									AND partido_id IN ({numero_place_holders})) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_estadio pe
		                    ON p.partido_id=pe.partido_id
		                    LEFT JOIN estadios e
		                    ON pe.estadio_id=e.estadio_id
		                    LEFT JOIN equipo_estadio ee
							ON e.estadio_id=ee.estadio_id
							LEFT JOIN equipos eq
							ON ee.equipo_id=eq.equipo_id
							WHERE e.capacidad IS NOT NULL
							GROUP BY e.estadio_id, e.nombre, e.codigo_estadio
							ORDER BY numero_veces DESC
							LIMIT %s""",
							(usuario, *partidos_ids, numero))

		estadios_asistidos=self.c.fetchall()

		return list(map(lambda estadio: (estadio["estadio_id"],
										estadio["nombre"],
										estadio["estadio"],
										estadio["escudo_equipo"],
										estadio["pais"],
										estadio["numero_veces"]), estadios_asistidos))

	# Metodo para saber si un usuario a asistido a un estadio o no
	def estadio_asistido_usuario(self, usuario:str, estadio_id:str)->bool:

		self.c.execute("""SELECT *
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_estadio pe
		                    ON p.partido_id=pe.partido_id
		                    LEFT JOIN estadios e
		                    ON pe.estadio_id=e.estadio_id
							WHERE e.estadio_id=%s""",
							(usuario, estadio_id))

		return False if not self.c.fetchone() else True

	# Metodo para obtener un partido asistido de un usuario
	def obtenerPartidoAsistidoUsuario(self, usuario:str, partido_id:str)->Optional[tuple]:

		self.c.execute("""SELECT pa.asistido_id, pa.partido_id, p.marcador,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								pa.comentario,
								CASE WHEN pa.imagen IS NULL
										THEN '-1'
										ELSE pa.imagen
								END as imagen_partido,
								pa.on_tour,
								TO_CHAR(pa.fecha_ida, 'DD-MM-YYYY') AS fecha_ida_str,
								TO_CHAR(pa.fecha_vuelta, 'DD-MM-YYYY') AS fecha_vuelta_str,
								pa.teletrabajo
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN equipos e1
							ON p.equipo_id_local=e1.equipo_id
							LEFT JOIN equipos e2
							ON p.equipo_id_visitante=e2.equipo_id
							WHERE pa.partido_id=%s""",
							(usuario, partido_id))

		asistido=self.c.fetchone()

		return None if not asistido else (asistido["asistido_id"],
											asistido["partido_id"],
											asistido["marcador"],
											asistido["cod_local"],
											asistido["local"],
											asistido["escudo_local"],
											asistido["cod_visitante"],
											asistido["visitante"],
											asistido["escudo_visitante"],
											asistido["comentario"],
											asistido["imagen_partido"],
											asistido["on_tour"],
											asistido["fecha_ida_str"],
											asistido["fecha_vuelta_str"],
											asistido["teletrabajo"])

	# Metodo para obtener el partido siguiente de un partido asistido de un usuario
	def obtenerPartidoAsistidoUsuarioSiguiente(self, usuario:str, partido_id:str)->Optional[str]:

		self.c.execute("""SELECT p2.partido_id
						FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa2
						LEFT JOIN partidos p2
	                    ON pa2.partido_id=p2.partido_id
						WHERE p2.fecha>(SELECT p.fecha
						    		FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
				                    LEFT JOIN partidos p
				                    ON pa.partido_id=p.partido_id
						    		WHERE p.partido_id=%s)
						ORDER BY p2.fecha ASC
						LIMIT 1""",
						(usuario, usuario, partido_id))

		partido_asistido=self.c.fetchone()

		return None if not partido_asistido else partido_asistido["partido_id"]

	# Metodo para obtener el partido anterior de un partido asistido de un usuario
	def obtenerPartidoAsistidoUsuarioAnterior(self, usuario:str, partido_id:str)->Optional[str]:

		self.c.execute("""SELECT p2.partido_id
						FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa2
						LEFT JOIN partidos p2
	                    ON pa2.partido_id=p2.partido_id
						WHERE p2.fecha<(SELECT p.fecha
						    		FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
				                    LEFT JOIN partidos p
				                    ON pa.partido_id=p.partido_id
						    		WHERE p.partido_id=%s)
						ORDER BY p2.fecha DESC
						LIMIT 1""",
						(usuario, usuario, partido_id))

		partido_asistido=self.c.fetchone()

		return None if not partido_asistido else partido_asistido["partido_id"]

	# Metodo para actualizar el comentario de un partido asistido
	def actualizarComentarioPartidoAsistido(self, partido_id:str, usuario:str, comentario_nuevo:str)->None:

		self.c.execute("""UPDATE partidos_asistidos
							SET Comentario=%s
							WHERE Partido_Id=%s
							AND Usuario=%s""",
							(comentario_nuevo, partido_id, usuario))

		self.confirmar()

	# Metodo para obtener los equipos de los partidos asistidos de un usuario por cantidad de veces enfrentado
	def obtenerEquiposPartidosAsistidosUsuarioCantidad(self, usuario:str, numero:int)->List[Optional[tuple]]:

		equipo_id=self.obtenerEquipo(usuario)

		self.c.execute("""SELECT equipo, nombre_equipo, escudo, pais, COUNT(equipo) as numero_veces
							FROM (SELECT p.equipo_id_local as equipo, e1.nombre as nombre_equipo,
									CASE WHEN e1.escudo IS NULL
											THEN -1
											ELSE e1.escudo
									END as escudo,
									CASE WHEN e1.codigo_pais IS NULL
										THEN '-1'
										ELSE e1.codigo_pais
									END as pais
									FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
				                    LEFT JOIN partidos p
				                    ON pa.partido_id=p.partido_id
				                    LEFT JOIN equipos e1
									ON p.equipo_id_local=e1.equipo_id
									LEFT JOIN equipos e2
									ON p.equipo_id_visitante=e2.equipo_id
									UNION ALL
									SELECT p.equipo_id_visitante as equipo, e2.nombre as nombre_equipo,
									CASE WHEN e2.escudo IS NULL
											THEN -1
											ELSE e2.escudo
									END as escudo,
									CASE WHEN e2.codigo_pais IS NULL
										THEN '-1'
										ELSE e2.codigo_pais
									END as pais
									FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
				                    LEFT JOIN partidos p
				                    ON pa.partido_id=p.partido_id
				                    LEFT JOIN equipos e1
									ON p.equipo_id_local=e1.equipo_id
									LEFT JOIN equipos e2
									ON p.equipo_id_visitante=e2.equipo_id) as t
							GROUP BY equipo, nombre_equipo, escudo, pais
							HAVING equipo!=%s
							ORDER BY numero_veces DESC
							LIMIT %s""",
							(usuario, usuario, equipo_id, numero))

		equipos_enfrentados=self.c.fetchall()

		return list(map(lambda equipo: (equipo["equipo"],
										equipo["nombre_equipo"],
										equipo["escudo"],
										equipo["pais"],
										equipo["numero_veces"]), equipos_enfrentados))

	# Metodo para obtener los equipos de los partidos asistidos filtrados de un usuario por cantidad de veces enfrentado
	def obtenerEquiposPartidosAsistidosUsuarioCantidadFiltrado(self, usuario:str, partidos_ids:tuple, numero:int)->List[Optional[tuple]]:

		numero_place_holders=", ".join(["%s"]*len(partidos_ids))

		equipo_id=self.obtenerEquipo(usuario)

		self.c.execute(f"""SELECT equipo, nombre_equipo, escudo, pais, COUNT(equipo) as numero_veces
							FROM (SELECT p.equipo_id_local as equipo, e1.nombre as nombre_equipo,
									CASE WHEN e1.escudo IS NULL
											THEN -1
											ELSE e1.escudo
									END as escudo,
									CASE WHEN e1.codigo_pais IS NULL
										THEN '-1'
										ELSE e1.codigo_pais
									END as pais
									FROM (SELECT *
											FROM partidos_asistidos
											WHERE usuario=%s
											AND partido_id IN ({numero_place_holders})) pa
				                    LEFT JOIN partidos p
				                    ON pa.partido_id=p.partido_id
				                    LEFT JOIN equipos e1
									ON p.equipo_id_local=e1.equipo_id
									LEFT JOIN equipos e2
									ON p.equipo_id_visitante=e2.equipo_id
									UNION ALL
									SELECT p.equipo_id_visitante as equipo, e2.nombre as nombre_equipo,
									CASE WHEN e2.escudo IS NULL
											THEN -1
											ELSE e2.escudo
									END as escudo,
									CASE WHEN e2.codigo_pais IS NULL
										THEN '-1'
										ELSE e2.codigo_pais
									END as pais
									FROM (SELECT *
											FROM partidos_asistidos
											WHERE usuario=%s
											AND partido_id IN ({numero_place_holders})) pa
				                    LEFT JOIN partidos p
				                    ON pa.partido_id=p.partido_id
				                    LEFT JOIN equipos e1
									ON p.equipo_id_local=e1.equipo_id
									LEFT JOIN equipos e2
									ON p.equipo_id_visitante=e2.equipo_id) as t
							GROUP BY equipo, nombre_equipo, escudo, pais
							HAVING equipo!=%s
							ORDER BY numero_veces DESC
							LIMIT %s""",
							(usuario, *partidos_ids, usuario, *partidos_ids, equipo_id, numero))

		equipos_enfrentados=self.c.fetchall()

		return list(map(lambda equipo: (equipo["equipo"],
										equipo["nombre_equipo"],
										equipo["escudo"],
										equipo["pais"],
										equipo["numero_veces"]), equipos_enfrentados))

	# Metodo para insertar un partido asistido favorito
	def insertarPartidoAsistidoFavorito(self, partido_id:str, usuario:str)->None:

		self.c.execute("""INSERT INTO partido_asistido_favorito
							VALUES (%s, %s)""",
							(partido_id, usuario))

		self.confirmar()

	# Metodo para comprobar si ya existe un partido asistido favorito de un usuario
	def existe_partido_asistido_favorito(self, partido_id:str, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM partido_asistido_favorito
						WHERE partido_id=%s
						AND usuario=%s""",
						(partido_id, usuario))

		return False if not self.c.fetchone() else True

	# Metodo para obtener el partido asistido favorito del usuario
	def obtenerPartidoAsistidoFavorito(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT partido_id
						FROM partido_asistido_favorito
						WHERE usuario=%s""",
						(usuario,))

		partido_asistido_favorito=self.c.fetchone()

		return None if not partido_asistido_favorito else partido_asistido_favorito["partido_id"]

	# Metodo para eliminar un partido asistido favorito
	def eliminarPartidoAsistidoFavorito(self, partido_id:str, usuario:str)->None:

		self.c.execute("""DELETE FROM partido_asistido_favorito
							WHERE Partido_Id=%s
							AND Usuario=%s""",
							(partido_id, usuario))

		self.confirmar()

	# Metodo para eliminar un partido asistido
	def eliminarPartidoAsistido(self, partido_id:str, usuario:str)->None:

		self.c.execute("""DELETE FROM partidos_asistidos
							WHERE Partido_Id=%s
							AND Usuario=%s""",
							(partido_id, usuario))

		self.confirmar()

	# Metodo para obtener los paises estadios de los partidos asistidos de un usuario por cantidad de veces visitado
	def obtenerPaisesEstadiosPartidosAsistidosUsuarioCantidad(self, usuario:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.codigo_pais, e.pais, COUNT(DISTINCT p.partido_id) as numero_veces
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_estadio pe
		                    ON p.partido_id=pe.partido_id
		                    LEFT JOIN estadios e
		                    ON pe.estadio_id=e.estadio_id
							WHERE e.capacidad IS NOT NULL
							AND e.codigo_pais IS NOT NULL
							GROUP BY e.codigo_pais, e.pais
							ORDER BY numero_veces DESC
							LIMIT %s""",
							(usuario, numero))

		paises_asistidos=self.c.fetchall()

		return list(map(lambda pais: (pais["codigo_pais"],
										pais["pais"],
										pais["numero_veces"]), paises_asistidos))

	# Metodo para obtener los estadios de los partidos asistidos de un usuario y un pais por cantidad de veces visitado
	def obtenerEstadiosPaisPartidosAsistidosUsuarioCantidad(self, usuario:str, codigo_pais:str, numero:int)->List[Optional[tuple]]:

		estadios_asistidos=self.obtenerEstadiosPartidosAsistidosUsuarioCantidad(usuario, numero)

		return list(filter(lambda estadio: estadio[4]==codigo_pais, estadios_asistidos))

	# Metodo para obtener las competiciones de los partidos asistidos de un usuario por cantidad de veces asistidas
	def obtenerCompeticionesPartidosAsistidosUsuarioCantidad(self, usuario:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT c.competicion_id, c.nombre,
						       CASE WHEN c.codigo_logo IS NULL
						            THEN '-1'
						            ELSE c.codigo_logo
						       END as logo_competicion,
						       CASE WHEN c.codigo_pais IS NULL
						                THEN '-1'
						                ELSE c.codigo_pais
					           END as pais,
						       COUNT(DISTINCT p.partido_id) as numero_veces
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_competicion pc
		                    ON p.partido_id=pc.partido_id
		                    LEFT JOIN competiciones c
		                    ON pc.competicion_id=c.competicion_id
		                    WHERE c.competicion_id IS NOT NULL
							GROUP BY c.competicion_id, c.nombre, c.codigo_logo, c.codigo_pais
							ORDER BY numero_veces DESC
							LIMIT %s""",
							(usuario, numero))

		competiciones_asistidas=self.c.fetchall()

		return list(map(lambda competicion: (competicion["competicion_id"],
											competicion["nombre"],
											competicion["logo_competicion"],
											competicion["pais"],
											competicion["numero_veces"]), competiciones_asistidas))

	# Metodo para obtener las competiciones de los partidos asistidos filtrados de un usuario por cantidad de veces asistidas
	def obtenerCompeticionesPartidosAsistidosUsuarioCantidadFiltrado(self, usuario:str, partidos_ids:tuple, numero:int)->List[Optional[tuple]]:

		numero_place_holders=", ".join(["%s"]*len(partidos_ids))

		self.c.execute(f"""SELECT c.competicion_id, c.nombre,
						       CASE WHEN c.codigo_logo IS NULL
						            THEN '-1'
						            ELSE c.codigo_logo
						       END as logo_competicion,
						       CASE WHEN c.codigo_pais IS NULL
						                THEN '-1'
						                ELSE c.codigo_pais
					           END as pais,
						       COUNT(DISTINCT p.partido_id) as numero_veces
							FROM (SELECT *
									FROM partidos_asistidos
									WHERE usuario=%s
									AND partido_id IN ({numero_place_holders})) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_competicion pc
		                    ON p.partido_id=pc.partido_id
		                    LEFT JOIN competiciones c
		                    ON pc.competicion_id=c.competicion_id
		                    WHERE c.competicion_id IS NOT NULL
							GROUP BY c.competicion_id, c.nombre, c.codigo_logo, c.codigo_pais
							ORDER BY numero_veces DESC
							LIMIT %s""",
							(usuario, *partidos_ids, numero))

		competiciones_asistidas=self.c.fetchall()

		return list(map(lambda competicion: (competicion["competicion_id"],
											competicion["nombre"],
											competicion["logo_competicion"],
											competicion["pais"],
											competicion["numero_veces"]), competiciones_asistidas))

	# Metodo para obtener las coordenadas de los estadios de los partidos asistidos de un usuario
	def obtenerCoordenadasEstadiosPartidosAsistidosUsuario(self, usuario:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT DISTINCT e.latitud, e.longitud
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_estadio pe
		                    ON p.partido_id=pe.partido_id
		                    LEFT JOIN estadios e
		                    ON pe.estadio_id=e.estadio_id
							WHERE e.latitud IS NOT NULL
							AND e.longitud IS NOT NULL
							LIMIT %s""",
							(usuario, numero))

		coordenadas_estadios_asistidos=self.c.fetchall()

		return list(map(lambda coordenada: (coordenada["latitud"],
											coordenada["longitud"]), coordenadas_estadios_asistidos))

	# Metodo para obtener los datos y las coordenadas de los estadios de los partidos asistidos de un usuario
	def obtenerDatosCoordenadasEstadiosPartidosAsistidosUsuario(self, usuario:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT DISTINCT e.nombre, e.latitud, e.longitud,
								CASE WHEN e.codigo_estadio IS NULL
										THEN -1
										ELSE e.codigo_estadio
								END as imagen_estadio,
								(CASE WHEN e.codigo_pais IS NULL
					                THEN 
					                	CASE WHEN eq.codigo_pais IS NULL
					                		THEN '-1'
					                		ELSE eq.codigo_pais
					           			END
					                ELSE e.codigo_pais
					           	END) as pais
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_estadio pe
		                    ON p.partido_id=pe.partido_id
		                    LEFT JOIN estadios e
		                    ON pe.estadio_id=e.estadio_id
    	                    LEFT JOIN equipo_estadio ee
							ON e.estadio_id=ee.estadio_id
    						LEFT JOIN equipos eq
							ON ee.equipo_id=eq.equipo_id
							WHERE e.latitud IS NOT NULL
							AND e.longitud IS NOT NULL
							LIMIT %s""",
							(usuario, numero))

		datos_estadios_asistidos=self.c.fetchall()

		return list(map(lambda datos_estadio: (datos_estadio["nombre"],
												datos_estadio["latitud"],
												datos_estadio["longitud"],
												datos_estadio["imagen_estadio"],
												datos_estadio["pais"]), datos_estadios_asistidos))

	# Metodo para obtener los datos y las coordenadas de los estadios de los partidos asistidos de un usuario y un pais
	def obtenerDatosCoordenadasEstadiosPaisPartidosAsistidosUsuario(self, usuario:str, codigo_pais:str, numero:int)->List[Optional[tuple]]:

		datos_estadios_asistidos=self.obtenerDatosCoordenadasEstadiosPartidosAsistidosUsuario(usuario, numero)

		return list(filter(lambda dato_estadio: dato_estadio[4]==codigo_pais, datos_estadios_asistidos))

	# Metodo para obtener el numero de veces visitado a un estadio de los partidos asistidos
	def obtenerNumeroVecesEstadioPartidosAsistidosUsuario(self, usuario:str, estadio_id:str)->int:

		estadios=self.obtenerDatosEstadios()

		estadios_asistidos=self.obtenerEstadiosPartidosAsistidosUsuarioCantidad(usuario, len(estadios))

		estadio_veces=list(filter(lambda estadio: estadio[0]==estadio_id, estadios_asistidos))

		return 0 if not estadio_veces else estadio_veces[0][5]

	# Metodo para obtener los proximos partidos de un equipo
	def obtenerProximosPartidosEquipo(self, equipo_id:str, numero:int)->List[tuple]:

		self.c.execute("""SELECT pp.partido_id, pp.fecha, pp.hora,
								pp.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								pp.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								pp.competicion
						FROM proximos_partidos pp
						LEFT JOIN equipos e1
						ON pp.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON pp.equipo_id_visitante=e2.equipo_id
						WHERE pp.equipo_id_local=%s
						OR pp.equipo_id_visitante=%s
						ORDER BY fecha ASC
						LIMIT %s""",
						(equipo_id, equipo_id, numero))

		proximos_partidos=self.c.fetchall()

		return list(map(lambda proximo_partido: (proximo_partido["partido_id"],
												proximo_partido["fecha"].strftime("%d/%m/%Y"),
												proximo_partido["hora"],
												proximo_partido["cod_local"],
												proximo_partido["local"],
												proximo_partido["escudo_local"],
												proximo_partido["cod_visitante"],
												proximo_partido["visitante"],
												proximo_partido["escudo_visitante"],
												proximo_partido["competicion"]), proximos_partidos))

	# Metodo para comprobar si ya existe un entrenador
	def existe_entrenador(self, entrenador_id:str)->bool:

		self.c.execute("""SELECT *
						FROM entrenadores
						WHERE entrenador_id=%s""",
						(entrenador_id,))

		return False if not self.c.fetchone() else True

	# Metodo para obtener los datos de un entrenador
	def obtenerDatosEntrenador(self, entrenador_id:str)->Optional[tuple]:

		self.c.execute("""SELECT en.entrenador_id, en.nombre,
								CASE WHEN en.codigo_pais IS NULL
										THEN '-1'
										ELSE en.codigo_pais
								END as pais,
								CASE WHEN en.codigo_entrenador IS NULL
										THEN '-1'
										ELSE en.codigo_entrenador
								END as entrenador,
								en.puntuacion, e.equipo_id, e.nombre as nombre_equipo,
								CASE WHEN e.escudo IS NULL
										THEN -1
										ELSE e.escudo
								END as escudo_equipo,
								CASE WHEN en.equipo_id IS NULL
										THEN False
										ELSE True
								END as equipo_existe
						FROM entrenadores en
						LEFT JOIN equipos e
						ON en.equipo_id=e.equipo_id
						WHERE en.entrenador_id=%s""",
						(entrenador_id,))

		entrenador=self.c.fetchone()

		return None if not entrenador else (entrenador["entrenador_id"],
											entrenador["nombre"],
											entrenador["pais"],
											entrenador["entrenador"],
											entrenador["puntuacion"],
											entrenador["equipo_id"],
											entrenador["nombre_equipo"],
											entrenador["escudo_equipo"],
											entrenador["equipo_existe"])

	# Metodo para actualizar la imagen de un partido asistido
	def actualizarImagenPartidoAsistido(self, partido_id:str, usuario:str, imagen:str)->None:

		self.c.execute("""UPDATE partidos_asistidos
							SET Imagen=%s
							WHERE Partido_Id=%s
							AND Usuario=%s""",
							(imagen, partido_id, usuario))

		self.confirmar()

	# Metodo para obtener los equipos de un jugador
	def obtenerEquiposJugador(self, jugador_id:str)->List[tuple]:

		self.c.execute("""SELECT e.equipo_id, e.nombre,
							CASE WHEN e.escudo IS NULL
									THEN -1
									ELSE e.escudo
							END as escudo_equipo,
							je.temporadas, je.goles, je.partidos
							FROM jugadores_equipo je
							LEFT JOIN equipos e
							ON je.equipo_id=e.equipo_id
							WHERE je.jugador_id=%s
							ORDER BY je.partidos DESC""",
							(jugador_id,))

		equipos_jugador=self.c.fetchall()

		return list(map(lambda equipo: (equipo["equipo_id"],
										equipo["nombre"],
										equipo["escudo_equipo"],
										equipo["temporadas"],
										equipo["goles"],
										equipo["partidos"]), equipos_jugador))

	# Metodo para obtener la seleccion de un jugador
	def obtenerSeleccionJugador(self, jugador_id:str)->Optional[tuple]:

		self.c.execute("""SELECT CASE WHEN codigo_seleccion IS NULL
									THEN -1
									ELSE codigo_seleccion
							END as seleccion,
							convocatorias, goles, asistencias
							FROM jugadores_seleccion
							WHERE jugador_id=%s""",
							(jugador_id,))

		seleccion_jugador=self.c.fetchone()

		return None if not seleccion_jugador else (seleccion_jugador["seleccion"],
													seleccion_jugador["convocatorias"],
													seleccion_jugador["goles"],
													seleccion_jugador["asistencias"])

	# Metodo para obtener los partidos asistidos de un usuario en un estadio concreto
	def obtenerPartidosAsistidosUsuarioEstadio(self, usuario:str, equipo_id:str, estadio_id:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT p.partido_id, p.marcador, p.fecha,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								p.competicion,
								pe.estadio_id as estadio_partido,
								CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_ganado,
						       CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_perdido,
   						       CASE WHEN p.resultado LIKE %s
							            THEN 1
							            ELSE 0
						       END as partido_empatado
						FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
	                    LEFT JOIN partidos p
	                    ON pa.partido_id=p.partido_id
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						LEFT JOIN partido_estadio pe
						ON p.partido_id=pe.partido_id
						WHERE pe.estadio_id=%s
						ORDER BY p.fecha DESC""",
						(r'%Local%', equipo_id, r'%Visitante%', equipo_id, 
						r'%Visitante%', equipo_id, r'%Local%', equipo_id, 
						r'%Empate%', usuario, estadio_id))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["marcador"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["cod_local"],
											partido["local"],
											partido["escudo_local"],
											partido["cod_visitante"],
											partido["visitante"],
											partido["escudo_visitante"],
											partido["competicion"],
											partido["estadio_partido"],
											partido["partido_ganado"],
											partido["partido_perdido"],
											partido["partido_empatado"]), partidos))

	# Metodo para obtener los partidos asistidos de un usuario de un equipo concreto
	def obtenerPartidosAsistidosUsuarioEquipo(self, usuario:str, equipo_id:str, equipo_id_filtrar:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT p.partido_id, p.marcador, p.fecha,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								p.competicion,
								pe.estadio_id as estadio_partido,
								CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_ganado,
						       CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_perdido,
   						       CASE WHEN p.resultado LIKE %s
							            THEN 1
							            ELSE 0
						       END as partido_empatado
						FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
	                    LEFT JOIN partidos p
	                    ON pa.partido_id=p.partido_id
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						LEFT JOIN partido_estadio pe
						ON p.partido_id=pe.partido_id
						WHERE p.equipo_id_local=%s
						OR p.equipo_id_visitante=%s
						ORDER BY p.fecha DESC""",
						(r'%Local%', equipo_id, r'%Visitante%', equipo_id, 
						r'%Visitante%', equipo_id, r'%Local%', equipo_id, 
						r'%Empate%', usuario, equipo_id_filtrar, equipo_id_filtrar))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["marcador"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["cod_local"],
											partido["local"],
											partido["escudo_local"],
											partido["cod_visitante"],
											partido["visitante"],
											partido["escudo_visitante"],
											partido["competicion"],
											partido["estadio_partido"],
											partido["partido_ganado"],
											partido["partido_perdido"],
											partido["partido_empatado"]), partidos))

	# Metodo para obtener los partidos asistidos de un usuario de una competicion concreta
	def obtenerPartidosAsistidosUsuarioCompeticion(self, usuario:str, equipo_id:str, competicion_id:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT p.partido_id, p.marcador, p.fecha,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								p.competicion,
								pe.estadio_id as estadio_partido,
								CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_ganado,
						       CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_perdido,
   						       CASE WHEN p.resultado LIKE %s
							            THEN 1
							            ELSE 0
						       END as partido_empatado
						FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
	                    LEFT JOIN partidos p
	                    ON pa.partido_id=p.partido_id
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						LEFT JOIN partido_estadio pe
						ON p.partido_id=pe.partido_id
						LEFT JOIN partido_competicion pc
						ON p.partido_id=pc.partido_id
						WHERE pc.competicion_id=%s
						ORDER BY p.fecha DESC""",
						(r'%Local%', equipo_id, r'%Visitante%', equipo_id, 
						r'%Visitante%', equipo_id, r'%Local%', equipo_id, 
						r'%Empate%', usuario, competicion_id))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["marcador"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["cod_local"],
											partido["local"],
											partido["escudo_local"],
											partido["cod_visitante"],
											partido["visitante"],
											partido["escudo_visitante"],
											partido["competicion"],
											partido["estadio_partido"],
											partido["partido_ganado"],
											partido["partido_perdido"],
											partido["partido_empatado"]), partidos))

	# Metodo para actualizar el campo on tour de un partido asistido
	def actualizarOnTourPartidoAsistido(self, partido_id:str, usuario:str, on_tour:bool)->None:

		self.c.execute("""UPDATE partidos_asistidos
							SET On_Tour=%s
							WHERE Partido_Id=%s
							AND Usuario=%s""",
							(on_tour, partido_id, usuario))

		self.confirmar()

	# Metodo para obtener la fecha de un partido
	def obtenerFechaPartido(self, partido_id:str)->Optional[str]:

		self.c.execute("""SELECT fecha
						FROM partidos
						WHERE partido_id=%s""",
						(partido_id,))

		fecha=self.c.fetchone()

		return None if not fecha else fecha["fecha"].strftime("%Y-%m-%d")

	# Metodo para actualizar ls datos del on tour de un partido asistido
	def actualizarDatosOnTourPartidoAsistido(self, partido_id:str, usuario:str, fecha_ida:str, fecha_vuelta:str, teletrabajo:bool)->None:

		self.c.execute("""UPDATE partidos_asistidos
							SET On_Tour=True, Fecha_Ida=%s, Fecha_Vuelta=%s, Teletrabajo=%s
							WHERE Partido_Id=%s
							AND Usuario=%s""",
							(fecha_ida, fecha_vuelta, teletrabajo, partido_id, usuario))

		self.confirmar()

	# Metodo para obtener las fechas minimas y maximas de los partidos
	def obtenerFechaMinimaMaximaPartidos(self, equipo_id:str)->Optional[tuple]:

		self.c.execute("""SELECT MIN(fecha) as minima, MAX(fecha) as maxima
							FROM partidos
							WHERE equipo_id_local=%s
							OR equipo_id_visitante=%s""",
							(equipo_id, equipo_id))

		fechas=self.c.fetchone()

		try:

			return (fechas["minima"].strftime("%Y-%m-%d"), fechas["maxima"].strftime("%Y-%m-%d"))

		except Exception:

			return None

	# Metodo para obtener los partidos de un equipo para el calendario
	def obtenerPartidosEquipoCalendario(self, equipo_id:str, usuario:str, ano_mes:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT p.partido_id,
								CASE WHEN p.marcador LIKE %s
										THEN REGEXP_REPLACE(p.marcador, %s, '-', 'g')
										ELSE p.marcador
								END as marcador_partido,
								p.fecha,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								p.competicion,
								pe.estadio_id as estadio_partido,
								CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_ganado,
						       CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_perdido,
   						       CASE WHEN p.resultado LIKE %s
							            THEN 1
							            ELSE 0
						       END as partido_empatado,
						       CASE WHEN pa.asistido_id IS NOT NULL
										THEN 2
										ELSE 1
								END as tipo_partido
						FROM partidos p
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						LEFT JOIN partido_estadio pe
						ON p.partido_id=pe.partido_id
						LEFT JOIN (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
						ON p.partido_id=pa.partido_id
						WHERE (p.equipo_id_local=%s
						OR p.equipo_id_visitante=%s)
						AND TO_CHAR(p.fecha,'YYYY-MM')=%s
						ORDER BY p.fecha ASC""",
						('%)%', r'\s*\(.*?\)\s*', r'%Local%', equipo_id, r'%Visitante%', equipo_id, 
						r'%Visitante%', equipo_id, r'%Local%', equipo_id, 
						r'%Empate%', usuario, equipo_id, equipo_id, ano_mes))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["marcador_partido"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["fecha"].strftime("%Y-%m-%d"),
											partido["cod_local"],
											partido["local"],
											partido["escudo_local"],
											partido["cod_visitante"],
											partido["visitante"],
											partido["escudo_visitante"],
											partido["competicion"],
											partido["estadio_partido"],
											partido["partido_ganado"],
											partido["partido_perdido"],
											partido["partido_empatado"],
											partido["tipo_partido"]), partidos))

	# Metodo para obtener la fecha del ultimo partido de una temporada
	def obtenerFechaUltimoPartidoTemporada(self, equipo_id:str, temporada:str)->Optional[str]:

		self.c.execute("""SELECT MAX(fecha) as ultima_fecha
							FROM partidos
							WHERE (equipo_id_local=%s
							OR equipo_id_visitante=%s)
							AND partido_id LIKE %s""",
							(equipo_id, equipo_id, f"{temporada}%"))

		fecha=self.c.fetchone()

		try:

			return fecha["ultima_fecha"].strftime("%Y-%m-%d")

		except Exception:

			return None

	# Metodo para obtener los proximos partidos de un equipo para el calendario
	def obtenerProximosPartidosEquipoCalendario(self, equipo_id:str, ano_mes:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT pp.partido_id, pp.fecha, pp.hora,
								pp.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								pp.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								pp.competicion
						FROM proximos_partidos pp
						LEFT JOIN equipos e1
						ON pp.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON pp.equipo_id_visitante=e2.equipo_id
						WHERE (pp.equipo_id_local=%s
						OR pp.equipo_id_visitante=%s)
						AND TO_CHAR(pp.fecha,'YYYY-MM')=%s
						ORDER BY pp.fecha ASC""",
						(equipo_id, equipo_id, ano_mes))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["hora"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["fecha"].strftime("%Y-%m-%d"),
											partido["cod_local"],
											partido["local"],
											partido["escudo_local"],
											partido["cod_visitante"],
											partido["visitante"],
											partido["escudo_visitante"],
											partido["competicion"],
											0), partidos))

	# Metodo para obtener las fechas minimas y maximas de los proximos partidos
	def obtenerFechaMinimaMaximaProximosPartidos(self, equipo_id:str)->Optional[tuple]:

		self.c.execute("""SELECT MIN(fecha) as minima, MAX(fecha) as maxima
							FROM proximos_partidos
							WHERE equipo_id_local=%s
							OR equipo_id_visitante=%s""",
							(equipo_id, equipo_id))

		fechas=self.c.fetchone()

		try:

			return (fechas["minima"].strftime("%Y-%m-%d"), fechas["maxima"].strftime("%Y-%m-%d"))

		except Exception:

			return None

	# Metodo para obtener la fecha del primer proximo partido
	def obtenerFechaPrimerProximoPartido(self, equipo_id:str)->Optional[str]:

		self.c.execute("""SELECT MIN(fecha) as primer_fecha
							FROM proximos_partidos
							WHERE equipo_id_local=%s
							OR equipo_id_visitante=%s""",
							(equipo_id, equipo_id))

		fecha=self.c.fetchone()

		try:

			return fecha["primer_fecha"].strftime("%Y-%m-%d")

		except Exception:

			return None

	# Metodo para obtener los paises
	def obtenerPaises(self)->List[str]:

		self.c.execute("""SELECT DISTINCT(pais)
	                 		FROM ciudades
	                 		ORDER BY pais""")

		paises=self.c.fetchall()

		return list(map(lambda pais: pais["pais"], paises))

	# Metodo para obtener las ciudades de un pais
	def obtenerCiudadesPais(self, pais:str, poblacion:int=0)->List[str]:

		self.c.execute("""SELECT ciudad
	                 		FROM ciudades 
	                 		WHERE pais=%s
	                 		AND poblacion>=%s
	                 		ORDER BY ciudad""",
	                 		(pais, poblacion))

		ciudades=self.c.fetchall()

		return list(map(lambda ciudad: ciudad["ciudad"], ciudades))

	# Metodo para obtener el codigo de una ciudad
	def obtenerCodigoCiudad(self, ciudad:str)->Optional[int]:

		self.c.execute("""SELECT codciudad
							FROM ciudades
							WHERE ciudad=%s""",
							(ciudad,))

		ciudad=self.c.fetchone()

		return None if ciudad is None else ciudad["codciudad"]

	# Metodo para obtener el codigo de una ciudad de un pais concreto
	def obtenerCodigoCiudadPais(self, ciudad:str, pais:str)->Optional[int]:

		self.c.execute("""SELECT codciudad
							FROM ciudades
							WHERE ciudad=%s
							AND pais=%s""",
							(ciudad, pais))

		ciudad=self.c.fetchone()

		return None if ciudad is None else ciudad["codciudad"]

	# Metodo para comprobar si existe un codigo ciudad
	def existe_codigo_ciudad(self, codigo_ciudad:str)->bool:

		self.c.execute("""SELECT *
						FROM ciudades
						WHERE codciudad=%s""",
						(codigo_ciudad,))

		return False if not self.c.fetchone() else True

	# Metodo para insertar un trayecto de un partido asistido
	def insertarTrayectoPartidoAsistido(self, trayecto_id:str, partido_id, usuario:str, tipo_trayecto:str,
						codciudad:int, transporte:str, estadio_id:str)->None:

		self.c.execute("""INSERT INTO trayecto_partido_asistido
							VALUES (%s, %s, %s, %s, %s, %s, %s)""",
							(trayecto_id, partido_id, usuario, tipo_trayecto, codciudad, transporte, estadio_id))

		self.confirmar()

	# Metodo para obtener la ciudad y pais de un usuario
	def obtenerPaisCiudadUsuario(self, usuario:str)->Optional[tuple]:

		self.c.execute("""SELECT c.pais, c.ciudad
						FROM usuarios u
						JOIN ciudades c
						ON u.codciudad=c.codciudad
						WHERE u.usuario=%s""",
						(usuario,))

		ciudad_pais=self.c.fetchone()

		return None if not ciudad_pais else (ciudad_pais["pais"], ciudad_pais["ciudad"])

	# Metodo para obtener el estadio de un partido
	def obtenerEstadioPartido(self, partido_id:str)->Optional[tuple]:

		self.c.execute("""SELECT e.ciudad, e.nombre, c.pais
						FROM partidos p
						JOIN partido_estadio pe
						ON p.partido_id=pe.partido_id
						JOIN estadios e
						ON pe.estadio_id=e.estadio_id
						JOIN ciudades c
						ON e.ciudad=c.ciudad
						WHERE p.partido_id=%s
						AND e.ciudad IS NOT NULL""",
						(partido_id,))

		estadio=self.c.fetchone()

		return None if not estadio else (estadio["ciudad"], estadio["nombre"], estadio["pais"])

	# Metodo para eliminar los trayectos de un partido asistido
	def eliminarTrayectosPartidoAsistido(self, partido_id:str, usuario:str)->None:

		self.c.execute("""DELETE FROM trayecto_partido_asistido
							WHERE Partido_Id=%s
							AND Usuario=%s""",
							(partido_id, usuario))

		self.confirmar()

	# Metodo para obtener el trayecto de de un partido asistido
	def obtenerTrayectoPartidoAsistido(self, partido_id:str, usuario:str, tipo_trayecto:str)->Optional[tuple]:

		self.c.execute("""SELECT t.Tipo_Trayecto, t.Transporte,
								CASE WHEN t.Tipo_Trayecto='I'
										THEN c1.Ciudad 
										ELSE e.Nombre
								END AS Ciudad_Origen,
								CASE WHEN t.Tipo_Trayecto='I'
										THEN cast(c1.Latitud AS FLOAT)
										ELSE cast(e.Latitud AS FLOAT)
								END as Latitud_Origen,
								CASE WHEN t.Tipo_Trayecto='I'
										THEN cast(c1.Longitud AS FLOAT)
										ELSE cast(e.Longitud AS FLOAT)
								END as Longitud_Origen,
								CASE WHEN t.Tipo_Trayecto='I'
										THEN e.Nombre
										ELSE c2.Ciudad
								END AS Ciudad_Destino,
								CASE WHEN t.Tipo_Trayecto='I'
										THEN cast(e.Latitud AS FLOAT)
										ELSE cast(c2.Latitud AS FLOAT)
								END as Latitud_Destino,
								CASE WHEN t.Tipo_Trayecto='I'
										THEN cast(e.Longitud AS FLOAT)
										ELSE cast(c2.Longitud AS FLOAT)
								END as Longitud_Destino,
								CASE WHEN t.Tipo_Trayecto='I'
									THEN REPLACE(LOWER(t.Transporte), ' ', '_')
									ELSE cast(e.Codigo_Estadio AS VARCHAR)
								END AS Imagen_Origen,
								CASE WHEN t.Tipo_Trayecto='I'
									THEN cast(e.Codigo_Estadio AS VARCHAR)
									ELSE REPLACE(LOWER(t.Transporte), ' ', '_')
								END AS Imagen_Destino
							FROM trayecto_partido_asistido t
							JOIN ciudades c1
							ON t.CodCiudad_Origen=c1.CodCiudad
							JOIN ciudades c2
							ON t.CodCiudad_Destino=c2.CodCiudad
							JOIN partidos p
							ON t.partido_id=p.partido_id
							JOIN partido_estadio pe
							ON p.partido_id=pe.partido_id
							JOIN estadios e
							ON pe.estadio_id=e.estadio_id
							WHERE t.Partido_Id=%s
							AND t.Usuario=%s
							AND t.Tipo_Trayecto=%s""",
							(partido_id, usuario, tipo_trayecto))

		trayecto=self.c.fetchone()

		return None if not trayecto else (trayecto["tipo_trayecto"],
											trayecto["transporte"],
											trayecto["ciudad_origen"],
											trayecto["latitud_origen"],
											trayecto["longitud_origen"],
											trayecto["ciudad_destino"],
											trayecto["latitud_destino"],
											trayecto["longitud_destino"],
											trayecto["imagen_origen"],
											trayecto["imagen_destino"])

	# Metodo para obtener los estadios por competicion del equipo de los partidos asistidos de un usuario
	def obtenerEstadiosPartidosAsistidosUsuarioCompeticionCantidad(self, usuario:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT eq.competicion AS competicion_nombre_simple, c.competicion_id AS codigo_competicion,
								c.nombre AS competicion_nombre_patrocinio, c.codigo_logo AS codigo_logo,
								c.codigo_pais, COUNT(DISTINCT e.estadio_id) as visitados,
								(SELECT COUNT(DISTINCT e2.estadio_id)
								    FROM equipo_estadio ee2
								    JOIN estadios e2
								    ON ee2.estadio_id=e2.estadio_id
								    JOIN equipos eq2
								    ON ee2.equipo_id=eq2.equipo_id
								    WHERE eq2.competicion=eq.competicion
								    AND eq2.codigo_competicion=eq.codigo_competicion
								    AND e2.capacidad IS NOT NULL) AS total
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_estadio pe
		                    ON p.partido_id=pe.partido_id
		                    LEFT JOIN estadios e
		                    ON pe.estadio_id=e.estadio_id
		                    LEFT JOIN equipo_estadio ee
		                    ON e.estadio_id=ee.estadio_id
		                    LEFT JOIN equipos eq
		                    ON ee.equipo_id=eq.equipo_id
		                    LEFT JOIN competiciones c
		                    ON eq.codigo_competicion=c.competicion_id
							WHERE e.capacidad IS NOT NULL
							AND eq.competicion IS NOT NULL
							GROUP BY eq.competicion, eq.codigo_competicion, c.competicion_id, c.nombre, c.codigo_logo, c.codigo_pais
							ORDER BY visitados DESC, total ASC
							LIMIT %s""",
							(usuario, numero))

		estadios_competicion_asistidos=self.c.fetchall()

		return list(map(lambda estadio_competicion: (estadio_competicion["competicion_nombre_simple"],
													estadio_competicion["codigo_competicion"],
													estadio_competicion["competicion_nombre_patrocinio"],
													estadio_competicion["codigo_logo"],
													estadio_competicion["codigo_pais"],
													estadio_competicion["visitados"],
													estadio_competicion["total"]), estadios_competicion_asistidos))

	# Metodo para obtener los estadios de una competicion del equipo de los partidos asistidos de un usuario
	def obtenerEstadiosCompeticionPartidosAsistidosUsuario(self, usuario:str, competicion:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.estadio_id, e.nombre,
							CASE WHEN e.codigo_estadio IS NULL
					            THEN -1
					            ELSE e.codigo_estadio
					        END as codigo_estadio,
					        MAX(CASE WHEN eq.escudo IS NULL
				                THEN -1
				                ELSE eq.escudo
				            END) as escudo_equipo,
					        MAX(CASE WHEN e.codigo_pais IS NULL
				                THEN 
				                	CASE WHEN eq.codigo_pais IS NULL
				                		THEN '-1'
				                		ELSE eq.codigo_pais
				           			END
				                ELSE e.codigo_pais
				            END) as pais,
						    MAX(CASE WHEN pa.partido_id IS NOT NULL
						    	THEN 1
						    	ELSE 0
						    END) AS asistido
							FROM equipos eq
							JOIN equipo_estadio ee
							ON eq.equipo_id=ee.equipo_id
							JOIN estadios e
							ON ee.estadio_id=e.estadio_id
							JOIN competiciones c
							ON eq.codigo_competicion=c.competicion_id
							LEFT JOIN partido_estadio pe
							ON pe.estadio_id=e.estadio_id
							LEFT JOIN partidos p
							ON p.partido_id=pe.partido_id
							LEFT JOIN (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
							ON pa.partido_id=p.partido_id
							WHERE eq.codigo_competicion=%s
							AND e.capacidad IS NOT NULL
							GROUP BY e.estadio_id, e.nombre, e.codigo_estadio, e.codigo_pais, eq.codigo_pais
							ORDER BY asistido DESC, e.nombre ASC
							LIMIT %s""",
							(usuario, competicion, numero))

		estadios_competicion_asistidos=self.c.fetchall()

		return list(map(lambda estadio_competicion: (estadio_competicion["estadio_id"],
													estadio_competicion["nombre"],
													estadio_competicion["codigo_estadio"],
													estadio_competicion["escudo_equipo"],
													estadio_competicion["pais"],
													estadio_competicion["asistido"]), estadios_competicion_asistidos))

	# Metodo para obtener el logo de una competicion
	def obtenerCodigoLogoCompeticion(self, competicion_id:str)->Optional[str]:

		competicion=self.obtenerDatosCompeticion(competicion_id)

		return None if not competicion else competicion[2]

	# Metodo para obtener las ciudades de los estadios de los partidos asistidos de un usuario por cantidad de veces visitadas
	def obtenerCiudadesEstadiosPartidosAsistidosUsuarioCantidad(self, usuario:str, numero:int)->List[Optional[tuple]]:

		self.c.execute("""SELECT e.pais, e.ciudad,
							MAX(CASE WHEN e.codigo_pais IS NULL
				                THEN 
				                	CASE WHEN eq.codigo_pais IS NULL
				                		THEN '-1'
				                		ELSE eq.codigo_pais
				           			END
				                ELSE e.codigo_pais
						    END) as codigo_pais,
							COUNT(DISTINCT p.partido_id) as numero_veces
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN partido_estadio pe
		                    ON p.partido_id=pe.partido_id
		                    LEFT JOIN estadios e
		                    ON pe.estadio_id=e.estadio_id
		                    LEFT JOIN equipo_estadio ee
							ON e.estadio_id=ee.estadio_id
							LEFT JOIN equipos eq
							ON ee.equipo_id=eq.equipo_id
							WHERE e.capacidad IS NOT NULL
							AND e.ciudad IS NOT NULL
							GROUP BY e.pais, e.ciudad
							ORDER BY numero_veces DESC, e.pais ASC
							LIMIT %s""",
							(usuario, numero))

		ciudades_estadios_asistidos=self.c.fetchall()

		return list(map(lambda ciudad: (ciudad["pais"],
										ciudad["ciudad"],
										ciudad["codigo_pais"],
										ciudad["numero_veces"]), ciudades_estadios_asistidos))

	# Metodo para obtener las ciudades de los estadios de los partidos asistidos de un usuario y un pais por cantidad de veces visitaas
	def obtenerCiudadesEstadiosPaisPartidosAsistidosUsuarioCantidad(self, usuario:str, codigo_pais:str, numero:int)->List[Optional[tuple]]:

		ciudades_estadios_asistidos=self.obtenerCiudadesEstadiosPartidosAsistidosUsuarioCantidad(usuario, numero)

		return list(filter(lambda ciudad: ciudad[2]==codigo_pais, ciudades_estadios_asistidos))

	# Metodo para obtener los partidos asistidos de un usuario en una ciudad concreta
	def obtenerPartidosAsistidosUsuarioCiudad(self, usuario:str, equipo_id:str, ciudad:str, codigo_pais:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT p.partido_id, p.marcador, p.fecha,
								p.equipo_id_local as cod_local, e1.nombre as local,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								p.equipo_id_visitante as cod_visitante, e2.nombre as visitante,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante,
								p.competicion,
								pe.estadio_id as estadio_partido,
								e.ciudad as ciudad_partido,
								CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_ganado,
						       CASE WHEN (p.resultado LIKE %s AND p.equipo_id_local=%s) 
						              OR (p.resultado LIKE %s AND p.equipo_id_visitante=%s) 
							            THEN 1
							            ELSE 0
						       END as partido_perdido,
   						       CASE WHEN p.resultado LIKE %s
							            THEN 1
							            ELSE 0
						       END as partido_empatado
						FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
	                    LEFT JOIN partidos p
	                    ON pa.partido_id=p.partido_id
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						LEFT JOIN partido_estadio pe
						ON p.partido_id=pe.partido_id
						LEFT JOIN estadios e
						ON pe.estadio_id=e.estadio_id
						WHERE LOWER(e.ciudad)=%s
						AND e.codigo_pais=%s
						ORDER BY p.fecha DESC""",
						(r'%Local%', equipo_id, r'%Visitante%', equipo_id, 
						r'%Visitante%', equipo_id, r'%Local%', equipo_id, 
						r'%Empate%', usuario, ciudad.lower(), codigo_pais))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["marcador"],
											partido["fecha"].strftime("%d/%m/%Y"),
											partido["cod_local"],
											partido["local"],
											partido["escudo_local"],
											partido["cod_visitante"],
											partido["visitante"],
											partido["escudo_visitante"],
											partido["competicion"],
											partido["estadio_partido"],
											partido["ciudad_partido"],
											partido["partido_ganado"],
											partido["partido_perdido"],
											partido["partido_empatado"]), partidos))

	# Metodo para obtener la informacion de una ciudad
	def obtenerCiudad(self, ciudad:str, codigo_pais:str)->Optional[tuple]:

		self.c.execute("""SELECT c.ciudad, c.pais, e.codigo_pais
						FROM ciudades c
						JOIN estadios e
						ON c.ciudad=e.ciudad
    					WHERE LOWER(c.ciudad)=%s
    					AND e.codigo_pais=%s""",
						(ciudad.lower(), codigo_pais))

		ciudad=self.c.fetchone()

		return None if not ciudad else (ciudad["ciudad"],
										ciudad["pais"],
										ciudad["codigo_pais"])

	# Metodo para obtener las coordenadas de una ciudad
	def obtenerCoordenadasCiudad(self, codigo_ciudad:str)->Optional[tuple]:

		self.c.execute("""SELECT latitud, longitud
						FROM ciudades
    					WHERE codciudad=%s""",
						(codigo_ciudad,))

		coordenadas=self.c.fetchone()

		return None if not coordenadas else (coordenadas["latitud"],
											coordenadas["longitud"])

	# Metodo para insertar multiples trayectos de un partido asistido
	def insertarTrayectosPartidoAsistido(self, df:pd.DataFrame)->None:

		trayectos=df.values.tolist()

		for trayecto in trayectos:

			self.insertarTrayectoPartidoAsistido(trayecto[0], trayecto[1], trayecto[2], trayecto[3], trayecto[4], trayecto[5], trayecto[6])

	# Metodo para obtener los trayectos de de un partido asistido
	def obtenerTrayectosPartidoAsistido(self, partido_id:str, usuario:str, tipo_trayecto:str)->Optional[tuple]:

		self.c.execute(r"""WITH trayectos_numerados AS (
							SELECT t.*, c1.Ciudad AS Ciudad_Origen_Ciudad, c2.Ciudad AS Ciudad_Destino_Ciudad,
									c1.Pais AS Pais_Origen_Ciudad, c2.Pais AS Pais_Destino_Ciudad,
									e.Nombre AS Estadio_Nombre, e.Pais AS Pais_Estadio, c1.Latitud AS Ciudad_Origen_Lat, c1.Longitud AS Ciudad_Origen_Lon,
									c2.Latitud AS Ciudad_Destino_Lat, c2.Longitud AS Ciudad_Destino_Lon, e.Latitud AS Estadio_Lat,
									e.Longitud AS Estadio_Lon, e.Codigo_Estadio,
									REPLACE(LOWER(t.Transporte), ' ', '_') AS Transporte_Normalizado,
									COALESCE(CAST(REGEXP_REPLACE(t.Trayecto_Id, '.*_(\d+)$', '\1') AS INT),0) AS num_trayecto,
									MAX(COALESCE(CAST(REGEXP_REPLACE(t.Trayecto_Id, '.*_(\d+)$', '\1') AS INT), 0)) OVER () AS max_num_trayecto,
									MIN(COALESCE(CAST(REGEXP_REPLACE(t.Trayecto_Id, '.*_(\d+)$', '\1') AS INT), 0)) OVER () AS min_num_trayecto,
									CASE WHEN COALESCE(CAST(REGEXP_REPLACE(t.Trayecto_Id, '.*_(\d+)$', '\1') AS INT),0)=MAX(COALESCE(CAST(REGEXP_REPLACE(t.Trayecto_Id, '.*_(\d+)$', '\1') AS INT), 0)) OVER ()
										THEN TRUE
										ELSE FALSE
									END AS es_maximo,
									CASE WHEN COALESCE(CAST(REGEXP_REPLACE(t.Trayecto_Id, '.*_(\d+)$', '\1') AS INT),0)=MIN(COALESCE(CAST(REGEXP_REPLACE(t.Trayecto_Id, '.*_(\d+)$', '\1') AS INT), 0)) OVER ()
										THEN TRUE
										ELSE FALSE
									END AS es_minimo
							FROM trayecto_partido_asistido t
							JOIN ciudades c1
							ON t.CodCiudad_Origen=c1.CodCiudad
							JOIN ciudades c2
							ON t.CodCiudad_Destino=c2.CodCiudad
							JOIN partidos p
							ON t.partido_id=p.partido_id
							JOIN partido_estadio pe
							ON p.partido_id=pe.partido_id
							JOIN estadios e
							ON pe.estadio_id=e.estadio_id
							WHERE t.Partido_Id=%s
							AND t.Usuario=%s
							AND t.Tipo_Trayecto=%s)

		SELECT t.Trayecto_Id, t.Tipo_Trayecto, t.Transporte, t.num_trayecto, t.es_maximo, t.es_minimo,
			    CASE WHEN t.Tipo_Trayecto = 'V' AND t.es_minimo=True
					THEN t.Estadio_Nombre
					ELSE t.Ciudad_Origen_Ciudad
			    END AS Ciudad_Origen,
			    CASE WHEN t.Tipo_Trayecto = 'V' AND t.es_minimo=True
					THEN t.Pais_Estadio
					ELSE t.Pais_Origen_Ciudad
			    END AS Pais_Origen,
			    CASE WHEN t.Tipo_Trayecto = 'V' AND t.es_minimo=True
					THEN CAST(t.Estadio_Lat AS FLOAT)
					ELSE CAST(t.Ciudad_Origen_Lat AS FLOAT)
			    END AS Latitud_Origen,
			    CASE WHEN t.Tipo_Trayecto = 'V' AND t.es_minimo=True
					THEN CAST(t.Estadio_Lon AS FLOAT)
			        ELSE CAST(t.Ciudad_Origen_Lon AS FLOAT)
			    END AS Longitud_Origen,
			    CASE WHEN t.Tipo_Trayecto = 'I' AND t.es_maximo=True
					THEN t.Estadio_Nombre
			        ELSE t.Ciudad_Destino_Ciudad
			    END AS Ciudad_Destino,
			    CASE WHEN t.Tipo_Trayecto = 'I' AND t.es_maximo=True
					THEN t.Pais_Estadio
			        ELSE t.Pais_Destino_Ciudad
			    END AS Pais_Destino,
			    CASE WHEN t.Tipo_Trayecto = 'I' AND t.es_maximo=True
					THEN CAST(t.Estadio_Lat AS FLOAT)
			        ELSE CAST(t.Ciudad_Destino_Lat AS FLOAT)
			    END AS Latitud_Destino,
			    CASE WHEN t.Tipo_Trayecto = 'I' AND t.es_maximo=True
					THEN CAST(t.Estadio_Lon AS FLOAT)
			        ELSE CAST(t.Ciudad_Destino_Lon AS FLOAT)
			    END AS Longitud_Destino,
			    CASE WHEN t.Tipo_Trayecto = 'V' AND t.es_minimo=True
					THEN CAST(t.Codigo_Estadio AS VARCHAR)
			        ELSE t.Transporte_Normalizado
			    END AS Imagen_Origen,
			    CASE WHEN t.Tipo_Trayecto = 'I' AND t.es_maximo=True
					THEN CAST(t.Codigo_Estadio AS VARCHAR)
			        ELSE t.Transporte_Normalizado
			    END AS Imagen_Destino,
			    CASE WHEN t.Tipo_Trayecto = 'I' AND t.es_minimo=True
					THEN 'origen'
				WHEN t.Tipo_Trayecto = 'V' AND t.es_minimo=True
					THEN 'estadio_mapa'
					ELSE 'destino'
			    END AS Imagen_Tramo_Origen,
			    CASE WHEN t.Tipo_Trayecto = 'I' AND t.es_maximo=True
			    	THEN 'estadio_mapa'
			    WHEN t.Tipo_Trayecto = 'V' AND t.es_maximo=True
					THEN 'origen'
					else 'destino'
			    END AS Imagen_Tramo_Destino
		FROM trayectos_numerados t
		ORDER BY t.Trayecto_Id""",
		(partido_id, usuario, tipo_trayecto))

		trayectos=self.c.fetchall()

		return list(map(lambda trayecto: (trayecto["trayecto_id"],
											trayecto["tipo_trayecto"],
											trayecto["transporte"],
											trayecto["ciudad_origen"],
											trayecto["pais_origen"],
											trayecto["latitud_origen"],
											trayecto["longitud_origen"],
											trayecto["ciudad_destino"],
											trayecto["pais_destino"],
											trayecto["latitud_destino"],
											trayecto["longitud_destino"],
											trayecto["imagen_origen"],
											trayecto["imagen_destino"],
											trayecto["imagen_tramo_origen"],
											trayecto["imagen_tramo_destino"]), trayectos))