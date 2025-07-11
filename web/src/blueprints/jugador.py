from flask import Blueprint, render_template, redirect, current_app
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PAISES, URL_DATALAKE_ESCUDOS, URL_DATALAKE_JUGADORES, URL_DATALAKE_SELECCIONES, URL_DATALAKE_USUARIOS

bp_jugador=Blueprint("jugador", __name__)


@bp_jugador.route("/jugador/<jugador_id>")
@login_required
def pagina_jugador(jugador_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_jugador(jugador_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_jugador=con.obtenerDatosJugador(jugador_id)

	equipos_jugador=con.obtenerEquiposJugador(jugador_id)

	seleccion_jugador=con.obtenerSeleccionJugador(jugador_id)

	con.cerrarConexion()

	return render_template("jugador.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							datos_jugador=datos_jugador,
							equipos_jugador=equipos_jugador,
							seleccion_jugador=seleccion_jugador,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_jugador=URL_DATALAKE_JUGADORES,
							url_imagen_seleccion=URL_DATALAKE_SELECCIONES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_jugador.route("/jugadores")
@login_required
def pagina_jugadores():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_jugadores=con.obtenerDatosJugadores()

	numero_top=8

	datos_jugadores_top=con.obtenerDatosJugadoresTop(numero_top)

	con.cerrarConexion()

	return render_template("jugadores.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							datos_jugadores=datos_jugadores,
							numero_top=numero_top,
							datos_jugadores_top=datos_jugadores_top,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_jugador=URL_DATALAKE_JUGADORES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")