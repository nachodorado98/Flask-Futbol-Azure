from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PAISES, URL_DATALAKE_ESCUDOS, URL_DATALAKE_ENTRENADORES

bp_entrenador=Blueprint("entrenador", __name__)


@bp_entrenador.route("/entrenador/<entrenador_id>")
@login_required
def pagina_entrenador(entrenador_id:str):

	con=Conexion()

	if not con.existe_entrenador(entrenador_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	datos_entrenador=con.obtenerDatosEntrenador(entrenador_id)

	con.cerrarConexion()

	return render_template("entrenador.html",
							usuario=current_user.id,
							equipo=equipo,
							datos_entrenador=datos_entrenador,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_entrenador=URL_DATALAKE_ENTRENADORES)