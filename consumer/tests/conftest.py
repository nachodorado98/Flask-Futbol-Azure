import os
import sys
sys.path.append("..")

import pytest
from src.datalake.conexion_data_lake import ConexionDataLake

@pytest.fixture()
def datalake():

    return ConexionDataLake()