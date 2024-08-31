from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_PAISES

from src.utilidades.utils import anadirPuntos

bp_estadio=Blueprint("estadio", __name__)


@bp_estadio.route("/estadio/<estadio_id>")
@login_required
def pagina_estadio(estadio_id:str):

	con=Conexion()

	if not con.existe_estadio(estadio_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	estadio=con.obtenerEstadio(estadio_id)

	equipos_estadio=con.obtenerEquipoEstadio(estadio_id)

	con.cerrarConexion()

	return render_template("estadio.html",
							usuario=current_user.id,
							equipo=equipo,
							estadio=estadio,
							equipos_estadio=equipos_estadio,
							anadirPuntos=anadirPuntos,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS)

@bp_estadio.route("/estadios")
@login_required
def pagina_estadios():

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	datos_estadios=con.obtenerDatosEstadios()

	con.cerrarConexion()

	return render_template("estadios.html",
							usuario=current_user.id,
							equipo=equipo,
							datos_estadios=datos_estadios,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS)