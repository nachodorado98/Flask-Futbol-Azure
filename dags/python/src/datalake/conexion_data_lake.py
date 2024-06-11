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

		except Exception as e:

			raise Exception("Error al crear la conexion con cliente del data lake")

	# Metodo para cerrar la conexion con el Data Lake
	def cerrarConexion(self)->None:

		self.cliente_data_lake.close()

	# Metodo para crear un contenedor
	def crearContenedor(self, nombre_contenedor:str)->None:

		try:

			self.cliente_data_lake.create_file_system(file_system=nombre_contenedor)

		except Exception as e:

			raise Exception("Error al crear el contenedor")

	# Metodo para obtener los contenedores del data lake
	def contenedores_data_lake(self)->Optional[List[Dict]]:

		try:

			contenedores=self.cliente_data_lake.list_file_systems()

			return list(contenedores)

		except Exception as e:

			raise Exception("Error al obtener los contenedores")

	# Metodo para eliminar un contenedor
	def eliminarContenedor(self, nombre_contenedor:str)->None:

		try:

			self.cliente_data_lake.delete_file_system(file_system=nombre_contenedor)

		except Exception as e:

			raise Exception("Error al eliminar el contenedor")