import os
import sys
sys.path.append("..")

import pytest
from src import crear_app
from src.database.conexion import Conexion
from src.datalake.conexion_data_lake import ConexionDataLake
from confmain import config
from src.utilidades.utils import vaciarCarpeta

@pytest.fixture()
def app():

	configuracion=config["development"]

	app=crear_app(configuracion)

	yield app

@pytest.fixture()
def cliente(app):

	return app.test_client()

@pytest.fixture()
def password_hash():

	return "$2b$12$NZ.GhycT.kofGXpTgwyYuenY/BPbF1dpO7udruM.sKb09/46Gn7aK"

@pytest.fixture()
def entorno():

	return config["development"].ENVIROMENT

@pytest.fixture()
def conexion(entorno):

	con=Conexion(entorno)

	con.vaciarBBDD()

	return con

@pytest.fixture()
def conexion_entorno(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre_Completo, Nombre, Siglas, Escudo, Puntuacion, Pais, Codigo_Pais, Ciudad,
												Competicion, Codigo_Competicion, Temporadas, Fundacion, Entrenador, Codigo_Entrenador,
												Presidente, Codigo_Presidente)
						VALUES('atletico-madrid', 'Club Atletico de Madrid', 'Atletico', 'ATM', 369, 94, 'España', 'es', 'Madrid',
								'Primera', 'primera', 88, 1903, 'Cholo Simeone', 13, 'Cerezo', 27257)""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('20190622', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Codigo_Estadio, Nombre, Direccion, Latitud, Longitud, Ciudad,
												Capacidad, Fecha, Largo, Ancho, Telefono, Cesped, Pais, Codigo_Pais)
						VALUES('metropolitano', 23, 'Metropolitano', 'Av Luis Aragones', 40.436, -3.599, 'Madrid', 100000,
								2017, 105, 68, 'Telefono', 'Cedped', 'España', 'es')""")

	conexion.c.execute("""INSERT INTO partido_estadio
						VALUES('20190622', 'metropolitano')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano')""")

	conexion.c.execute("""INSERT INTO competiciones
						VALUES('primera', 'Primera', 'primera-division-ea', 'es')""")

	conexion.c.execute("""INSERT INTO partido_competicion
						VALUES('20190622', 'primera')""")

	conexion.c.execute("""INSERT INTO competiciones_campeones
						VALUES('primera', 2025, 'atletico-madrid'), ('primera', 2024, 'atletico-madrid')""")

	conexion.c.execute("""INSERT INTO jugadores
						VALUES('julian-alvarez', 'Julian', 'atletico-madrid', 'ar', '1324', 100, 100.0, 9, 'DC')""")

	conexion.c.execute("""INSERT INTO jugadores_equipo
						VALUES('julian-alvarez', 'atletico-madrid', 1, 1, 1)""")

	conexion.c.execute("""INSERT INTO jugadores_seleccion
						VALUES('julian-alvarez', 1, 1, 1, 1)""")

	conexion.c.execute("""INSERT INTO partido_goleador
						VALUES('20190622', 'julian-alvarez', 1, 0, True),
								('20190622', 'julian-alvarez', 2, 0, False)""")

	conexion.c.execute("""INSERT INTO proximos_partidos
						VALUES('20200622', 'atletico-madrid', 'atletico-madrid', '2020-06-22', '22:00', 'Liga')""")

	conexion.c.execute("""INSERT INTO entrenadores
						VALUES('diego-pablo', 'Diego Simeone', 'atletico-madrid', 'ar', '13', 100)""")

	conexion.confirmar()

	return conexion

@pytest.fixture()
def conexion_entorno_usuario(conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	return conexion_entorno

@pytest.fixture()
def datalake():

    return ConexionDataLake()

def pytest_sessionstart(session):

	entorno=config["development"].ENVIROMENT

	dl=ConexionDataLake()

	if not dl.existe_contenedor(entorno):

		dl.crearContenedor(entorno)

	if not dl.existe_carpeta(entorno, "usuarios"):

		dl.crearCarpeta(entorno, "usuarios")

	else:

		dl.eliminarCarpeta(entorno, "usuarios")

		dl.crearCarpeta(entorno, "usuarios")

	dl.cerrarConexion()

	print(f"\nEntorno del DataLake de {entorno} creado")

def pytest_sessionfinish(session, exitstatus):

	entorno=config["development"].ENVIROMENT

	con=Conexion(entorno)

	con.vaciarBBDD()

	con.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES ('atletico-madrid')""")

	con.confirmar()

	con.cerrarConexion()

	print("\nLimpieza de la BBDD correcta")

	ruta_carpeta_mapas_estadios=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

	ruta_carpeta_mapas_trayectos=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "trayectos")

	ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

	vaciarCarpeta(ruta_carpeta_mapas_estadios)

	vaciarCarpeta(ruta_carpeta_mapas_trayectos)

	print("\nLimpieza de la carpeta mapas correcta")

	vaciarCarpeta(ruta_carpeta_imagenes)

	print("\nLimpieza de la carpeta imagenes correcta")

	dl=ConexionDataLake()

	if dl.existe_carpeta(entorno, "usuarios"):

		dl.eliminarCarpeta(entorno, "usuarios")

	dl.crearCarpeta(entorno, "usuarios")

	dl.cerrarConexion()

	print("\nLimpieza del DataLake correcta")