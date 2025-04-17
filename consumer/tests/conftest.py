import os
import sys
sys.path.append("..")

import pytest
from src.datalake.conexion_data_lake import ConexionDataLake
from src.config import CONTENEDOR

@pytest.fixture()
def datalake():

    return ConexionDataLake()

def pytest_sessionstart(session):

    dl=ConexionDataLake()

    if not dl.existe_carpeta(CONTENEDOR, "usuarios"):

        dl.crearCarpeta(CONTENEDOR, "usuarios")

    else:

        dl.eliminarCarpeta(CONTENEDOR, "usuarios")

        dl.crearCarpeta(CONTENEDOR, "usuarios")

    dl.cerrarConexion()

    print("\nEntorno del DataLake creado")

def pytest_sessionfinish(session, exitstatus):

    dl=ConexionDataLake()

    if dl.existe_carpeta(CONTENEDOR, "usuarios"):

        dl.eliminarCarpeta(CONTENEDOR, "usuarios")

    dl.crearCarpeta(CONTENEDOR, "usuarios")

    dl.cerrarConexion()

    print("\nLimpieza del DataLake correcta")