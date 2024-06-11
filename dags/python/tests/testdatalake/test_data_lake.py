import pytest
from azure.storage.filedatalake import DataLakeServiceClient, FileSystemClient

from src.datalake.conexion_data_lake import ConexionDataLake

@pytest.mark.parametrize(["cuenta", "clave"],
	[("", ""),("cuenta", "clave")]
)
def test_crear_conexion_data_lake_error(cuenta, clave):

	with pytest.raises(Exception):

		ConexionDataLake(cuenta, clave)

def test_crear_conexion_data_lake():

	datalake=ConexionDataLake()

	assert isinstance(datalake.cliente_data_lake, DataLakeServiceClient)

	datalake.cerrarConexion()

def test_crear_contenedor_data_lake(datalake):

	datalake.crearContenedor("contenedor1")

	contenedores=list(datalake.cliente_data_lake.list_file_systems())

	assert contenedores[0]["name"]=="contenedor1"

	datalake.cerrarConexion()

def test_crear_contenedor_data_lake_existe_error(datalake):

	with pytest.raises(Exception):

		datalake.crearContenedor("contenedor1")

	datalake.cerrarConexion()

def test_contenedores_data_lake(datalake):

	contenedores=datalake.contenedores_data_lake()

	assert len(contenedores)==1

	datalake.cerrarConexion()

def test_eliminar_contenedor_data_lake(datalake):

	datalake.eliminarContenedor("contenedor1")

	contenedores=datalake.contenedores_data_lake()

	assert not contenedores

	datalake.cerrarConexion()

def test_eliminar_contenedor_data_lake_no_existe_error(datalake):

	with pytest.raises(Exception):

		datalake.eliminarContenedor("contenedor1")

	datalake.cerrarConexion()

def test_conexion_disponible(datalake):

	assert datalake.conexion_disponible()

	datalake.cerrarConexion()

@pytest.mark.parametrize(["nombre_contenedor"],
	[("contenedor1",),("contenedornacho",),("no_existo",)]
)
def test_existe_contenedor_no_existe(datalake, nombre_contenedor):

	assert not datalake.existe_contenedor(nombre_contenedor)

	datalake.cerrarConexion()

def test_existe_contenedor_existe(datalake):

	datalake.crearContenedor("contenedor2")

	assert datalake.existe_contenedor("contenedor2")

	datalake.cerrarConexion()

def test_obtener_contenedor_no_existe(datalake):

	with pytest.raises(Exception):

		datalake.obtenerContenedor("contenedornacho")

	datalake.cerrarConexion()

def test_obtener_contenedor_existe(datalake):

	objeto_contenedor=datalake.obtenerContenedor("contenedor2")

	assert isinstance(objeto_contenedor, FileSystemClient)

	datalake.eliminarContenedor("contenedor2")

	datalake.cerrarConexion()