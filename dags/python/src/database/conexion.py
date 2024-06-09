import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List

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
						FROM ligas""")

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