from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_JUGADORES, URL_DATALAKE_USUARIOS

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

	partido_id_asistido_anterior=con.obtenerPartidoAsistidoUsuarioAnterior(current_user.id, partido_id)

	partido_id_asistido_siguiente=con.obtenerPartidoAsistidoUsuarioSiguiente(current_user.id, partido_id)

	id_partido_asistido_favorito=con.obtenerPartidoAsistidoFavorito(current_user.id)

	partido_asistido_favorito=True if id_partido_asistido_favorito==partido_id else False

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
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_usuario_imagenes=f"{URL_DATALAKE_USUARIOS}{current_user.id}/imagenes/")

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

	con.cerrarConexion()

	return redirect("/partidos/asistidos")