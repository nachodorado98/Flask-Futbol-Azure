from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user

from src.database.conexion import Conexion

bp_partido_asistido=Blueprint("partido_asistido", __name__)


@bp_partido_asistido.route("/anadir_partido_asistido")
@login_required
def pagina_anadir_partido_asistido():

	todos=request.args.get("todos", default=False, type=bool)
	partido_id_anadir=request.args.get("partido_id", default=None)

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	if todos:

		partidos_no_asistidos=con.obtenerPartidosNoAsistidosUsuario(current_user.id, equipo)

	else:

		partidos_no_asistidos=con.obtenerPartidosNoAsistidosUsuarioRecientes(current_user.id, equipo)

	con.cerrarConexion()

	if not partidos_no_asistidos:

		return render_template("no_partidos_asistidos.html",
								usuario=current_user.id,
								equipo=equipo)

	return render_template("anadir_partido_asistido.html",
							usuario=current_user.id,
							equipo=equipo,
							partidos_no_asistidos=partidos_no_asistidos,
							todos=todos,
							partido_id_anadir=partido_id_anadir)

@bp_partido_asistido.route("/insertar_partido_asistido", methods=["POST"])
@login_required
def pagina_insertar_partido_asistido():

	partido_id=request.form.get("partido_anadir")
	comentario=request.form.get("comentario")

	con=Conexion()

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	usuario=current_user.id

	if con.existe_partido_asistido(partido_id, usuario):

		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	if comentario and len(comentario)>255:
		
		con.cerrarConexion()

		return redirect("/anadir_partido_asistido")

	con.insertarPartidoAsistido(partido_id, usuario, comentario)

	con.cerrarConexion()

	return redirect("/partidos")