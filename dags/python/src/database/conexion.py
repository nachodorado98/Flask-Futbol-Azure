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