from flask import Blueprint, render_template, redirect, request, jsonify, current_app
from flask_login import login_required, current_user
import os
import time
import pandas as pd
pd.set_option('display.max_columns', None)

from src.database.conexion import Conexion

from src.utilidades.utils import crearCarpeta, extraerExtension, comprobarFechas, ciudad_estadio_correcta
from src.utilidades.utils import existen_paradas, obtenerParadas, obtenerDataframeDireccion, obtenerDataframeDireccionParadas
from src.utilidades.utils import validarDataFramesTrayectosCorrectos, validarDataFrameDuplicados
from src.utilidades.configutils import TRANSPORTES

from src.datalake.conexion_data_lake import ConexionDataLake

from src.config import CONTENEDOR

from src.kafka.kafka_utils import enviarMensajeKafka

from src.kafka.configkafka import TOPIC

bp_anadir_partido_asistido=Blueprint("anadir_partido_asistido", __name__)


@bp_anadir_partido_asistido.route("/anadir_partido_asistido")
@login_required
def pagina_anadir_partido_asistido():

	entorno=current_app.config["ENVIROMENT"]

	todos=request.args.get("todos", default=False, type=bool)
	partido_id_anadir=request.args.get("partido_id", default=None)

	con=Conexion(entorno)

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

	entorno=current_app.config["ENVIROMENT"]

	partido_id=request.args.get("partido_id")

	if not partido_id:

		return jsonify({"error": "No se especifico el partido"}), 400

	con=Conexion(entorno)

	fecha_partido=con.obtenerFechaPartido(partido_id)

	con.cerrarConexion()

	return jsonify({"fecha_ida": fecha_partido}) if fecha_partido else jsonify({"error": "Partido no encontrado"}), 404

@bp_anadir_partido_asistido.route("/ciudades_pais_trayectos")
def obtenerCiudadesPais():

	entorno=current_app.config["ENVIROMENT"]

	pais=request.args.get("pais")

	if not pais:
		return jsonify({"error": "No se especificó el pais"}), 400

	con=Conexion(entorno)

	ciudades=con.obtenerCiudadesPais(pais, 50000)

	con.cerrarConexion()

	return jsonify(ciudades) if ciudades else jsonify({"error": "Pais no encontrado"}), 404

@bp_anadir_partido_asistido.route("/estadio_partido")
def obtenerEstadioPartido():

	entorno=current_app.config["ENVIROMENT"]

	partido_id=request.args.get("partido_id")

	if not partido_id:
		return jsonify({"error": "No se especificó el partido"}), 400

	con=Conexion(entorno)

	estadio_partido=con.obtenerEstadioPartido(partido_id)

	con.cerrarConexion()

	return jsonify({"estadio": estadio_partido}) if estadio_partido else jsonify({"error": "Partido no encontrado"}), 404
		
