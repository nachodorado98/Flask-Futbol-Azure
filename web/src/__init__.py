from flask import Flask

from .blueprints.inicio import bp_inicio
from .blueprints.registro import bp_registro
from .blueprints.login import bp_login
from .blueprints.partidos import bp_partidos
from .blueprints.partido import bp_partido
from .blueprints.equipo import bp_equipo
from .blueprints.estadio import bp_estadio

from .extensiones.manager import login_manager

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

	return app