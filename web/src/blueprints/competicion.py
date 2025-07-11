from flask import Blueprint, render_template, redirect, current_app
from flask_login import login_required, current_user

from src.utilidades.utils import limpiarResultadosPartidos

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PAISES, URL_DATALAKE_COMPETICIONES, URL_DATALAKE_ESCUDOS, URL_DATALAKE_USUARIOS

bp_competicion=Blueprint("competicion", __name__)


@bp_competicion.route("/competicion/<competicion_id>")
@login_required
def pagina_competicion(competicion_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_competicion(competicion_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_competicion=con.obtenerDatosCompeticion(competicion_id)

	equipos_competicion=con.obtenerEquiposCompeticion(competicion_id)

	equipos_campeones=con.obtenerCampeonesCompeticion(competicion_id)

	partidos_competicion=con.obtenerPartidosCompeticion(competicion_id)

	con.cerrarConexion()

	return render_template("competicion.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							datos_competicion=datos_competicion,
							equipos_competicion=equipos_competicion,
							equipos_campeones=equipos_campeones,
							partidos_competicion=partidos_competicion,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_competicion.route("/competiciones")
@login_required
def pagina_competiciones():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_competiciones=con.obtenerDatosCompeticiones()

	numero_top=8

	datos_competiciones_top=con.obtenerDatosCompeticionesTop(numero_top)

	con.cerrarConexion()

	return render_template("competiciones.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							datos_competiciones=datos_competiciones,
							numero_top=numero_top,
							datos_competiciones_top=datos_competiciones_top,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_competicion.route("/competiciones/mis_competiciones")
@login_required
def pagina_mis_competiciones():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_competiciones=con.obtenerDatosCompeticiones()

	numero_competiciones=len(datos_competiciones)

	competiciones_asistidos=con.obtenerCompeticionesPartidosAsistidosUsuarioCantidad(current_user.id, numero_competiciones)

	con.cerrarConexion()

	if not competiciones_asistidos:

		return redirect("/partidos")

	return render_template("mis_competiciones.html",
						usuario=current_user.id,
						imagen_perfil=current_user.imagen_perfil,
						equipo=equipo,
						estadio_equipo=estadio_equipo,
						competiciones_asistidos=competiciones_asistidos,
						numero_competiciones=len(competiciones_asistidos),
						url_imagen_pais=URL_DATALAKE_PAISES,
						url_imagen_competicion=URL_DATALAKE_COMPETICIONES,
						url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_competicion.route("/competiciones/mis_competiciones/partidos_competicion/<competicion_id>")
@login_required
def pagina_mis_competiciones_competicion_partidos_competicion(competicion_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	partidos_asistidos_competicion=con.obtenerPartidosAsistidosUsuarioCompeticion(current_user.id, equipo, competicion_id)

	if not partidos_asistidos_competicion:

		con.cerrarConexion()

		return redirect("/partidos")

	datos_competicion=con.obtenerDatosCompeticion(competicion_id)

	resultados_partidos_asistidos_competicion=limpiarResultadosPartidos(partidos_asistidos_competicion)

	con.cerrarConexion()

	return render_template("partidos_asistidos_competicion.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							partidos_asistidos_competicion=partidos_asistidos_competicion,
							datos_competicion=datos_competicion,
							numero_partidos_asistidos_competicion=len(partidos_asistidos_competicion),
							resultados_partidos_asistidos_competicion=resultados_partidos_asistidos_competicion,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")