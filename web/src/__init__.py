from flask import Flask
import os

from .blueprints.inicio import bp_inicio
from .blueprints.registro import bp_registro
from .blueprints.login import bp_login
from .blueprints.partidos import bp_partidos
from .blueprints.partido import bp_partido
from .blueprints.equipo import bp_equipo
from .blueprints.estadio import bp_estadio
from .blueprints.competicion import bp_competicion
from .blueprints.jugador import bp_jugador
from .blueprints.anadir_partido_asistido import bp_anadir_partido_asistido
from .blueprints.entrenador import bp_entrenador
from .blueprints.settings import bp_settings

from .extensiones.manager import login_manager

from .utilidades.utils import crearCarpeta

from .datalake.conexion_data_lake import ConexionDataLake

from .config import CARPETAS

# Funcion para crear el entorno
def creacionEntorno(entorno:str)->None:

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "src", "templates", "mapas"))
	crearCarpeta(os.path.join(ruta, "src", "templates", "mapas", "estadios"))
	crearCarpeta(os.path.join(ruta, "src", "templates", "mapas", "trayectos"))
	crearCarpeta(os.path.join(ruta, "src", "templates", "imagenes"))
	crearCarpeta(os.path.join(ruta, "src", "templates", "imagenes", "partidos"))
	crearCarpeta(os.path.join(ruta, "src", "templates", "imagenes", "perfil"))

	dl=ConexionDataLake()

	if not dl.existe_contenedor(entorno):

		dl.crearContenedor(entorno)

		for carpeta in CARPETAS:

			if not dl.existe_carpeta(entorno, carpeta):

				dl.crearCarpeta(entorno, carpeta)

	dl.cerrarConexion()

# Funcion para crear la instancia de la aplicacion
def crear_app(configuracion:object)->Flask:

	app=Flask(__name__, template_folder="templates")

	app.config.from_object(configuracion)

	login_manager.init_app(app)
	login_manager.login_view="login.login"

	app.register_blueprint(bp_inicio)
	app.register_blueprint(bp_registro)
	app.register_blueprint(bp_login)
	app.register_blueprint(bp_partidos)
	app.register_blueprint(bp_partido)
	app.register_blueprint(bp_equipo)
	app.register_blueprint(bp_estadio)
	app.register_blueprint(bp_competicion)
	app.register_blueprint(bp_jugador)
	app.register_blueprint(bp_anadir_partido_asistido)
	app.register_blueprint(bp_entrenador)
	app.register_blueprint(bp_settings)

	entorno=app.config["ENVIROMENT"]

	creacionEntorno(entorno)

	return app