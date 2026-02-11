from flask import Blueprint, render_template, request, redirect, current_app, send_file
from flask_login import login_required, current_user
import os
from collections import Counter

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_USUARIOS, URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_PAISES

from src.utilidades.utils import estadiosVisitadosWrappedLimpio, equiposVistosWrappedLimpio, limpiarResultadosPartidos
from src.utilidades.utils import partidoMasGolesWrapped, partidosMesWrapped, paisesVisitadosWrappedLimpio, coordenadasEstadiosWrappedLimpio
from src.utilidades.utils import vaciarCarpetaMapasUsuario, obtenerCentroide, crearMapaMisEstadios, crearMapaMisEstadiosDetalle
from src.utilidades.utils import crearMapaMisEstadiosDetallePaises, obtenerTrayectos, obtenerTrayectosDatosPartidosAsistidos
from src.utilidades.utils import obtenerDistanciaTotalTrayectosWrapped, obtenerTrayectoMasLejanoWrapped, anadirPuntos
from src.utilidades.utils import obtenerKPISPartidosWrapped, obtenerKPISTrayectosWrapped


bp_wrapped=Blueprint("wrapped", __name__)


@bp_wrapped.route("/wrapped/annio/<annio>")
@login_required
def wrapped_annio(annio:int):

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

	estadios_asistidos_annio, estadios_nuevos_annio, paises_asistidos_annio, equipos_vistos_annio=obtenerKPISPartidosWrapped(partidos_asistidos_annio, equipo)

	partidos_asistidos_annio_anterior=con.obtenerPartidosAsistidosUsuarioAnnio(current_user.id, int(annio)-1)

	estadios_asistidos_annio_anterior, estadios_nuevos_annio_anterior, paises_asistidos_annio_anterior, equipos_vistos_annio_anterior=obtenerKPISPartidosWrapped(partidos_asistidos_annio_anterior, equipo)

	resultados_partidos_asistidos_annio=limpiarResultadosPartidos(partidos_asistidos_annio)

	partido_mas_goles=partidoMasGolesWrapped(partidos_asistidos_annio)

	datos_grafica_barras=partidosMesWrapped(partidos_asistidos_annio)

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	vaciarCarpetaMapasUsuario(os.path.join(ruta, "templates", "mapas", "estadios"), current_user.id)

	datos_coordenadas=coordenadasEstadiosWrappedLimpio(partidos_asistidos_annio)

	nombre_mapa_small=f"mapa_small_wrapped_annio_{annio}_user_{current_user.id}.html"

	nombre_mapa_detalle=f"mapa_detalle_wrapped_annio_{annio}_user_{current_user.id}.html"

	nombre_mapa_detalle_paises=f"mapa_detalle_paises_wrapped_annio_{annio}_user_{current_user.id}.html"

	mapas_correcto=True

	try:

		centroide=obtenerCentroide(datos_coordenadas)

		crearMapaMisEstadios(os.path.join(ruta, "templates", "mapas", "estadios"), datos_coordenadas, nombre_mapa_small, centroide)

		crearMapaMisEstadiosDetalle(os.path.join(ruta, "templates", "mapas", "estadios"), datos_coordenadas, nombre_mapa_detalle, centroide)

		coordenadas=[(dato[1], dato[2]) for dato in datos_coordenadas]

		crearMapaMisEstadiosDetallePaises(os.path.join(ruta, "templates", "mapas", "estadios"), coordenadas, nombre_mapa_detalle_paises, centroide)

	except Exception as e:

		print(e)
		mapas_correcto=False

	trayectos_partidos_asistidos_annio=con.obtenerTrayectosPartidosAsistidosAnnio(current_user.id, annio)

	partidos_asistidos_trayectos_annio, distancia_total_trayectos_annio, partido_asistido_trayecto_mas_lejano_annio, partido_asistido_trayecto_mas_locura_annio=obtenerKPISTrayectosWrapped(trayectos_partidos_asistidos_annio, partidos_asistidos_annio)

	trayectos_partidos_asistidos_annio_anterior=con.obtenerTrayectosPartidosAsistidosAnnio(current_user.id, int(annio)-1)

	partidos_asistidos_trayectos_annio_anterior, distancia_total_trayectos_annio_anterior, partido_asistido_trayecto_mas_lejano_annio_anterior, partido_asistido_trayecto_mas_locura_annio_anterior=obtenerKPISTrayectosWrapped(trayectos_partidos_asistidos_annio_anterior, partidos_asistidos_annio_anterior)

	con.cerrarConexion()

	return render_template("wrapped_annio.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							annio=annio,
							partidos_asistidos_annio=partidos_asistidos_annio,
							numero_partidos_asistidos_annio=len(partidos_asistidos_annio),
							numero_partidos_asistidos_annio_anterior=len(partidos_asistidos_annio_anterior),
							estadios_asistidos_annio=estadios_asistidos_annio,
							numero_estadios_asistidos_annio=len(estadios_asistidos_annio),
							numero_estadios_asistidos_annio_anterior=len(estadios_asistidos_annio_anterior),
							equipos_vistos_annio=equipos_vistos_annio,
							equipo_mas_visto_annio=equipos_vistos_annio[0] if equipos_vistos_annio else None,
							estadios_nuevos_annio=estadios_nuevos_annio,
							numero_estadios_nuevos_annio=len(estadios_nuevos_annio),
							numero_estadios_nuevos_annio_anterior=len(estadios_nuevos_annio_anterior),
							paises_asistidos_annio=paises_asistidos_annio,
							numero_paises_asistidos_annio=len(paises_asistidos_annio),
							numero_paises_asistidos_annio_anterior=len(paises_asistidos_annio_anterior),
							resultados_partidos_asistidos_annio=resultados_partidos_asistidos_annio,
							partido_mas_goles=partido_mas_goles,
							datos_grafica_barras=datos_grafica_barras,
							nombre_mapa_small=nombre_mapa_small,
							nombre_mapa_detalle=nombre_mapa_detalle,
							nombre_mapa_detalle_paises=nombre_mapa_detalle_paises,
							mapas_correcto=mapas_correcto,
							anadirPuntos=anadirPuntos,
							partidos_asistidos_trayectos_annio=partidos_asistidos_trayectos_annio,
							distancia_total_trayectos_annio=distancia_total_trayectos_annio,
							distancia_total_trayectos_annio_anterior=distancia_total_trayectos_annio_anterior,
							partido_asistido_trayecto_mas_lejano_annio=partido_asistido_trayecto_mas_lejano_annio,
							partido_asistido_trayecto_mas_lejano_annio_anterior=partido_asistido_trayecto_mas_lejano_annio_anterior,
							partido_asistido_trayecto_mas_locura_annio=partido_asistido_trayecto_mas_locura_annio,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_wrapped.route("/wrapped/mapa/<nombre_mapa>")
@login_required
def visualizarMapaEstadios(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "mapas", "estadios", nombre_mapa)

	return send_file(ruta_mapa)