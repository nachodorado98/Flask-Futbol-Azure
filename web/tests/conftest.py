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

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre_Completo, Nombre, Siglas, Escudo, Puntuacion, Pais, Ciudad,
												Competicion, Temporadas, Fundacion, Entrenador, Codigo_Entrenador, Presidente,
												Codigo_Presidente)
						VALUES('atletico-madrid', 'Club Atletico de Madrid', 'Atletico', 'ATM', 369, 94, 'España', 'Madrid',
								'Primera', 88, 1903, 'Cholo Simeone', 13, 'Cerezo', 27257)""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('20190622', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO estadios
						VALUES('metropolitano', '23', 'Metropolitano', 'Av Luis Aragones', '40.436', '-3.599', 'Madrid', 100000, 2017, 105, 68, 'Telefono', 'Cedped')""")

	conexion.c.execute("""INSERT INTO partido_estadio
						VALUES('20190622', 'metropolitano')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano')""")

	conexion.confirmar()

	return conexion