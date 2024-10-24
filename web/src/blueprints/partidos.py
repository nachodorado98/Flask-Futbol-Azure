from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from src.utilidades.utils import limpiarResultadosPartidos

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS

bp_partidos=Blueprint("partidos", __name__)


@bp_partidos.route("/partidos")
@login_required
def pagina_partidos():

	local=request.args.get("local", default=0, type=int)
	temporada=request.args.get("temporada", default=None, type=int)

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	nombre_equipo=con.obtenerNombreEquipo(equipo)

	estadio_equipo=con.estadio_equipo(equipo)

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
								estadio_equipo=estadio_equipo,
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
						estadio_equipo=estadio_equipo,
						temporada_filtrada=temporada_filtrada,
						local=local,
						url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	resultados_partidos_disputados=limpiarResultadosPartidos(partidos_filtrados)

	partidos_asistidos_filtrados=list(filter(lambda asistido: asistido[0] in [partido_filtrado[0] for partido_filtrado in partidos_filtrados], partidos_asistidos_totales))

	return render_template("partidos.html",
							usuario=current_user.id,
							equipo=equipo,
							nombre_equipo=nombre_equipo,
							estadio_equipo=estadio_equipo,
							temporadas=temporadas,
							temporada_filtrada=temporada_filtrada,
							partidos=partidos_filtrados,
							numero_partidos=len(partidos_filtrados),
							resultados_partidos_disputados=resultados_partidos_disputados,
							partidos_asistidos=partidos_asistidos_filtrados,
							numero_partidos_asistidos=len(partidos_asistidos_filtrados),
							local=local,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS)

@bp_partidos.route("/partidos/asistidos")
@login_required
def pagina_partidos_asistidos():

	local=request.args.get("local", default=0, type=int)

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	nombre_equipo=con.obtenerNombreEquipo(equipo)

	estadio_equipo=con.estadio_equipo(equipo)

	if local==1:	

		partidos_asistidos=con.obtenerPartidosAsistidosUsuarioCasa(current_user.id)

	elif local==2:

		partidos_asistidos=con.obtenerPartidosAsistidosUsuarioFuera(current_user.id)

	else:

		partidos_asistidos=con.obtenerPartidosAsistidosUsuario(current_user.id)

	if not partidos_asistidos:

		con.cerrarConexion()

		return render_template("no_partidos_asistidos.html",
								usuario=current_user.id,
								equipo=equipo,
								nombre_equipo=nombre_equipo,
								estadio_equipo=estadio_equipo,
								local=local,
								url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	resultados_partidos_asistidos=limpiarResultadosPartidos(partidos_asistidos)

	equipos_mas_enfrentados=con.obtenerEquiposPartidosAsistidosUsuarioCantidad(current_user.id, 1)

	if not equipos_mas_enfrentados:

		con.cerrarConexion()

		return render_template("error.html",
								usuario=current_user.id,
								equipo=equipo,
								nombre_equipo=nombre_equipo,
								estadio_equipo=estadio_equipo,
								local=local,
								url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	estadios_mas_visitados=con.obtenerEstadiosPartidosAsistidosUsuarioCantidad(current_user.id, 1)

	con.cerrarConexion()

	return render_template("partidos_asistidos.html",
							usuario=current_user.id,
							equipo=equipo,
							nombre_equipo=nombre_equipo,
							estadio_equipo=estadio_equipo,
							partidos_asistidos=partidos_asistidos,
							numero_partidos_asistidos=len(partidos_asistidos),
							resultados_partidos_asistidos=resultados_partidos_asistidos,
							equipo_mas_enfrentado=equipos_mas_enfrentados[0],
							estadio_mas_visitado=estadios_mas_visitados[0],
							local=local,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS)