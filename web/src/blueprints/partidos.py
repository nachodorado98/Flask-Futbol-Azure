from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from src.utilidades.utils import limpiarResultadosPartidos

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS

bp_partidos=Blueprint("partidos", __name__)


@bp_partidos.route("/partidos")
@login_required
def pagina_partidos():

	local=request.args.get("local", default=0, type=int)
	temporada=request.args.get("temporada", default=None, type=int)

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	nombre_equipo=con.obtenerNombreEquipo(equipo)

	if local==1:	

		partidos=con.obtenerPartidosCasa(equipo)

	elif local==2:

		partidos=con.obtenerPartidosFuera(equipo)

	else:

		partidos=con.obtenerPartidosEquipo(equipo)

	temporadas=con.obtenerTemporadasEquipo(equipo)

	partidos_asistidos_totales=con.obtenerPartidosAsistidosUsuario(current_user.id)

	con.cerrarConexion()

	if not partidos:

		return render_template("no_partidos.html",
								usuario=current_user.id,
								equipo=equipo,
								nombre_equipo=nombre_equipo,
								temporada_filtrada=None,
								local=local,
								url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	temporada_filtrada=temporadas[0] if not temporada else temporada

	partidos_filtrados=list(filter(lambda partido: partido[0].startswith(str(temporada_filtrada)), partidos))

	if not partidos_filtrados:

		return render_template("no_partidos.html",
						usuario=current_user.id,
						equipo=equipo,
						nombre_equipo=nombre_equipo,
						temporada_filtrada=temporada_filtrada,
						local=local,
						url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	partidos_ganados=len(list(filter(lambda partido: partido[-1]==1, partidos_filtrados)))

	partidos_asistidos_filtrados=list(filter(lambda asistido: asistido[0] in [partido_filtrado[0] for partido_filtrado in partidos_filtrados], partidos_asistidos_totales))

	return render_template("partidos.html",
							usuario=current_user.id,
							equipo=equipo,
							nombre_equipo=nombre_equipo,
							temporadas=temporadas,
							temporada_filtrada=temporada_filtrada,
							partidos=partidos_filtrados,
							numero_partidos=len(partidos_filtrados),
							partidos_ganados=partidos_ganados,
							partidos_asistidos=partidos_asistidos_filtrados,
							numero_partidos_asistidos=len(partidos_asistidos_filtrados),
							local=local,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS)

@bp_partidos.route("/partidos/asistidos")
@login_required
def pagina_partidos_asistidos():

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	nombre_equipo=con.obtenerNombreEquipo(equipo)

	partidos_asistidos=con.obtenerPartidosAsistidosUsuario(current_user.id)

	con.cerrarConexion()

	if not partidos_asistidos:

		return render_template("no_partidos_asistidos.html",
								usuario=current_user.id,
								equipo=equipo,
								nombre_equipo=nombre_equipo,
								url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	resultados_partidos_asistidos=limpiarResultadosPartidos(partidos_asistidos)	

	return render_template("partidos_asistidos.html",
							usuario=current_user.id,
							equipo=equipo,
							nombre_equipo=nombre_equipo,
							partidos_asistidos=partidos_asistidos,
							numero_partidos_asistidos=len(partidos_asistidos),
							resultados_partidos_asistidos=resultados_partidos_asistidos,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS)