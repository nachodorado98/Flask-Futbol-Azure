from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PAISES, URL_DATALAKE_ESCUDOS, URL_DATALAKE_JUGADORES 

bp_jugador=Blueprint("jugador", __name__)


@bp_jugador.route("/jugador/<jugador_id>")
@login_required
def pagina_jugador(jugador_id:str):

	con=Conexion()

	if not con.existe_jugador(jugador_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	datos_jugador=con.obtenerDatosJugador(jugador_id)

	con.cerrarConexion()

	return render_template("jugador.html",
							usuario=current_user.id,
							equipo=equipo,
							datos_jugador=datos_jugador,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_jugador=URL_DATALAKE_JUGADORES)

@bp_jugador.route("/jugadores")
@login_required
def pagina_jugadores():

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	datos_jugadores=con.obtenerDatosJugadores()

	numero_top=7

	datos_jugadores_top=con.obtenerDatosJugadoresTop(numero_top)

	con.cerrarConexion()

	return render_template("jugadores.html",
							usuario=current_user.id,
							equipo=equipo,
							datos_jugadores=datos_jugadores,
							numero_top=numero_top,
							datos_jugadores_top=datos_jugadores_top,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_jugador=URL_DATALAKE_JUGADORES)