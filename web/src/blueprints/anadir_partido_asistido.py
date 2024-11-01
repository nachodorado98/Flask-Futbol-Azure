from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user

from src.database.conexion import Conexion

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

	con.cerrarConexion()

	return render_template("anadir_partido_asistido.html",
							usuario=current_user.id,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							partidos_no_asistidos=partidos_no_asistidos,
							todos=todos,
							partido_id_anadir=partido_id_anadir,
							existe_partido_asistido_favorito=existe_partido_asistido_favorito)

@bp_anadir_partido_asistido.route("/insertar_partido_asistido", methods=["POST"])
@login_required
def pagina_insertar_partido_asistido():

	partido_id=request.form.get("partido_anadir")
	comentario=request.form.get("comentario")
	partido_asistido_favorito=request.form.get("partido-favorito")

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