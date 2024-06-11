import pytest
from azure.storage.filedatalake import DataLakeServiceClient

from src.datalake.conexion_data_lake import ConexionDataLake

def test_crear_conexion_data_lake_error():

	with pytest.raises(Exception):

		ConexionDataLake("", "")

def test_crear_conexion_data_lake_no_error():

	datalake=ConexionDataLake("cuenta", "clave")

	assert isinstance(datalake.cliente_data_lake, DataLakeServiceClient)

	datalake.cerrarConexion()

def test_crear_conexion_data_lake():

	datalake=ConexionDataLake()

	assert isinstance(datalake.cliente_data_lake, DataLakeServiceClient)

	datalake.cerrarConexion()

def test_crear_contenedor_data_lake_error():

	datalake=ConexionDataLake("cuenta", "clave")

	with pytest.raises(Exception):

		datalake.crearContenedor("contenedor1")

	datalake.cerrarConexion()

def test_crear_contenedor_data_lake():

	datalake=ConexionDataLake()

	datalake.crearContenedor("contenedor1")

	contenedores=list(datalake.cliente_data_lake.list_file_systems())

	assert contenedores[0]["name"]=="contenedor1"

	datalake.cerrarConexion()

def test_crear_contenedor_data_lake_existe():

	datalake=ConexionDataLake()

	with pytest.raises(Exception):

		datalake.crearContenedor("contenedor1")

	datalake.cerrarConexion()

def test_contenedores_data_lake_error():

	datalake=ConexionDataLake("cuenta", "clave")

	with pytest.raises(Exception):

		datalake.contenedores_data_lake()

	datalake.cerrarConexion()

def test_contenedores_data_lake():

	datalake=ConexionDataLake()

	contenedores=datalake.contenedores_data_lake()

	assert len(contenedores)==1

	datalake.cerrarConexion()

def test_eliminar_contenedor_data_lake_error():

	datalake=ConexionDataLake("cuenta", "clave")

	with pytest.raises(Exception):

		datalake.eliminarContenedor("contenedor1")

	datalake.cerrarConexion()

def test_eliminar_contenedor_data_lake():

	datalake=ConexionDataLake()

	datalake.eliminarContenedor("contenedor1")

	contenedores=datalake.contenedores_data_lake()

	assert not contenedores

	datalake.cerrarConexion()

def test_eliminar_contenedor_data_lake_no_existe():

	datalake=ConexionDataLake()

	with pytest.raises(Exception):

		datalake.eliminarContenedor("contenedor1")

	datalake.cerrarConexion()