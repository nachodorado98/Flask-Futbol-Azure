import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List

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

		self.c.execute("DELETE FROM temporada_jugadores")

		self.c.execute("DELETE FROM usuarios")

		self.c.execute("DELETE FROM partidos_asistidos")

		self.confirmar()

	# Metodo para insertar un usuario
	def insertarUsuario(self, usuario:str, correo:str, contrasena:str, nombre:str,
						apellido:str, fecha_nacimiento:str, equipo_id:str)->None:

		self.c.execute("""INSERT INTO usuarios
							VALUES (%s, %s, %s, %s, %s, %s, %s)""",
							(usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, equipo_id))

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
						       END as partido_ganado
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
						(r'%Local%', equipo_id, r'%Visitante%', equipo_id, equipo_id, equipo_id))

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
											partido["partido_ganado"]), partidos))

	# Metodo para obtener los partidos de un equipo de local
	def obtenerPartidosEquipoLocal(self, equipo_id:str)->List[tuple]:

		partidos=self.obtenerPartidosEquipo(equipo_id)

		return list(filter(lambda partido: partido[3]==equipo_id, partidos))

	# Metodo para obtener los partidos de un equipo de visitante
	def obtenerPartidosEquipoVisitante(self, equipo_id:str)->List[tuple]:

		partidos=self.obtenerPartidosEquipo(equipo_id)

		return list(filter(lambda partido: partido[6]==equipo_id, partidos))

	# Metodo para obtener el estadio de un equipo
	def estadio_equipo(self, equipo_id:str)->Optional[tuple]:

		self.c.execute("""SELECT estadio_id
							FROM equipo_estadio
							WHERE equipo_id=%s""",
							(equipo_id,))

		estadio=self.c.fetchone()

		return None if not estadio else estadio["estadio_id"]

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
								END as competicion_existe
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
										equipo["equipo_pais"])

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

		self.c.execute("""SELECT nombre,
								CASE WHEN codigo_estadio IS NULL
										THEN -1
										ELSE codigo_estadio
								END as imagen_estadio,
								direccion, latitud, longitud, ciudad, CAST(capacidad AS TEXT) AS espectadores, fecha, largo, ancho
						FROM estadios
						WHERE estadio_id=%s""",
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
										estadio["ancho"])

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
						       MAX(CASE WHEN eq.codigo_pais IS NULL
						                THEN '-1'
						                ELSE eq.codigo_pais
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
						       MAX(CASE WHEN eq.codigo_pais IS NULL
						                THEN '-1'
						                ELSE eq.codigo_pais
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

	# Metodo para obtener los partidos asistidos de un usuario
	def obtenerPartidosAsistidosUsuario(self, usuario:str)->List[Optional[tuple]]:

		self.c.execute("""SELECT pa.partido_id, p.marcador, p.fecha, p.competicion,
								CASE WHEN e1.escudo IS NULL
										THEN -1
										ELSE e1.escudo
								END as escudo_local,
								CASE WHEN e2.escudo IS NULL
										THEN -1
										ELSE e2.escudo
								END as escudo_visitante
							FROM (SELECT * FROM partidos_asistidos WHERE usuario=%s) pa
		                    LEFT JOIN partidos p
		                    ON pa.partido_id=p.partido_id
		                    LEFT JOIN equipos e1
							ON p.equipo_id_local=e1.equipo_id
							LEFT JOIN equipos e2
							ON p.equipo_id_visitante=e2.equipo_id
							ORDER BY p.fecha DESC""",
							(usuario,))

		asistidos=self.c.fetchall()

		return list(map(lambda asistido: (asistido["partido_id"],
											asistido["marcador"],
											asistido["fecha"].strftime("%d/%m/%Y"),
											asistido["competicion"],
											asistido["escudo_local"],
											asistido["escudo_visitante"]), asistidos))

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
						       MAX(CASE WHEN eq.codigo_pais IS NULL
						                THEN '-1'
						                ELSE eq.codigo_pais
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
						       MAX(CASE WHEN eq.codigo_pais IS NULL
						                THEN '-1'
						                ELSE eq.codigo_pais
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
								pa.comentario
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
											asistido["comentario"])

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