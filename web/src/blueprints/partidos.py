from flask import Blueprint, render_template
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE

bp_partidos=Blueprint("partidos", __name__)


@bp_partidos.route("/partidos")
@login_required
def pagina_partidos():

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	nombre_equipo=con.obtenerNombreEquipo(equipo)

	partidos=con.obtenerPartidosEquipo(equipo)

	con.cerrarConexion()

	return render_template("partidos.html",
							usuario=current_user.id,
							equipo=equipo,
							nombre_equipo=nombre_equipo,
							partidos=partidos,
							url_imagen=URL_DATALAKE)