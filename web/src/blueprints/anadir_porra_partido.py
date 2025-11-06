from flask import Blueprint, render_template, redirect, request, current_app
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.utilidades.utils import validarGolesGoleadores, goleadoresLimpios

bp_anadir_porra_partido=Blueprint("anadir_porra_partido", __name__)


@bp_anadir_porra_partido.route("/insertar_porra_partido", methods=["POST"])
@login_required
def pagina_insertar_porra_partido():

	entorno=current_app.config["ENVIROMENT"]

	partido_id=request.form.get("partido_id", type=str)

	goles_local=request.form.get("goles_local", type=int)
	goles_visitante=request.form.get("goles_visitante", type=int)

	goleadores_local=[]
	goleadores_visitante=[]

	for key, value in request.form.items():

		if key.startswith("local_goleador_"):

			goleadores_local.append(value)

		elif key.startswith("visitante_goleador_"):

			goleadores_visitante.append(value)

	con=Conexion(entorno)

	if not con.existe_proximo_partido(partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	if not con.equipo_proximo_partido(equipo, partido_id):

		con.cerrarConexion()

		return redirect("/partidos")

	if partido_id!=con.obtenerProximoPartidoPorra(equipo):

		con.cerrarConexion()

		return redirect("/partidos")

	if not validarGolesGoleadores(goles_local, goles_visitante, goleadores_local, goleadores_visitante, entorno):

		con.cerrarConexion()

		return redirect("/partidos")

	if not con.existe_porra_partido(partido_id, current_user.id):

		porra_id=f"{current_user.id}-{partido_id}"

		con.insertarPorraPartido(porra_id, current_user.id, partido_id, goles_local, goles_visitante)

		goleadores_local_limpios=goleadoresLimpios(goleadores_local, True)

		goleadores_visitante_limpios=goleadoresLimpios(goleadores_visitante, False)
		
		for goleador, goles, local in goleadores_local_limpios:

			con.insertarGoleadorPorra(porra_id, goleador, goles, local)

		for goleador, goles, local in goleadores_visitante_limpios:

			con.insertarGoleadorPorra(porra_id, goleador, goles, local)

	con.cerrarConexion()

	return redirect(f"/partido/{partido_id}/porra")