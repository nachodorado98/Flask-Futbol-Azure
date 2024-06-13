import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional

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

	#Metodo para insertar un estadio
	def insertarEstadio(self, estadio:List[str])->None:

		self.c.execute("""INSERT INTO estadios
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
	def obtenerCodigoEscudos(self)->Optional[List[int]]:

		self.c.execute("""SELECT Escudo
							FROM equipos
							WHERE Escudo IS NOT NULL""")

		escudos=self.c.fetchall()

		return list(map(lambda escudo: escudo["escudo"], escudos)) if escudos else None

	# Metodo para obtener los codigos de los entrenadores
	def obtenerCodigoEntrenadores(self)->Optional[List[int]]:

		self.c.execute("""SELECT Codigo_Entrenador
							FROM equipos
							WHERE Codigo_Entrenador IS NOT NULL""")

		codigo_entrenadores=self.c.fetchall()

		return list(map(lambda codigo_entrenador: codigo_entrenador["codigo_entrenador"], codigo_entrenadores)) if codigo_entrenadores else None