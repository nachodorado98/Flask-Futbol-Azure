import os
import sys
sys.path.append("..")

import pytest
from src.datalake.conexion_data_lake import ConexionDataLake

@pytest.fixture()
def datalake():

	return ConexionDataLake()

@pytest.fixture()
def entorno():

	return "dev"

def pytest_sessionstart(session):

	entorno="dev"

	dl=ConexionDataLake()

	if not dl.existe_contenedor(entorno):

		dl.crearContenedor(entorno)

	if not dl.existe_carpeta(entorno, "usuarios"):

		dl.crearCarpeta(entorno, "usuarios")

	else:

		dl.eliminarCarpeta(entorno, "usuarios")

		dl.crearCarpeta(entorno, "usuarios")

	dl.cerrarConexion()

	print("\nEntorno del DataLake creado")

def pytest_sessionfinish(session, exitstatus):

	entorno="dev"

	dl=ConexionDataLake()

	if dl.existe_carpeta(entorno, "usuarios"):

		dl.eliminarCarpeta(entorno, "usuarios")

	dl.crearCarpeta(entorno, "usuarios")

	dl.cerrarConexion()

	print("\nLimpieza del DataLake correcta")