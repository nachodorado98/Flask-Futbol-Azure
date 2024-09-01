from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_ENTRENADORES, URL_DATALAKE_PRESIDENTES
from src.config import URL_DATALAKE_PAISES, URL_DATALAKE_COMPETICIONES, URL_DATALAKE_JUGADORES

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

	jugador_equipo=con.obtenerDatosJugadorEquipoValoracion(equipo_id)

	ultimo_partido=con.ultimoPartidoEquipo(equipo_id)

	con.cerrarConexion()

	return render_template("equipo.html",
							usuario=current_user.id,
							equipo=equipo,
							datos_equipo=datos_equipo,
							favorito=favorito,
							jugador=jugador_equipo,
							ultimo_partido=ultimo_partido,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_entrenador=URL_DATALAKE_ENTRENADORES,
							url_imagen_presidente=URL_DATALAKE_PRESIDENTES,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_jugador=URL_DATALAKE_JUGADORES,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES)

@bp_equipo.route("/equipos")
@login_required
def pagina_equipos():

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	datos_equipos=con.obtenerDatosEquipos()

	numero_top=7

	datos_equipos_top=con.obtenerDatosEquiposTop(numero_top)

	con.cerrarConexion()

	return render_template("equipos.html",
							usuario=current_user.id,
							equipo=equipo,
							datos_equipos=datos_equipos,
							numero_top=numero_top,
							datos_equipos_top=datos_equipos_top,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES)