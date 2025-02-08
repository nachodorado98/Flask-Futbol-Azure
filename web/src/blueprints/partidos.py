from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from datetime import datetime

from src.utilidades.utils import limpiarResultadosPartidos, obtenerCompeticionesPartidosUnicas, obtenerPrimerUltimoDiaAnoMes
from src.utilidades.utils import obtenerAnoMesFechas, generarCalendario, mapearAnoMes, cruzarPartidosCalendario
from src.utilidades.utils import ano_mes_anterior, ano_mes_siguiente

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_COMPETICIONES

bp_partidos=Blueprint("partidos", __name__)


@bp_partidos.route("/partidos")
@login_required
def pagina_partidos():

	local=request.args.get("local", default=0, type=int)
	temporada=request.args.get("temporada", default=None, type=int)
	competicion=request.args.get("competicion", default=None, type=str)
	resultados=request.args.get("resultados", default=None, type=str)

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

	proximos_partidos=con.obtenerProximosPartidosEquipo(equipo, 1)

	if not partidos:

		con.cerrarConexion()

		return render_template("no_partidos.html",
								usuario=current_user.id,
								equipo=equipo,
								nombre_equipo=nombre_equipo,
								estadio_equipo=estadio_equipo,
								temporada_filtrada=None,
								competicion_filtrada=None,
								resultado_filtrado=None,
								local=local,
								ano_mes_calendario=None,
								url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	temporada_filtrada=temporadas[0] if not temporada else temporada

	fecha_ultimo_partido=con.obtenerFechaUltimoPartidoTemporada(equipo, str(temporada_filtrada))

	ano_mes_calendario=datetime.strptime(fecha_ultimo_partido, "%Y-%m-%d").strftime("%Y-%m") if fecha_ultimo_partido else None

	con.cerrarConexion()

	partidos_filtrados=list(filter(lambda partido: partido[0].startswith(str(temporada_filtrada)), partidos))

	if not partidos_filtrados:

		return render_template("no_partidos.html",
						usuario=current_user.id,
						equipo=equipo,
						nombre_equipo=nombre_equipo,
						estadio_equipo=estadio_equipo,
						temporada_filtrada=temporada_filtrada,
						competicion_filtrada=None,
						resultado_filtrado=None,
						local=local,
						ano_mes_calendario=ano_mes_calendario,
						url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	competiciones_unicas=obtenerCompeticionesPartidosUnicas(partidos_filtrados)

	competicion_filtrada="Todo" if not competicion else competicion

	if competicion_filtrada!="Todo":

		partidos_filtrados_competicion=list(filter(lambda partido: partido[9]==competicion_filtrada, partidos_filtrados))

	else:

		partidos_filtrados_competicion=partidos_filtrados

	if not partidos_filtrados_competicion:

		return render_template("no_partidos.html",
					usuario=current_user.id,
					equipo=equipo,
					nombre_equipo=nombre_equipo,
					estadio_equipo=estadio_equipo,
					temporada_filtrada=temporada_filtrada,
					competicion_filtrada=competicion_filtrada,
					resultado_filtrado=None,
					local=local,
					ano_mes_calendario=ano_mes_calendario,
					url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	resultado_filtrado="Todo" if not resultados else resultados

	if resultado_filtrado=="Ganados":

		partidos_filtrados_resultado=list(filter(lambda partido: partido[-3]==1, partidos_filtrados_competicion))

	elif resultado_filtrado=="Perdidos":

		partidos_filtrados_resultado=list(filter(lambda partido: partido[-2]==1, partidos_filtrados_competicion))

	elif resultado_filtrado=="Empatados":

		partidos_filtrados_resultado=list(filter(lambda partido: partido[-1]==1, partidos_filtrados_competicion))

	else:

		partidos_filtrados_resultado=partidos_filtrados_competicion

	if not partidos_filtrados_resultado:

		return render_template("no_partidos.html",
								usuario=current_user.id,
								equipo=equipo,
								nombre_equipo=nombre_equipo,
								estadio_equipo=estadio_equipo,
								temporada_filtrada=temporada_filtrada,
								competicion_filtrada=competicion_filtrada,
								resultado_filtrado=resultado_filtrado,
								local=local,
								ano_mes_calendario=ano_mes_calendario,
								url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	resultados_partidos_disputados=limpiarResultadosPartidos(partidos_filtrados_resultado)

	partidos_asistidos_filtrados=list(filter(lambda asistido: asistido[0] in [partido_filtrado[0] for partido_filtrado in partidos_filtrados_resultado], partidos_asistidos_totales))

	return render_template("partidos.html",
							usuario=current_user.id,
							equipo=equipo,
							nombre_equipo=nombre_equipo,
							estadio_equipo=estadio_equipo,
							temporadas=temporadas,
							temporada_filtrada=temporada_filtrada,
							partidos=partidos_filtrados_resultado,
							numero_partidos=len(partidos_filtrados_resultado),
							resultados_partidos_disputados=resultados_partidos_disputados,
							partidos_asistidos=partidos_asistidos_filtrados,
							numero_partidos_asistidos=len(partidos_asistidos_filtrados),
							proximos_partidos=proximos_partidos,
							competiciones_unicas=competiciones_unicas,
							competicion_filtrada=competicion_filtrada,
							resultado_filtrado=resultado_filtrado,
							local=local,
							ano_mes_calendario=ano_mes_calendario,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS)

@bp_partidos.route("/partidos/calendario/<ano_mes>")
@login_required
def pagina_partidos_calendario(ano_mes:str):

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	nombre_equipo=con.obtenerNombreEquipo(equipo)

	estadio_equipo=con.estadio_equipo(equipo)

	primer_ultimo_dia=obtenerPrimerUltimoDiaAnoMes(ano_mes)

	if not primer_ultimo_dia:

		return redirect("/partidos")

	fecha_minima_maxima=con.obtenerFechaMinimaMaximaPartidos(equipo)

	if not fecha_minima_maxima:

		return redirect("/partidos")

	anterior_ano_mes, siguiente_ano_mes=ano_mes_anterior(ano_mes), ano_mes_siguiente(ano_mes)

	ano_mes_calendario=mapearAnoMes(ano_mes)

	partidos_calendario=con.obtenerPartidosEquipoCalendario(equipo, ano_mes)

	anos_meses=obtenerAnoMesFechas(fecha_minima_maxima[0], fecha_minima_maxima[1])

	ano_mes_anterior_boton=anterior_ano_mes if list(filter(lambda ano_mes: ano_mes[0]==anterior_ano_mes, anos_meses)) else None

	ano_mes_siguiente_boton=siguiente_ano_mes if list(filter(lambda ano_mes: ano_mes[0]==siguiente_ano_mes, anos_meses)) else None

	calendario=generarCalendario(primer_ultimo_dia[0], primer_ultimo_dia[1])

	semanas=cruzarPartidosCalendario(partidos_calendario, calendario)

	return render_template("partidos_calendario.html",
								usuario=current_user.id,
								equipo=equipo,
								nombre_equipo=nombre_equipo,
								estadio_equipo=estadio_equipo,
								ano_mes_calendario=ano_mes_calendario,
								anos_meses=anos_meses,
								semanas=semanas,
								primer_ultimo_dia=primer_ultimo_dia,
								partidos_calendario=partidos_calendario,
								ano_mes_anterior_boton=ano_mes_anterior_boton,
								ano_mes_siguiente_boton=ano_mes_siguiente_boton,
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

	partidos_asistidos_ids=tuple(map(lambda partido_asistido: partido_asistido[0], partidos_asistidos))

	equipos_mas_enfrentados=con.obtenerEquiposPartidosAsistidosUsuarioCantidadFiltrado(current_user.id, partidos_asistidos_ids, 1)

	estadios_mas_visitados=con.obtenerEstadiosPartidosAsistidosUsuarioCantidadFiltrado(current_user.id, partidos_asistidos_ids, 1)

	competiciones_mas_asistidas=con.obtenerCompeticionesPartidosAsistidosUsuarioCantidadFiltrado(current_user.id, partidos_asistidos_ids, 1)

	if not equipos_mas_enfrentados or not estadios_mas_visitados or not competiciones_mas_asistidas:

		con.cerrarConexion()

		return render_template("error.html",
								usuario=current_user.id,
								equipo=equipo,
								nombre_equipo=nombre_equipo,
								estadio_equipo=estadio_equipo,
								local=local,
								url_imagen_escudo=URL_DATALAKE_ESCUDOS)

	id_partido_asistido_favorito=con.obtenerPartidoAsistidoFavorito(current_user.id)

	datos_partido_asistido_favorito=con.obtenerPartido(id_partido_asistido_favorito)

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
							competicion_mas_asistida=competiciones_mas_asistidas[0],
							local=local,
							partidos_asistidos_ids=partidos_asistidos_ids,
							id_partido_asistido_favorito=id_partido_asistido_favorito,
							datos_partido_asistido_favorito=datos_partido_asistido_favorito,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES)

@bp_partidos.route("/partidos/proximos")
@login_required
def pagina_partidos_proximos():

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	nombre_equipo=con.obtenerNombreEquipo(equipo)

	estadio_equipo=con.estadio_equipo(equipo)

	proximos_partidos=con.obtenerProximosPartidosEquipo(equipo, 100)

	con.cerrarConexion()

	if not proximos_partidos:

		return redirect("/partidos")

	return render_template("proximos_partidos.html",
							usuario=current_user.id,
							equipo=equipo,
							nombre_equipo=nombre_equipo,
							estadio_equipo=estadio_equipo,
							proximos_partidos=proximos_partidos,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS)