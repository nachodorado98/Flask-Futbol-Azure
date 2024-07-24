from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE

bp_partido=Blueprint("partido", __name__)


@bp_partido.route("/partido/<partido_id>")
@login_required
def pagina_partido(partido_id:str):

	con=Conexion()

	if not con.existe_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	partido=con.obtenerPartido(partido_id)

	con.cerrarConexion()

	return render_template("partido.html",
							usuario=current_user.id,
							equipo=equipo,
							partido=partido,
							url_imagen=URL_DATALAKE)