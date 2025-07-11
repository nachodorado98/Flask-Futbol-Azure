from flask import Blueprint, render_template, redirect, current_app
from flask_login import login_required, current_user

from src.utilidades.utils import limpiarResultadosPartidos

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_ENTRENADORES, URL_DATALAKE_PRESIDENTES
from src.config import URL_DATALAKE_PAISES, URL_DATALAKE_COMPETICIONES, URL_DATALAKE_JUGADORES, URL_DATALAKE_USUARIOS

bp_equipo=Blueprint("equipo", __name__)


@bp_equipo.route("/equipo/<equipo_id>")
@login_required
def pagina_equipo(equipo_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_equipo(equipo_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_equipo=con.obtenerDatosEquipo(equipo_id)

	favorito=True if equipo==equipo_id else False

	jugador_equipo=con.obtenerDatosJugadorEquipoValoracion(equipo_id)

	ultimo_partido=con.ultimoPartidoEquipo(equipo_id)

	jugadores_equipo=con.obtenerJugadoresEquipo(equipo_id)

	con.cerrarConexion()

	return render_template("equipo.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							datos_equipo=datos_equipo,
							estadio_equipo=estadio_equipo,
							favorito=favorito,
							jugador=jugador_equipo,
							ultimo_partido=ultimo_partido,
							jugadores_equipo=jugadores_equipo,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_entrenador=URL_DATALAKE_ENTRENADORES,
							url_imagen_presidente=URL_DATALAKE_PRESIDENTES,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_jugador=URL_DATALAKE_JUGADORES,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_equipo.route("/equipos")
@login_required
def pagina_equipos():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_equipos=con.obtenerDatosEquipos()

	numero_top=8

	datos_equipos_top=con.obtenerDatosEquiposTop(numero_top)

	con.cerrarConexion()

	return render_template("equipos.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							datos_equipos=datos_equipos,
							numero_top=numero_top,
							datos_equipos_top=datos_equipos_top,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_equipo.route("/equipos/mis_equipos")
@login_required
def pagina_mis_equipos():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_equipos=con.obtenerDatosEquipos()

	numero_equipos=len(datos_equipos)

	equipos_enfrentados=con.obtenerEquiposPartidosAsistidosUsuarioCantidad(current_user.id, numero_equipos)

	con.cerrarConexion()

	if not equipos_enfrentados:

		return redirect("/partidos")

	return render_template("mis_equipos.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							equipos_enfrentados=equipos_enfrentados,
							numero_equipos=len(equipos_enfrentados),
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_equipo.route("/equipos/mis_equipos/partidos_equipo/<equipo_id>")
@login_required
def pagina_mis_equipos_equipo_partidos_equipo(equipo_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	partidos_asistidos_equipo=con.obtenerPartidosAsistidosUsuarioEquipo(current_user.id, equipo, equipo_id)

	if not partidos_asistidos_equipo:

		con.cerrarConexion()

		return redirect("/partidos")

	datos_equipo=con.obtenerDatosEquipo(equipo_id)

	resultados_partidos_asistidos_equipo=limpiarResultadosPartidos(partidos_asistidos_equipo)

	con.cerrarConexion()

	return render_template("partidos_asistidos_equipo.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							partidos_asistidos_equipo=partidos_asistidos_equipo,
							datos_equipo=datos_equipo,
							numero_partidos_asistidos_equipo=len(partidos_asistidos_equipo),
							resultados_partidos_asistidos_equipo=resultados_partidos_asistidos_equipo,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")