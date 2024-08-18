from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PAISES, URL_DATALAKE_COMPETICIONES, URL_DATALAKE_ESCUDOS

bp_competicion=Blueprint("competicion", __name__)


@bp_competicion.route("/competicion/<competicion_id>")
@login_required
def pagina_competicion(competicion_id:str):

	con=Conexion()

	if not con.existe_competicion(competicion_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	datos_competicion=con.obtenerDatosCompeticion(competicion_id)

	equipos_competicion=con.obtenerEquiposCompeticion(competicion_id)

	equipos_campeones=con.obtenerCampeonesCompeticion(competicion_id)

	partidos_competicion=con.obtenerPartidosCompeticion(competicion_id)

	con.cerrarConexion()

	return render_template("competicion.html",
							usuario=current_user.id,
							equipo=equipo,
							datos_competicion=datos_competicion,
							equipos_competicion=equipos_competicion,
							equipos_campeones=equipos_campeones,
							partidos_competicion=partidos_competicion,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS)