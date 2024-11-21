from flask import Blueprint, render_template, redirect, request, send_file
from flask_login import login_required, current_user
import os

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_PAISES

from src.utilidades.utils import anadirPuntos, obtenerNombrePaisSeleccionado, obtenerPaisesNoSeleccionados
from src.utilidades.utils import vaciarCarpetaMapasUsuario, crearMapaMisEstadios, crearMapaMisEstadiosDetalle, obtenerCentroide

bp_estadio=Blueprint("estadio", __name__)


@bp_estadio.route("/estadio/<estadio_id>")
@login_required
def pagina_estadio(estadio_id:str):

	con=Conexion()

	if not con.existe_estadio(estadio_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	estadio=con.obtenerEstadio(estadio_id)

	equipos_estadio=con.obtenerEquipoEstadio(estadio_id)

	estadio_asistido=con.estadio_asistido_usuario(current_user.id, estadio_id)

	con.cerrarConexion()

	return render_template("estadio.html",
							usuario=current_user.id,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							estadio=estadio,
							equipos_estadio=equipos_estadio,
							anadirPuntos=anadirPuntos,
							estadio_asistido=estadio_asistido,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_pais=URL_DATALAKE_PAISES)

@bp_estadio.route("/estadios")
@login_required
def pagina_estadios():

	numero_top=request.args.get("top_estadios", default=8, type=int)

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_estadios=con.obtenerDatosEstadios()

	datos_estadios_top=con.obtenerDatosEstadiosTop(numero_top)

	con.cerrarConexion()

	return render_template("estadios.html",
							usuario=current_user.id,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							datos_estadios=datos_estadios,
							numero_top=numero_top,
							tops=[8, 10, 15, 20, 25],
							datos_estadios_top=datos_estadios_top,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS)

@bp_estadio.route("/estadios/mis_estadios")
@login_required
def pagina_mis_estadios():

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_estadios=con.obtenerDatosEstadios()

	numero_estadios=len(datos_estadios)

	estadios_asistidos=con.obtenerEstadiosPartidosAsistidosUsuarioCantidad(current_user.id, numero_estadios)

	if not estadios_asistidos:

		con.cerrarConexion()

		return redirect("/partidos")

	numero_estadios_asistidos_fecha=4

	estadios_asistidos_fecha=con.obtenerEstadiosPartidosAsistidosUsuarioFecha(current_user.id, numero_estadios_asistidos_fecha)

	paises_asistidos=con.obtenerPaisesEstadiosPartidosAsistidosUsuarioCantidad(current_user.id, numero_estadios)

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	vaciarCarpetaMapasUsuario(os.path.join(ruta, "templates", "mapas"), current_user.id)

	datos_coordenadas=con.obtenerDatosCoordenadasEstadiosPartidosAsistidosUsuario(current_user.id, numero_estadios)

	centroide=obtenerCentroide(datos_coordenadas)

	crearMapaMisEstadios(os.path.join(ruta, "templates", "mapas"),
						datos_coordenadas,
						f"mapa_small_mis_estadios_user_{current_user.id}.html",
						centroide)

	crearMapaMisEstadiosDetalle(os.path.join(ruta, "templates", "mapas"),
								datos_coordenadas,
								f"mapa_detalle_mis_estadios_user_{current_user.id}.html",
								centroide)

	con.cerrarConexion()

	return render_template("mis_estadios.html",
							usuario=current_user.id,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							estadios_asistidos=estadios_asistidos,
							numero_estadios=len(estadios_asistidos),
							estadios_asistidos_fecha=estadios_asistidos_fecha,
							paises_asistidos=paises_asistidos,
							numero_paises=len(paises_asistidos),
							nombre_mapa_small=f"mapa_small_mis_estadios_user_{current_user.id}.html",
							nombre_mapa_detalle=f"mapa_detalle_mis_estadios_user_{current_user.id}.html",
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS)

@bp_estadio.route("/estadios/mis_estadios/mapa/<nombre_mapa>")
@login_required
def visualizarMapaMisEstadios(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "mapas", nombre_mapa)

	return send_file(ruta_mapa)

@bp_estadio.route("/estadios/mis_estadios/<codigo_pais>")
@login_required
def pagina_pais_mis_estadios(codigo_pais:str):

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_estadios=con.obtenerDatosEstadios()

	numero_estadios=len(datos_estadios)

	estadios_asistidos_pais=con.obtenerEstadiosPaisPartidosAsistidosUsuarioCantidad(current_user.id, codigo_pais, numero_estadios)

	if not estadios_asistidos_pais:

		con.cerrarConexion()

		return redirect("/partidos")

	paises_asistidos=con.obtenerPaisesEstadiosPartidosAsistidosUsuarioCantidad(current_user.id, numero_estadios)

	nombre_pais_seleccionado=obtenerNombrePaisSeleccionado(paises_asistidos, codigo_pais)

	paises_no_seleccionados=obtenerPaisesNoSeleccionados(paises_asistidos, codigo_pais)

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	vaciarCarpetaMapasUsuario(os.path.join(ruta, "templates", "mapas"), current_user.id)

	datos_coordenadas=con.obtenerDatosCoordenadasEstadiosPaisPartidosAsistidosUsuario(current_user.id, codigo_pais, numero_estadios)

	centroide=obtenerCentroide(datos_coordenadas)

	crearMapaMisEstadios(os.path.join(ruta, "templates", "mapas"),
						datos_coordenadas,
						f"mapa_small_mis_estadios_user_{current_user.id}.html",
						centroide,
						3)

	con.cerrarConexion()

	return render_template("mis_estadios_pais.html",
							usuario=current_user.id,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							codigo_pais=codigo_pais,
							estadios_asistidos_pais=estadios_asistidos_pais,
							numero_estadios_pais=len(estadios_asistidos_pais),
							nombre_pais_seleccionado=nombre_pais_seleccionado,
							paises_no_seleccionados=paises_no_seleccionados,
							nombre_mapa_small_detalle=f"mapa_small_mis_estadios_user_{current_user.id}.html",
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS)

@bp_estadio.route("/estadios/mis_estadios_pais/mapa/<nombre_mapa>")
@login_required
def visualizarMapaMisEstadiosPais(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "mapas", nombre_mapa)

	return send_file(ruta_mapa)