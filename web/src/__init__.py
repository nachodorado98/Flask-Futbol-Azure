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

from .extensiones.manager import login_manager

from .utilidades.utils import crearCarpeta

# Funcion para crear el entorno
def creacionEntorno()->None:

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "src", "templates", "mapas"))

	crearCarpeta(os.path.join(ruta, "src", "templates", "imagenes"))

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

	creacionEntorno()

	return app