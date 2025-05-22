from flask import Blueprint, render_template, redirect, send_file
from flask_login import login_required, current_user
import os

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_JUGADORES, URL_DATALAKE_USUARIOS

from src.utilidades.utils import vaciarCarpetaMapasUsuario, crearMapaTrayecto, crearMapaTrayectosIdaVuelta


bp_partido=Blueprint("partido", __name__)


@bp_partido.route("/partido/<partido_id>")
@login_required
def pagina_partido(partido_id:str):

	con=Conexion()

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	if not con.equipo_partido(equipo, partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	estadio_equipo=con.estadio_equipo(equipo)

	partido=con.obtenerPartido(partido_id)

	partido_id_anterior=con.obtenerPartidoAnterior(partido_id, equipo)

	partido_id_siguiente=con.obtenerPartidoSiguiente(partido_id, equipo)

	goleadores=con.obtenerGoleadoresPartido(partido_id)

	partidos_entre_equipos=con.obtenerPartidosEntreEquipos(partido[4], partido[7], 3)

	historial_entre_equipos=con.obtenerPartidosHistorialEntreEquipos(partido[4], partido[7])

	partido_asistido=con.existe_partido_asistido(partido_id, current_user.id)

	con.cerrarConexion()

	return render_template("partido.html",
							usuario=current_user.id,
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
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_jugador=URL_DATALAKE_JUGADORES)

@bp_partido.route("/partido/<partido_id>/asistido")
@login_required
def pagina_partido_asistido(partido_id:str):

	con=Conexion()

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

	trayectos_ida=con.obtenerTrayectosPartidoAsistido(partido_id, current_user.id, "I")

	trayectos_vuelta=con.obtenerTrayectosPartidoAsistido(partido_id, current_user.id, "V")

	con.cerrarConexion()

	return render_template("partido_asistido.html",
							usuario=current_user.id,
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
							trayectos_vuelta=trayectos_vuelta,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_usuario_imagenes=f"{URL_DATALAKE_USUARIOS}{current_user.id}/imagenes/")

@bp_partido.route("/partido/<partido_id>/asistido/trayecto/mapa/<nombre_mapa>")
@login_required
def visualizarMapaTrayecto(partido_id:str, nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "mapas", "trayectos", nombre_mapa)

	return send_file(ruta_mapa)

@bp_partido.route("/partido/<partido_id>/asistido/quitar_partido_favorito")
@login_required
def pagina_quitar_partido_asistido_favorito(partido_id:str):

	con=Conexion()

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

	con=Conexion()

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

	con=Conexion()

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

	con.eliminarPartidoAsistido(partido_id, current_user.id)

	con.eliminarPartidoAsistidoFavorito(partido_id, current_user.id)

	con.eliminarTrayectosPartidoAsistido(partido_id, current_user.id)

	con.cerrarConexion()

	return redirect("/partidos/asistidos")

def es_numero(value):

    try:

        float(value)
        return True

    except (ValueError, TypeError):
    	
        return False

bp_partido.add_app_template_filter(es_numero, name='es_numero')