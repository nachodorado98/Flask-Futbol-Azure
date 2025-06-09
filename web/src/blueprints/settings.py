from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.kafka.kafka_utils import enviarMensajeKafka

from src.kafka.configkafka import TOPIC


bp_settings=Blueprint("settings", __name__)


@bp_settings.route("/settings")
@login_required
def settings():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	con.cerrarConexion()

	return render_template("settings.html",
							usuario=current_user.id,
							equipo=equipo,
							estadio_equipo=estadio_equipo)

@bp_settings.route("/settings/eliminar_cuenta")
@login_required
def pagina_eliminar_cuenta():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	con.eliminarUsuario(current_user.id)

	con.cerrarConexion()

	try:

		mensaje_eliminar_carpeta={"categoria":"datalake_eliminar_carpeta", "usuario":current_user.id, "entorno":entorno}

		enviarMensajeKafka(TOPIC, mensaje_eliminar_carpeta)

	except Exception as e:

		print(f"Error en conexion con kafka: {e}")

	return redirect("/")