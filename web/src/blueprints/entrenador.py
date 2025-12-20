from flask import Blueprint, render_template, redirect, current_app
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PAISES, URL_DATALAKE_ESCUDOS, URL_DATALAKE_ENTRENADORES, URL_DATALAKE_USUARIOS
from src.config import URL_DATALAKE_TITULOS

bp_entrenador=Blueprint("entrenador", __name__)


@bp_entrenador.route("/entrenador/<entrenador_id>")
@login_required
def pagina_entrenador(entrenador_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_entrenador(entrenador_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	datos_entrenador=con.obtenerDatosEntrenador(entrenador_id)

	equipos_entrenador=con.obtenerEquiposEntrenador(entrenador_id)

	titulos_entrenador=con.obtenerTitulosEntrenador(entrenador_id)

	con.cerrarConexion()

	return render_template("entrenador.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							datos_entrenador=datos_entrenador,
							equipos_entrenador=equipos_entrenador,
							titulos_entrenador=titulos_entrenador,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_entrenador=URL_DATALAKE_ENTRENADORES,
							url_imagen_titulos=URL_DATALAKE_TITULOS,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")