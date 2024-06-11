from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.filedatalake import FileSystemClient
from typing import List, Dict, Optional

from .confconexiondatalake import CUENTA, CLAVE

# Clase para la conexion con el Data Lake
class ConexionDataLake:

	def __init__(self, cuenta:str=CUENTA, clave:str=CLAVE)->None:

		try:

			url_data_lake=f"https://{cuenta}.dfs.core.windows.net"

			self.cliente_data_lake=DataLakeServiceClient(url_data_lake, credential=clave)

		except Exception:

			raise Exception("Error al crear la conexion con cliente del data lake")

		if not self.conexion_disponible():

			self.cerrarConexion()

			raise Exception("Error al crear la conexion con cliente del data lake")

	# Metodo para cerrar la conexion con el Data Lake
	def cerrarConexion(self)->None:

		self.cliente_data_lake.close()

	# Metodo para obtener los contenedores del data lake
	def contenedores_data_lake(self)->Optional[List[Dict]]:

		try:

			contenedores=self.cliente_data_lake.list_file_systems()

			return list(contenedores)

		except Exception:

			raise Exception("Error al obtener los contenedores")

	# Metodo para comprobar que la conexion esta disponible
	def conexion_disponible(self)->bool:

		try:

			self.contenedores_data_lake()

			return True

		except Exception:

			return False

	# Metodo para comprobar que existe un contenedor
	def existe_contenedor(self, nombre_contenedor:str)->bool:

		contenedores=self.contenedores_data_lake()

		contenedores_existen=list(filter(lambda contenedor: nombre_contenedor==contenedor["name"], contenedores))

		return False if not contenedores_existen else True

	# Metodo para crear un contenedor
	def crearContenedor(self, nombre_contenedor:str)->None:

		if self.existe_contenedor(nombre_contenedor):

			raise Exception("Error al crear el contenedor. Contenedor existente")

		try:

			self.cliente_data_lake.create_file_system(file_system=nombre_contenedor)

		except Exception:

			raise Exception("Error al crear el contenedor")

	# Metodo para eliminar un contenedor
	def eliminarContenedor(self, nombre_contenedor:str)->None:

		if not self.existe_contenedor(nombre_contenedor):

			raise Exception("Error al eliminar el contenedor. Contenedor no existente")

		try:

			self.cliente_data_lake.delete_file_system(file_system=nombre_contenedor)

		except Exception:

			raise Exception("Error al eliminar el contenedor")

	# Metodo para obtener un objeto contenedor
	def obtenerContenedor(self, nombre_contenedor:str)->Optional[FileSystemClient]:

		if not self.existe_contenedor(nombre_contenedor):

			raise Exception("Error al obtener el contenedor")

		return self.cliente_data_lake.get_file_system_client(nombre_contenedor)

	# Metodo para obtener los paths de un contenedor
	def paths_contenedor(self, nombre_contenedor:str)->Optional[List[Dict]]:

		if not self.existe_contenedor(nombre_contenedor):

			raise Exception("Error al obtener los paths en el contenedor. Contenedor no existente")

		objeto_contenedor=self.obtenerContenedor(nombre_contenedor)

		paths=objeto_contenedor.get_paths()

		return list(paths)

	# Metodo para comprobar que existe una carpeta en un contenedor
	def existe_carpeta(self, nombre_contenedor:str, nombre_carpeta:str)->bool:

		if not self.existe_contenedor(nombre_contenedor):

			raise Exception("Error al comprobar la carpeta en el contenedor. Contenedor no existente")

		paths=self.paths_contenedor(nombre_contenedor)

		paths_existen=list(filter(lambda path: nombre_carpeta==path["name"], paths))

		return False if not paths_existen else True

	# Metodo para crear una carpeta en un contenedor
	def crearCarpeta(self, nombre_contenedor:str, nombre_carpeta:str)->None:

		if not self.existe_contenedor(nombre_contenedor):

			raise Exception("Error al crear la carpeta en el contenedor. Contenedor no existente")

		if self.existe_carpeta(nombre_contenedor, nombre_carpeta):

			raise Exception("Error al crear la carpeta en el contenedor. Carpeta existente")

		objeto_contenedor=self.obtenerContenedor(nombre_contenedor)

		objeto_contenedor.create_directory(nombre_carpeta)

	# Metodo para eliminar una carpeta en un contenedor
	def eliminarCarpeta(self, nombre_contenedor:str, nombre_carpeta:str)->None:

		if not self.existe_contenedor(nombre_contenedor):

			raise Exception("Error al eliminar la carpeta en el contenedor. Contenedor no existente")

		if not self.existe_carpeta(nombre_contenedor, nombre_carpeta):

			raise Exception("Error al eliminar la carpeta en el contenedor. Carpeta no existente")

		objeto_contenedor=self.obtenerContenedor(nombre_contenedor)

		objeto_contenedor.delete_directory(nombre_carpeta)

	# Metodo para obtener los paths de una carpeta de un contenedor
	def paths_carpeta_contenedor(self, nombre_contenedor:str, nombre_carpeta:str)->Optional[List[Dict]]:

		if not self.existe_contenedor(nombre_contenedor):

			raise Exception("Error al obtener los paths en el contenedor. Contenedor no existente")

		if not self.existe_carpeta(nombre_contenedor, nombre_carpeta):

			raise Exception("Error al obtener los paths en el contenedor. Carpeta no existente")

		objeto_contenedor=self.obtenerContenedor(nombre_contenedor)

		paths=objeto_contenedor.get_paths(path=nombre_carpeta)

		return list(paths)