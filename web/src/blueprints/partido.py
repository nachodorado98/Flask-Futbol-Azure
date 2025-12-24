from flask import Blueprint, render_template, redirect, send_file, current_app
from flask_login import login_required, current_user
import os

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_JUGADORES, URL_DATALAKE_USUARIOS
from src.config import URL_DATALAKE_ENTRENADORES

from src.utilidades.utils import vaciarCarpetaMapasUsuario, crearMapaTrayecto, crearMapaTrayectosIdaVuelta, obtenerTrayectosConDistancia
from src.utilidades.utils import obtenerDistanciaTotalTrayecto, es_numero, obtenerNumeroDias

from src.kafka.kafka_utils import enviarMensajeKafka

from src.kafka.configkafka import TOPIC


bp_partido=Blueprint("partido", __name__)


@bp_partido.route("/partido/<partido_id>")
@login_required
def pagina_partido(partido_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	equipo_partido=True if con.equipo_partido(equipo, partido_id) else False

	estadio_equipo=con.estadio_equipo(equipo)

	partido=con.obtenerPartido(partido_id)

	partido_id_anterior=con.obtenerPartidoAnterior(partido_id, equipo)

	partido_id_siguiente=con.obtenerPartidoSiguiente(partido_id, equipo)

	goleadores=con.obtenerGoleadoresPartido(partido_id)

	partidos_entre_equipos=con.obtenerPartidosEntreEquipos(partido[4], partido[7], 3)

	historial_entre_equipos=con.obtenerPartidosHistorialEntreEquipos(partido[4], partido[7])

	partido_asistido=con.existe_partido_asistido(partido_id, current_user.id)

	entrenadores_partido=con.obtenerEntrenadoresPartido(partido_id)

	jugadores_local_partido=con.obtenerJugadoresEquipoPartido(partido_id, True)

	jugadores_visitante_partido=con.obtenerJugadoresEquipoPartido(partido_id, False)

	con.cerrarConexion()

	return render_template("partido.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							partido=partido,
							partido_id=partido_id,
							partido_id_anterior=partido_id_anterior,
							partido_id_siguiente=partido_id_siguiente,
							goleadores=goleadores,
							partidos_entre_equipos=partidos_entre_equipos,
							historial_entre_equipos=historial_entre_equipos,
							partido_asistido=partido_asistido,
							equipo_partido=equipo_partido,
							entrenadores_partido=entrenadores_partido,
							jugadores_local_partido=jugadores_local_partido,
							jugadores_visitante_partido=jugadores_visitante_partido,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_jugador=URL_DATALAKE_JUGADORES,
							url_imagen_entrenador=URL_DATALAKE_ENTRENADORES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_partido.route("/partido/<partido_id>/asistido")
@login_required
def pagina_partido_asistido(partido_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	if not con.equipo_partido(equipo, partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	if not con.existe_partido_asistido(partido_id, current_user.id):

		con.cerrarConexion()

		return redirect("/partidos")

	estadio_equipo=con.estadio_equipo(equipo)

	partido_asistido=con.obtenerPartidoAsistidoUsuario(current_user.id, partido_id)

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	vaciarCarpetaMapasUsuario(os.path.join(ruta, "templates", "mapas", "trayectos"), current_user.id)

	trayecto_ida=con.obtenerTrayectoPartidoAsistido(partido_id, current_user.id, "I")

	trayecto_vuelta=con.obtenerTrayectoPartidoAsistido(partido_id, current_user.id, "V")

	nombre_mapa_ida=f"mapa_trayecto_ida_user_{current_user.id}.html"

	nombre_mapa_vuelta=f"mapa_trayecto_vuelta_user_{current_user.id}.html"

	nombre_mapa_ida_vuelta=f"mapa_trayecto_ida_vuelta_user_{current_user.id}.html"

	mapas_correcto=True

	try:

		crearMapaTrayecto(os.path.join(ruta, "templates", "mapas", "trayectos"), trayecto_ida, nombre_mapa_ida)

		crearMapaTrayecto(os.path.join(ruta, "templates", "mapas", "trayectos"), trayecto_vuelta, nombre_mapa_vuelta)

		crearMapaTrayectosIdaVuelta(os.path.join(ruta, "templates", "mapas", "trayectos"), [trayecto_ida, trayecto_vuelta], nombre_mapa_ida_vuelta)

	except Exception as e:

		print(f"Error en los mapas del trayecto: {e}")
		mapas_correcto=False

	partido_id_asistido_anterior=con.obtenerPartidoAsistidoUsuarioAnterior(current_user.id, partido_id)

	partido_id_asistido_siguiente=con.obtenerPartidoAsistidoUsuarioSiguiente(current_user.id, partido_id)

	id_partido_asistido_favorito=con.obtenerPartidoAsistidoFavorito(current_user.id)

	partido_asistido_favorito=True if id_partido_asistido_favorito==partido_id else False

	trayectos_ida_base=con.obtenerTrayectosPartidoAsistido(partido_id, current_user.id, "I")

	trayectos_vuelta_base=con.obtenerTrayectosPartidoAsistido(partido_id, current_user.id, "V")

	trayectos_ida=obtenerTrayectosConDistancia(trayectos_ida_base)

	trayectos_vuelta=obtenerTrayectosConDistancia(trayectos_vuelta_base)

	distancia_total_ida=obtenerDistanciaTotalTrayecto(trayectos_ida)

	distancia_total_vuelta=obtenerDistanciaTotalTrayecto(trayectos_vuelta)

	con.cerrarConexion()

	return render_template("partido_asistido.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							partido_asistido=partido_asistido,
							partido_id=partido_id,
							partido_asistido_favorito=partido_asistido_favorito,
							partido_id_asistido_anterior=partido_id_asistido_anterior,
							partido_id_asistido_siguiente=partido_id_asistido_siguiente,
							mapas_correcto=mapas_correcto,
							nombre_mapa_ida=nombre_mapa_ida,
							nombre_mapa_vuelta=nombre_mapa_vuelta,
							nombre_mapa_ida_vuelta=nombre_mapa_ida_vuelta,
							trayectos_ida=trayectos_ida,
							distancia_total_ida=distancia_total_ida,
							trayectos_vuelta=trayectos_vuelta,
							distancia_total_vuelta=distancia_total_vuelta,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_usuario_imagenes=f"{URL_DATALAKE_USUARIOS}{current_user.id}/imagenes/",
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_partido.route("/partido/<partido_id>/asistido/trayecto/mapa/<nombre_mapa>")
@login_required
def visualizarMapaTrayecto(partido_id:str, nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "mapas", "trayectos", nombre_mapa)

	return send_file(ruta_mapa)

@bp_partido.route("/partido/<partido_id>/asistido/quitar_partido_favorito")
@login_required
def pagina_quitar_partido_asistido_favorito(partido_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	if not con.equipo_partido(equipo, partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	if not con.existe_partido_asistido(partido_id, current_user.id):

		con.cerrarConexion()

		return redirect("/partidos")

	estadio_equipo=con.estadio_equipo(equipo)

	id_partido_favorito=con.obtenerPartidoAsistidoFavorito(current_user.id)

	if id_partido_favorito==partido_id:

		con.eliminarPartidoAsistidoFavorito(partido_id, current_user.id)

	con.cerrarConexion()

	return redirect(f"/partido/{partido_id}/asistido")

@bp_partido.route("/partido/<partido_id>/asistido/anadir_partido_favorito")
@login_required
def pagina_anadir_partido_asistido_favorito(partido_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	if not con.equipo_partido(equipo, partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	if not con.existe_partido_asistido(partido_id, current_user.id):

		con.cerrarConexion()

		return redirect("/partidos")

	estadio_equipo=con.estadio_equipo(equipo)

	id_partido_favorito=con.obtenerPartidoAsistidoFavorito(current_user.id)

	existe_partido_asistido_favorito=False if not id_partido_favorito else True

	if existe_partido_asistido_favorito:

		con.eliminarPartidoAsistidoFavorito(id_partido_favorito, current_user.id)
		
	con.insertarPartidoAsistidoFavorito(partido_id, current_user.id)

	con.cerrarConexion()

	return redirect(f"/partido/{partido_id}/asistido")

@bp_partido.route("/partido/<partido_id>/asistido/eliminar")
@login_required
def pagina_eliminar_partido_asistido(partido_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	if not con.equipo_partido(equipo, partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	if not con.existe_partido_asistido(partido_id, current_user.id):

		con.cerrarConexion()

		return redirect("/partidos")

	estadio_equipo=con.estadio_equipo(equipo)

	imagen_eliminar=con.obtenerImagenPartidoAsistido(partido_id, current_user.id)

	con.eliminarPartidoAsistido(partido_id, current_user.id)

	con.eliminarPartidoAsistidoFavorito(partido_id, current_user.id)

	con.eliminarTrayectosPartidoAsistido(partido_id, current_user.id)

	if imagen_eliminar:

		try:

			mensaje_eliminar_imagen={"categoria":"datalake_eliminar_imagen", "usuario":current_user.id, "imagen":imagen_eliminar, "entorno":entorno}

			enviarMensajeKafka(TOPIC, mensaje_eliminar_imagen)

		except Exception as e:

			print(f"Error en conexion con kafka: {e}")

	con.cerrarConexion()

	return redirect("/partidos/asistidos")

@bp_partido.route("/partido/<partido_id>/porra")
@login_required
def pagina_partido_porra(partido_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_proximo_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	if not con.equipo_proximo_partido(equipo, partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	if partido_id!=con.obtenerProximoPartidoPorra(equipo):

		con.cerrarConexion()

		return redirect("/partidos")

	estadio_equipo=con.estadio_equipo(equipo)

	proximo_partido=con.obtenerProximoPartido(partido_id)

	jugadores_local=con.obtenerJugadoresEquipo(proximo_partido[3])

	jugadores_visitante=con.obtenerJugadoresEquipo(proximo_partido[6])

	datos_porra=con.obtenerPorraPartido(partido_id, current_user.id) if con.existe_porra_partido(partido_id, current_user.id) else ()

	goleadores_porra=con.obtenerGoleadoresPorraPartido(partido_id, current_user.id)

	porras_usuarios=list(filter(lambda porra: porra[0]!=current_user.id, con.obtenerPorrasPartido(partido_id)))

	clasificacion_porras=con.obtenerClasificacionPorras()

	con.cerrarConexion()

	return render_template("porra_proximo_partido.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							proximo_partido=proximo_partido,
							partido_id=partido_id,
							jugadores_local=[{"id":jugador[0], "nombre":jugador[1], "imagen":jugador[2]} for jugador in jugadores_local],
							jugadores_visitante=[{"id":jugador[0], "nombre":jugador[1], "imagen":jugador[2]} for jugador in jugadores_visitante],
							datos_porra=datos_porra,
							porra_realizada=True if datos_porra else False,
							goleadores_porra=goleadores_porra,
							porras_usuarios=porras_usuarios,
							clasificacion_porras=clasificacion_porras,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_jugador=URL_DATALAKE_JUGADORES,
							url_imagen_usuario_imagenes=f"{URL_DATALAKE_USUARIOS}{current_user.id}/imagenes/",
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/",
							url_imagen_usuario_perfil_general=URL_DATALAKE_USUARIOS)

@bp_partido.route("/partido/<partido_id>/porra/eliminar")
@login_required
def pagina_eliminar_partido_porra(partido_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_proximo_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	if not con.equipo_proximo_partido(equipo, partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	if partido_id!=con.obtenerProximoPartidoPorra(equipo):

		con.cerrarConexion()

		return redirect("/partidos")

	estadio_equipo=con.estadio_equipo(equipo)

	con.eliminarPorraPartido(partido_id, current_user.id)

	return redirect(f"/partido/{partido_id}/porra")


bp_partido.add_app_template_filter(es_numero, name="es_numero")
bp_partido.add_app_template_filter(obtenerNumeroDias, name="obtenerNumeroDias")