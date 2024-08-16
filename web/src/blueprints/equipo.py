from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_ENTRENADORES, URL_DATALAKE_PRESIDENTES
from src.config import URL_DATALAKE_PAISES

bp_equipo=Blueprint("equipo", __name__)


@bp_equipo.route("/equipo/<equipo_id>")
@login_required
def pagina_equipo(equipo_id:str):

	con=Conexion()

	if not con.existe_equipo(equipo_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	datos_equipo=con.obtenerDatosEquipo(equipo_id)

	favorito=True if equipo==equipo_id else False

	con.cerrarConexion()

	return render_template("equipo.html",
							usuario=current_user.id,
							equipo=equipo,
							datos_equipo=datos_equipo,
							favorito=favorito,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_entrenador=URL_DATALAKE_ENTRENADORES,
							url_imagen_presidente=URL_DATALAKE_PRESIDENTES,
							url_imagen_pais=URL_DATALAKE_PAISES)