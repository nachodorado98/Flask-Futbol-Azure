from flask import Blueprint, render_template, redirect, request, jsonify
from flask_login import login_required, current_user
import os
import time

from src.database.conexion import Conexion

from src.utilidades.utils import crearCarpeta, extraerExtension, comprobarFechas, trayecto_correcto, ciudad_estadio_correcta
from src.utilidades.configutils import TRANSPORTES

from src.datalake.conexion_data_lake import ConexionDataLake

from src.config import CONTENEDOR

from src.kafka.kafka_utils import enviarMensajeKafka

from src.kafka.configkafka import TOPIC

bp_anadir_partido_asistido=Blueprint("anadir_partido_asistido", __name__)


@bp_anadir_partido_asistido.route("/anadir_partido_asistido")
@login_required
def pagina_anadir_partido_asistido():

	todos=request.args.get("todos", default=False, type=bool)
	partido_id_anadir=request.args.get("partido_id", default=None)

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	if todos:

		partidos_no_asistidos=con.obtenerPartidosNoAsistidosUsuario(current_user.id, equipo)

	else:

		partidos_no_asistidos=con.obtenerPartidosNoAsistidosUsuarioRecientes(current_user.id, equipo)

	if not partidos_no_asistidos:

		con.cerrarConexion()

		return render_template("anadir_no_partido_asistido.html",
								usuario=current_user.id,
								equipo=equipo,
								estadio_equipo=estadio_equipo)

	existe_partido_asistido_favorito=False if not con.obtenerPartidoAsistidoFavorito(current_user.id) else True

	fecha_partido=con.obtenerFechaPartido(partido_id_anadir) if partido_id_anadir else None

	paises=con.obtenerPaises()

	pais_usuario, ciudad_usuario=con.obtenerPaisCiudadUsuario(current_user.id)

	estadio_partido=con.obtenerEstadioPartido(partido_id_anadir) if partido_id_anadir else None

	con.cerrarConexion()

	return render_template("anadir_partido_asistido.html",
							usuario=current_user.id,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							partidos_no_asistidos=partidos_no_asistidos,
							todos=todos,
							partido_id_anadir=partido_id_anadir,
							existe_partido_asistido_favorito=existe_partido_asistido_favorito,
							fecha_partido=fecha_partido,
							paises=paises,
							pais_usuario=pais_usuario,
							ciudad_usuario=ciudad_usuario,
							estadio_partido=estadio_partido,
							transportes=TRANSPORTES)

@bp_anadir_partido_asistido.route("/fecha_partido")
def obtenerFechaPartido():

	partido_id=request.args.get("partido_id")

	if not partido_id:

		return jsonify({"error": "No se especifico el partido"}), 400

	con=Conexion()

	fecha_partido=con.obtenerFechaPartido(partido_id)

	con.cerrarConexion()

	return jsonify({"fecha_ida": fecha_partido}) if fecha_partido else jsonify({"error": "Partido no encontrado"}), 404

@bp_anadir_partido_asistido.route("/ciudades_pais_trayectos")
def obtenerCiudadesPais():

	pais=request.args.get("pais")

	if not pais:
		return jsonify({"error": "No se especificó el pais"}), 400

	con=Conexion()

	ciudades=con.obtenerCiudadesPais(pais, 50000)

	con.cerrarConexion()

	return jsonify(ciudades) if ciudades else jsonify({"error": "Pais no encontrado"}), 404

@bp_anadir_partido_asistido.route("/estadio_partido")
def obtenerEstadioPartido():

	partido_id=request.args.get("partido_id")

	if not partido_id:
		return jsonify({"error": "No se especificó el partido"}), 400

	con=Conexion()

	estadio_partido=con.obtenerEstadioPartido(partido_id)

	con.cerrarConexion()

	return jsonify({"estadio": estadio_partido}) if estadio_partido else jsonify({"error": "Partido no encontrado"}), 404
		
@bp_anadir_partido_asistido.route("/insertar_partido_asistido", methods=["POST"])
@login_required
def pagina_insertar_partido_asistido():

	partido_id=request.form.get("partido_anadir")
	comentario=request.form.get("comentario")
	partido_asistido_favorito=request.form.get("partido-favorito")
	archivos=request.files

	ciudad_ida=request.form.get("ciudad-ida")
	pais_ida=request.form.get("pais-ida")
	ciudad_ida_estadio=request.form.get("ciudad-ida-estadio")
	fecha_ida=request.form.get("fecha-ida")
	transporte_ida=request.form.get("transporte-ida")

	ciudad_vuelta=request.form.get("ciudad-vuelta")
	pais_vuelta=request.form.get("pais-vuelta")
	ciudad_vuelta_estadio=request.form.get("ciudad-vuelta-estadio")
	fecha_vuelta=request.form.get("fecha-vuelta")
	transporte_vuelta=request.form.get("transporte-vuelta")
	
	teletrabajo=request.form.get("teletrabajo", default=False, type=bool)

	con=Conexion()

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	if con.existe_partido_asistido(partido_id, current_user.id):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	if comentario and len(comentario)>255:
		
		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	con.insertarPartidoAsistido(partido_id, current_user.id, comentario)

	existe_partido_asistido_favorito=False if not con.obtenerPartidoAsistidoFavorito(current_user.id) else True

	if not existe_partido_asistido_favorito and partido_asistido_favorito:

		con.insertarPartidoAsistidoFavorito(partido_id, current_user.id)

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "templates", "imagenes", current_user.id))

	if "imagen" in archivos:

		imagen=archivos["imagen"]

		extension=extraerExtension(imagen.filename)

		if imagen.filename!="" and extension in ("png", "jpg", "jpeg"):

			ruta_carpeta=os.path.join(ruta, "templates", "imagenes", current_user.id)

			archivo_imagen=f"{current_user.id}_{partido_id}.{extension}"

			ruta_imagen=os.path.join(ruta_carpeta, archivo_imagen)

			imagen.save(ruta_imagen)

			try:

				dl=ConexionDataLake()

				if not dl.existe_carpeta(CONTENEDOR, f"usuarios/{current_user.id}"):

					mensaje_datalake={"categoria":"datalake_usuario", "usuario":current_user.id}

					enviarMensajeKafka(TOPIC, mensaje_datalake)

					time.sleep(10)

				dl.subirArchivo(CONTENEDOR, f"usuarios/{current_user.id}/imagenes", ruta_carpeta, archivo_imagen)

				dl.cerrarConexion()

				con.actualizarImagenPartidoAsistido(partido_id, current_user.id, archivo_imagen)

				os.remove(ruta_imagen)

			except Exception:

				print(f"Error al subir imagen {archivo_imagen} al datalake")

	fecha_partido=con.obtenerFechaPartido(partido_id)

	if comprobarFechas(fecha_ida, fecha_vuelta, fecha_partido):

		con.actualizarDatosOnTourPartidoAsistido(partido_id, current_user.id, fecha_ida, fecha_vuelta, teletrabajo)

		estadio_partido=con.obtenerEstadioPartido(partido_id)

		if not estadio_partido:

			con.cerrarConexion()

			return redirect("/partidos/asistidos")

		ciudad_estadio, pais_estadio=estadio_partido[0], estadio_partido[2]

		if ciudad_estadio_correcta(ciudad_ida_estadio, ciudad_vuelta_estadio, ciudad_estadio):

			codigo_ciudad_estadio=con.obtenerCodigoCiudadPais(ciudad_estadio, pais_estadio)

			codigo_ciudad_ida=con.obtenerCodigoCiudadPais(ciudad_ida, pais_ida)

			codigo_ciudad_vuelta=con.obtenerCodigoCiudadPais(ciudad_vuelta, pais_vuelta)

			ida_correcta=trayecto_correcto(codigo_ciudad_ida, codigo_ciudad_estadio, transporte_ida)

			vuelta_correcta=trayecto_correcto(codigo_ciudad_vuelta, codigo_ciudad_estadio, transporte_vuelta)

			if ida_correcta and vuelta_correcta:

				trayecto_id=f"id_{partido_id}_{current_user.id}"

				con.insertarTrayectoPartidoAsistido(f"{trayecto_id}_I", partido_id, current_user.id, "I", codigo_ciudad_ida, transporte_ida, codigo_ciudad_estadio)

				con.insertarTrayectoPartidoAsistido(f"{trayecto_id}_V", partido_id, current_user.id, "V", codigo_ciudad_estadio, transporte_vuelta, codigo_ciudad_vuelta)

	con.cerrarConexion()

	return redirect("/partidos/asistidos")

@bp_anadir_partido_asistido.route("/actualizar_comentario_partido_asistido/<partido_id>", methods=["POST"])
@login_required
def pagina_actualizar_comentario_partido_asistido(partido_id:str):

	nuevo_comentario=request.form.get("nuevo-comentario")

	con=Conexion()

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	if not con.existe_partido_asistido(partido_id, current_user.id):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	if nuevo_comentario and len(nuevo_comentario)>255:
		
		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	con.actualizarComentarioPartidoAsistido(partido_id, current_user.id, nuevo_comentario)

	con.cerrarConexion()

	return redirect(f"/partido/{partido_id}/asistido")

@bp_anadir_partido_asistido.route("/actualizar_imagen_partido_asistido/<partido_id>", methods=["POST"])
@login_required
def pagina_actualizar_imagen_partido_asistido(partido_id:str):

	archivos=request.files

	con=Conexion()

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	if not con.existe_partido_asistido(partido_id, current_user.id):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "templates", "imagenes", current_user.id))

	if "imagen" in archivos:

		imagen=archivos["imagen"]

		extension=extraerExtension(imagen.filename)

		if imagen.filename!="" and extension in ("png", "jpg", "jpeg"):

			ruta_carpeta=os.path.join(ruta, "templates", "imagenes", current_user.id)

			archivo_imagen=f"{current_user.id}_{partido_id}.{extension}"

			ruta_imagen=os.path.join(ruta_carpeta, archivo_imagen)

			imagen.save(ruta_imagen)

			try:

				dl=ConexionDataLake()

				if not dl.existe_carpeta(CONTENEDOR, f"usuarios/{current_user.id}"):

					mensaje_datalake={"categoria":"datalake_usuario", "usuario":current_user.id}

					enviarMensajeKafka(TOPIC, mensaje_datalake)

					time.sleep(10)

				dl.subirArchivo(CONTENEDOR, f"usuarios/{current_user.id}/imagenes", ruta_carpeta, archivo_imagen)

				dl.cerrarConexion()

				con.actualizarImagenPartidoAsistido(partido_id, current_user.id, archivo_imagen)

				os.remove(ruta_imagen)

			except Exception:

				print(f"Error al subir imagen {archivo_imagen} al datalake")

	con.cerrarConexion()

	return redirect(f"/partido/{partido_id}/asistido")