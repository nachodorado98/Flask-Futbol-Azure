from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, current_user
import os
from collections import Counter

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_USUARIOS, URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_PAISES

from src.utilidades.utils import estadiosVisitadosWrappedLimpio, equiposVistosWrappedLimpio, limpiarResultadosPartidos
from src.utilidades.utils import partidoMasGolesWrapped, partidosMesWrapped


bp_wrapped=Blueprint("wrapped", __name__)


@bp_wrapped.route("/wrapped/<annio>")
@login_required
def wrapped(annio:int):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	try:

		partidos_asistidos_annio=con.obtenerPartidosAsistidosUsuarioAnnio(current_user.id, annio)

	except Exception:

		con.cerrarConexion()

		return redirect("/partidos")

	if not partidos_asistidos_annio:

		con.cerrarConexion()

		return redirect("/partidos")

	estadios_asistidos_annio=estadiosVisitadosWrappedLimpio(partidos_asistidos_annio)

	equipos_vistos_annio=equiposVistosWrappedLimpio(partidos_asistidos_annio, equipo)

	partidos_estadios_nuevo_annio=list(filter(lambda partido: partido[16], partidos_asistidos_annio))

	estadios_nuevos_annio=estadiosVisitadosWrappedLimpio(partidos_estadios_nuevo_annio)

	resultados_partidos_asistidos_annio=limpiarResultadosPartidos(partidos_asistidos_annio)

	partido_mas_goles=partidoMasGolesWrapped(partidos_asistidos_annio)

	datos_grafica_barras=partidosMesWrapped(partidos_asistidos_annio)

	con.cerrarConexion()

	return render_template("wrapped.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							annio=annio,
							partidos_asistidos_annio=partidos_asistidos_annio,
							numero_partidos_asistidos_annio=len(partidos_asistidos_annio),
							estadios_asistidos_annio=estadios_asistidos_annio,
							numero_estadios_asistidos_annio=len(estadios_asistidos_annio),
							equipos_vistos_annio=equipos_vistos_annio,
							equipo_mas_visto_annio=equipos_vistos_annio[0] if equipos_vistos_annio else None,
							estadios_nuevos_annio=estadios_nuevos_annio,
							numero_estadios_nuevos_annio=len(estadios_nuevos_annio),
							resultados_partidos_asistidos_annio=resultados_partidos_asistidos_annio,
							partido_mas_goles=partido_mas_goles,
							datos_grafica_barras=datos_grafica_barras,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")