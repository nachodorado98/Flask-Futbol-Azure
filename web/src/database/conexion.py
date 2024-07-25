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

	# Metodo para insertar un usuario
	def insertarUsuario(self, usuario:str, correo:str, contrasena:str, nombre:str,
						apellido:str, fecha_nacimiento:str, equipo:str)->None:

		self.c.execute("""INSERT INTO usuarios
							VALUES (%s, %s, %s, %s, %s, %s, %s)""",
							(usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, equipo))

		self.confirmar()

	# Metodo para comprobar si ya existe un usuario
	def existe_usuario(self, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		return False if self.c.fetchone() is None else True

	# Metodo para comprobar si ya existe un equipo
	def existe_equipo(self, equipo:str)->bool:

		self.c.execute("""SELECT *
						FROM equipos
						WHERE equipo_id=%s""",
						(equipo,))

		return False if self.c.fetchone() is None else True

	# Metodo para obtener la contrasena de un usuario
	def obtenerContrasenaUsuario(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT contrasena
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		contrasena=self.c.fetchone()

		return None if contrasena is None else contrasena["contrasena"]

	# Metodo para obtener el nombre del usuario
	def obtenerNombre(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT nombre
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		nombre=self.c.fetchone()

		return None if nombre is None else nombre["nombre"]

	# Metodo para obtener el equipo del usuario
	def obtenerEquipo(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT equipo_id
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		equipo=self.c.fetchone()

		return None if equipo is None else equipo["equipo_id"]

	# Metodo para obtener el nombre del equipo
	def obtenerNombreEquipo(self, equipo:str)->Optional[str]:

		self.c.execute("""SELECT nombre_completo
						FROM equipos
						WHERE equipo_id=%s""",
						(equipo,))

		nombre_equipo=self.c.fetchone()

		return None if nombre_equipo is None else nombre_equipo["nombre_completo"]

	# Metodo para obtener los partidos de un equipo
	def obtenerPartidosEquipo(self, equipo:str)->List[tuple]:

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
						WHERE p.equipo_id_local=%s
						OR p.equipo_id_visitante=%s
						ORDER BY fecha DESC""",
						(equipo, equipo))

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

	# Metodo para obtener los partidos de un equipo de local
	def obtenerPartidosEquipoLocal(self, equipo:str)->List[tuple]:

		partidos=self.obtenerPartidosEquipo(equipo)

		return list(filter(lambda partido: partido[3]==equipo, partidos))

	# Metodo para obtener los partidos de un equipo de visitante
	def obtenerPartidosEquipoVisitante(self, equipo:str)->List[tuple]:

		partidos=self.obtenerPartidosEquipo(equipo)

		return list(filter(lambda partido: partido[6]==equipo, partidos))

	# Metodo para obtener las temporadas de los partidos
	def obtenerTemporadasEquipo(self, equipo:str)->List[tuple]:

		self.c.execute("""SELECT DISTINCT CAST(LEFT(partido_id, 4) AS INTEGER) AS temporada
						FROM partidos
						WHERE equipo_id_local=%s
						OR equipo_id_visitante=%s
						ORDER BY temporada DESC""",
						(equipo, equipo))

		temporadas=self.c.fetchall()

		return list(map(lambda temporada: temporada["temporada"], temporadas))

	# Metodo para saber si existe el partido
	def existe_partido(self, partido_id:str)->bool:

		self.c.execute("""SELECT *
							FROM partidos
							WHERE Partido_Id=%s""",
							(partido_id,))

		return False if self.c.fetchone() is None else True

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
								END as estadio_partido
						FROM partidos p
						LEFT JOIN equipos e1
						ON p.equipo_id_local=e1.equipo_id
						LEFT JOIN equipos e2
						ON p.equipo_id_visitante=e2.equipo_id
						LEFT JOIN partido_estadio pe
						ON p.partido_id=pe.partido_id
						LEFT JOIN estadios e
						ON pe.estadio_id=e.estadio_id
						WHERE p.partido_id=%s""",
						(partido_id,))

		partido=self.c.fetchone()

		return None if partido is None else (partido["marcador"],
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
											partido["estadio_partido"])