@bp_anadir_partido_asistido.route("/insertar_partido_asistido", methods=["POST"])
@login_required
def pagina_insertar_partido_asistido():

	entorno=current_app.config["ENVIROMENT"]

	partido_id=request.form.get("partido_anadir")
	comentario=request.form.get("comentario")
	partido_asistido_favorito=request.form.get("partido-favorito")
	archivos=request.files

	fecha_ida=request.form.get("fecha-ida")
	ciudad_ida=request.form.get("ciudad-ida")
	pais_ida=request.form.get("pais-ida")
	ciudad_ida_estadio=request.form.get("ciudad-ida-estadio")
	transporte_ida=request.form.get("transporte-ida")

	fecha_vuelta=request.form.get("fecha-vuelta")
	ciudad_vuelta=request.form.get("ciudad-vuelta")
	pais_vuelta=request.form.get("pais-vuelta")
	ciudad_vuelta_estadio=request.form.get("ciudad-vuelta-estadio")
	transporte_vuelta=request.form.get("transporte-vuelta")

	transportes_paradas_ida=request.form.getlist("transporte-parada-ida[]")
	paises_paradas_ida=request.form.getlist("pais-parada-ida[]")
	ciudades_paradas_ida=request.form.getlist("ciudad-parada-ida[]")

	transportes_paradas_vuelta=request.form.getlist("transporte-parada-vuelta[]")
	paises_paradas_vuelta=request.form.getlist("pais-parada-vuelta[]")
	ciudades_paradas_vuelta=request.form.getlist("ciudad-parada-vuelta[]")
	
	teletrabajo_str=request.form.get("teletrabajo", default="False")
	teletrabajo=teletrabajo_str in ("True", "on", "yes", True)

	con=Conexion(entorno)

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	if con.existe_partido_asistido(partido_id, current_user.id):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	if comentario and len(comentario)>255:
		
		con.cerrarConexion()

		return redirect(f"/anadir_partido_asistido?partido_id={partido_id}&todos=True")

	fecha_partido=con.obtenerFechaPartido(partido_id)

	if comprobarFechas(fecha_ida, fecha_vuelta, fecha_partido):

		estadio_partido=con.obtenerEstadioPartido(partido_id)

		if not estadio_partido:

			con.cerrarConexion()

			return redirect(f"/anadir_partido_asistido?partido_id={partido_id}&todos=True")

		ciudad_estadio, pais_estadio=estadio_partido[0], estadio_partido[2]

		if not ciudad_estadio_correcta(ciudad_ida_estadio, ciudad_vuelta_estadio, ciudad_estadio):

			con.cerrarConexion()

			return redirect(f"/anadir_partido_asistido?partido_id={partido_id}&todos=True")

		else:

			existen_paradas_ida=existen_paradas(transportes_paradas_ida, paises_paradas_ida, ciudades_paradas_ida)

			existen_paradas_vuelta=existen_paradas(transportes_paradas_vuelta, paises_paradas_vuelta, ciudades_paradas_vuelta)

			if existen_paradas_ida or existen_paradas_vuelta:

				paradas_ida=obtenerParadas(transportes_paradas_ida, paises_paradas_ida, ciudades_paradas_ida)

				paradas_vuelta=obtenerParadas(transportes_paradas_vuelta, paises_paradas_vuelta, ciudades_paradas_vuelta)

				if not paradas_ida and not paradas_vuelta:

					con.cerrarConexion()

					return redirect(f"/anadir_partido_asistido?partido_id={partido_id}&todos=True")

				if paradas_ida and not paradas_vuelta:

					df_ida_final=obtenerDataframeDireccionParadas(ciudad_ida, pais_ida, ciudad_estadio, pais_estadio, transporte_ida, paradas_ida, partido_id, current_user.id, "I", entorno)

					df_vuelta_final=obtenerDataframeDireccion(ciudad_estadio, pais_estadio, ciudad_vuelta, pais_vuelta, transporte_vuelta, partido_id, current_user.id, "V", entorno)

					if not validarDataFramesTrayectosCorrectos(df_ida_final, df_vuelta_final) or not validarDataFrameDuplicados(df_ida_final):

						con.cerrarConexion()

						return redirect(f"/anadir_partido_asistido?partido_id={partido_id}&todos=True")

					else:

						con.insertarPartidoAsistido(partido_id, current_user.id, comentario)

						con.actualizarDatosOnTourPartidoAsistido(partido_id, current_user.id, fecha_ida, fecha_vuelta, teletrabajo)

						df_trayectos=pd.concat([df_ida_final, df_vuelta_final], ignore_index=True)

						con.insertarTrayectosPartidoAsistido(df_trayectos)

				elif not paradas_ida and paradas_vuelta:

					df_ida_final=obtenerDataframeDireccion(ciudad_ida, pais_ida, ciudad_estadio, pais_estadio, transporte_ida, partido_id, current_user.id, "I", entorno)

					df_vuelta_final=obtenerDataframeDireccionParadas(ciudad_estadio, pais_estadio, ciudad_vuelta, pais_vuelta, transporte_vuelta, paradas_vuelta, partido_id, current_user.id, "V", entorno)
					
					if not validarDataFramesTrayectosCorrectos(df_ida_final, df_vuelta_final) or not validarDataFrameDuplicados(df_vuelta_final):

						con.cerrarConexion()

						return redirect(f"/anadir_partido_asistido?partido_id={partido_id}&todos=True")

					else:

						con.insertarPartidoAsistido(partido_id, current_user.id, comentario)

						con.actualizarDatosOnTourPartidoAsistido(partido_id, current_user.id, fecha_ida, fecha_vuelta, teletrabajo)

						df_trayectos=pd.concat([df_ida_final, df_vuelta_final], ignore_index=True)

						con.insertarTrayectosPartidoAsistido(df_trayectos)

				else:

					df_ida_final=obtenerDataframeDireccionParadas(ciudad_ida, pais_ida, ciudad_estadio, pais_estadio, transporte_ida, paradas_ida, partido_id, current_user.id, "I", entorno)

					df_vuelta_final=obtenerDataframeDireccionParadas(ciudad_estadio, pais_estadio, ciudad_vuelta, pais_vuelta, transporte_vuelta, paradas_vuelta, partido_id, current_user.id, "V", entorno)

					if not validarDataFramesTrayectosCorrectos(df_ida_final, df_vuelta_final) or not validarDataFrameDuplicados(df_ida_final) or not validarDataFrameDuplicados(df_vuelta_final):

						con.cerrarConexion()

						return redirect(f"/anadir_partido_asistido?partido_id={partido_id}&todos=True")

					else:

						con.insertarPartidoAsistido(partido_id, current_user.id, comentario)

						con.actualizarDatosOnTourPartidoAsistido(partido_id, current_user.id, fecha_ida, fecha_vuelta, teletrabajo)

						df_trayectos=pd.concat([df_ida_final, df_vuelta_final], ignore_index=True)

						con.insertarTrayectosPartidoAsistido(df_trayectos)

			else:

				df_ida_final=obtenerDataframeDireccion(ciudad_ida, pais_ida, ciudad_estadio, pais_estadio, transporte_ida, partido_id, current_user.id, "I", entorno)

				df_vuelta_final=obtenerDataframeDireccion(ciudad_estadio, pais_estadio, ciudad_vuelta, pais_vuelta, transporte_vuelta, partido_id, current_user.id, "V", entorno)

				if not validarDataFramesTrayectosCorrectos(df_ida_final, df_vuelta_final):

					con.cerrarConexion()

					return redirect(f"/anadir_partido_asistido?partido_id={partido_id}&todos=True")

				else:

					con.insertarPartidoAsistido(partido_id, current_user.id, comentario)

					con.actualizarDatosOnTourPartidoAsistido(partido_id, current_user.id, fecha_ida, fecha_vuelta, teletrabajo)

					df_trayectos=pd.concat([df_ida_final, df_vuelta_final], ignore_index=True)

					con.insertarTrayectosPartidoAsistido(df_trayectos)
					
	else:

		con.insertarPartidoAsistido(partido_id, current_user.id, comentario)

	existe_partido_asistido_favorito=False if not con.obtenerPartidoAsistidoFavorito(current_user.id) else True

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "templates", "imagenes", current_user.id))

	if not existe_partido_asistido_favorito and partido_asistido_favorito:

		con.insertarPartidoAsistidoFavorito(partido_id, current_user.id)

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

	return redirect("/partidos/asistidos")

@bp_anadir_partido_asistido.route("/actualizar_comentario_partido_asistido/<partido_id>", methods=["POST"])
@login_required
def pagina_actualizar_comentario_partido_asistido(partido_id:str):

	entorno=current_app.config["ENVIROMENT"]

	nuevo_comentario=request.form.get("nuevo-comentario")

	con=Conexion(entorno)

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

	entorno=current_app.config["ENVIROMENT"]

	archivos=request.files

	con=Conexion(entorno)

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