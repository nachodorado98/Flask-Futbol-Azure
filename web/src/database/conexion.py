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

	# Metodo para obtener los partidos de un equipo
	def obtenerPartidosEquipo(self, equipo:str)->List[tuple]:

		self.c.execute("""SELECT partido_id, equipo_id_local, equipo_id_visitante, marcador, TO_CHAR(fecha, 'DD-MM-YYYY') as fecha
						FROM partidos
						WHERE equipo_id_local=%s OR equipo_id_visitante=%s
						ORDER BY fecha""",
						(equipo, equipo))

		partidos=self.c.fetchall()

		return list(map(lambda partido: (partido["partido_id"],
											partido["equipo_id_local"],
											partido["equipo_id_visitante"],
											partido["marcador"],
											partido["fecha"]), partidos))