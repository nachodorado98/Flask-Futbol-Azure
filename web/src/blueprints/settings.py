from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, current_user
import os

from src.database.conexion import Conexion

from src.kafka.kafka_utils import enviarMensajeKafka

from src.kafka.configkafka import TOPIC

from src.config import URL_DATALAKE_USUARIOS

from src.utilidades.utils import crearCarpeta, extraerExtension

from src.datalake.conexion_data_lake import ConexionDataLake


bp_settings=Blueprint("settings", __name__)


@bp_settings.route("/settings")
@login_required
def settings():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	imagen_perfil=con.obtenerImagenPerfilUsuario(current_user.id)

	con.cerrarConexion()

	return render_template("settings.html",
							usuario=current_user.id,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							imagen_perfil=imagen_perfil,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

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

@bp_settings.route("/settings/actualizar_imagen_perfil", methods=["POST"])
@login_required
def pagina_subir_imagen_perfil():

	entorno=current_app.config["ENVIROMENT"]

	archivos=request.files

	con=Conexion(entorno)

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "templates", "imagenes", "perfil", current_user.id))

	if "imagen" in archivos:

		imagen=archivos["imagen"]

		extension=extraerExtension(imagen.filename)

		if imagen.filename!="" and extension in ("png", "jpg", "jpeg"):

			ruta_carpeta=os.path.join(ruta, "templates", "imagenes", "perfil", current_user.id,)

			archivo_imagen=f"{current_user.id}_perfil.{extension}"

			ruta_imagen=os.path.join(ruta_carpeta, archivo_imagen)

			imagen.save(ruta_imagen)

			try:

				dl=ConexionDataLake()

				if not dl.existe_carpeta(entorno, f"usuarios/{current_user.id}"):

					mensaje_datalake={"categoria":"datalake_usuario", "usuario":current_user.id, "entorno":entorno}

					enviarMensajeKafka(TOPIC, mensaje_datalake)

					time.sleep(10)

				dl.subirArchivo(entorno, f"usuarios/{current_user.id}/perfil", ruta_carpeta, archivo_imagen)

				dl.cerrarConexion()

				con.actualizarImagenPerfilUsuario(current_user.id, archivo_imagen)

				os.remove(ruta_imagen)

			except Exception:

				print(f"Error al subir imagen {archivo_imagen} al datalake")

	con.cerrarConexion()

	return redirect("/settings")