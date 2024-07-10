import psycopg2
from psycopg2.extras import RealDictCursor

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
	def insertarUsuario(self, usuario:str, contrasena:str, nombre:str, apellido:str, fecha_nacimiento:str, equipo:str)->None:

		self.c.execute("""INSERT INTO usuarios
							VALUES (%s, %s, %s, %s, %s, %s)""",
							(usuario, contrasena, nombre, apellido, fecha_nacimiento, equipo))

		self.confirmar()

	# Metodo para comprobar si ya existe un usuario
	def existe_usuario(self, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		usuario=self.c.fetchone()

		return False if usuario is None else True