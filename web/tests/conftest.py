import os
import sys
sys.path.append("..")

import pytest
from src import crear_app
from src.database.conexion import Conexion
from confmain import config

@pytest.fixture()
def app():

	configuracion=config["development"]

	app=crear_app(configuracion)

	yield app

@pytest.fixture()
def cliente(app):

	return app.test_client()

@pytest.fixture()
def conexion():

	con=Conexion()

	con.c.execute("DELETE FROM equipos")

	con.c.execute("DELETE FROM estadios")

	con.c.execute("DELETE FROM partidos")

	con.c.execute("DELETE FROM usuarios")

	con.confirmar()

	return con

@pytest.fixture()
def conexion_entorno(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id)
						VALUES('atletico-madrid')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('20190622', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	return conexion