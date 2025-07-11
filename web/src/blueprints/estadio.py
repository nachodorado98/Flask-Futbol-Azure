from flask import Blueprint, render_template, redirect, request, send_file, current_app
from flask_login import login_required, current_user
import os

from src.utilidades.utils import limpiarResultadosPartidos

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_ESCUDOS, URL_DATALAKE_ESTADIOS, URL_DATALAKE_PAISES, URL_DATALAKE_COMPETICIONES, URL_DATALAKE_USUARIOS

from src.utilidades.utils import anadirPuntos, obtenerNombrePaisSeleccionado, obtenerPaisesNoSeleccionados
from src.utilidades.utils import vaciarCarpetaMapasUsuario, crearMapaMisEstadios, crearMapaMisEstadiosDetalle
from src.utilidades.utils import obtenerCentroide, crearMapaMisEstadiosDetallePaises, crearMapaEstadio
from src.utilidades.utils import obtenerNombreDivisionSeleccionado, obtenerDivisionesNoSeleccionados

bp_estadio=Blueprint("estadio", __name__)


@bp_estadio.route("/estadio/<estadio_id>")
@login_required
def pagina_estadio(estadio_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	if not con.existe_estadio(estadio_id):

		con.cerrarConexion()

		return redirect("/partidos")

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	estadio=con.obtenerEstadio(estadio_id)

	equipos_estadio=con.obtenerEquipoEstadio(estadio_id)

	estadio_asistido=con.estadio_asistido_usuario(current_user.id, estadio_id)

	numero_veces_asistido=con.obtenerNumeroVecesEstadioPartidosAsistidosUsuario(current_user.id, estadio_id)

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	vaciarCarpetaMapasUsuario(os.path.join(ruta, "templates", "mapas", "estadios"), current_user.id)

	nombre_mapa_small_estadio=f"mapa_small_estadio_user_{current_user.id}.html"

	mapa_correcto=True

	try:

		crearMapaEstadio(os.path.join(ruta, "templates", "mapas", "estadios"), estadio, nombre_mapa_small_estadio)

	except Exception as e:

		print(e)
		mapa_correcto=False

	con.cerrarConexion()

	return render_template("estadio.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							estadio=estadio,
							equipos_estadio=equipos_estadio,
							anadirPuntos=anadirPuntos,
							estadio_asistido=estadio_asistido,
							numero_veces_asistido=numero_veces_asistido,
							nombre_mapa_small_estadio=nombre_mapa_small_estadio,
							mapa_correcto=mapa_correcto,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_estadio.route("/estadio/mapa/<nombre_mapa>")
@login_required
def visualizarMapaEstadio(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "mapas", "estadios", nombre_mapa)

	return send_file(ruta_mapa)

@bp_estadio.route("/estadios")
@login_required
def pagina_estadios():

	entorno=current_app.config["ENVIROMENT"]

	numero_top=request.args.get("top_estadios", default=8, type=int)

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_estadios=con.obtenerDatosEstadios()

	datos_estadios_top=con.obtenerDatosEstadiosTop(numero_top)

	con.cerrarConexion()

	return render_template("estadios.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							datos_estadios=datos_estadios,
							numero_top=numero_top,
							tops=[8, 10, 15, 20, 25],
							datos_estadios_top=datos_estadios_top,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_estadio.route("/estadios/mis_estadios")
@login_required
def pagina_mis_estadios():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_estadios=con.obtenerDatosEstadios()

	numero_estadios=len(datos_estadios)

	estadios_asistidos=con.obtenerEstadiosPartidosAsistidosUsuarioCantidad(current_user.id, numero_estadios)

	if not estadios_asistidos:

		con.cerrarConexion()

		return redirect("/partidos")

	estadios_asistidos_fecha=con.obtenerEstadiosPartidosAsistidosUsuarioFecha(current_user.id, 3)

	paises_asistidos=con.obtenerPaisesEstadiosPartidosAsistidosUsuarioCantidad(current_user.id, numero_estadios)

	estadios_competiciones_asistidos=con.obtenerEstadiosPartidosAsistidosUsuarioCompeticionCantidad(current_user.id, numero_estadios)

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	vaciarCarpetaMapasUsuario(os.path.join(ruta, "templates", "mapas", "estadios"), current_user.id)

	datos_coordenadas=con.obtenerDatosCoordenadasEstadiosPartidosAsistidosUsuario(current_user.id, numero_estadios)

	nombre_mapa_small=f"mapa_small_mis_estadios_user_{current_user.id}.html"

	nombre_mapa_detalle=f"mapa_detalle_mis_estadios_user_{current_user.id}.html"

	nombre_mapa_detalle_paises=f"mapa_detalle_paises_mis_estadios_user_{current_user.id}.html"

	mapas_correcto=True

	try:

		centroide=obtenerCentroide(datos_coordenadas)

		crearMapaMisEstadios(os.path.join(ruta, "templates", "mapas", "estadios"), datos_coordenadas, nombre_mapa_small, centroide)

		crearMapaMisEstadiosDetalle(os.path.join(ruta, "templates", "mapas", "estadios"), datos_coordenadas, nombre_mapa_detalle, centroide)

		coordenadas=con.obtenerCoordenadasEstadiosPartidosAsistidosUsuario(current_user.id, numero_estadios)

		crearMapaMisEstadiosDetallePaises(os.path.join(ruta, "templates", "mapas", "estadios"), coordenadas, nombre_mapa_detalle_paises, centroide)

	except Exception as e:

		print(e)
		mapas_correcto=False

	con.cerrarConexion()

	return render_template("mis_estadios.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							estadios_asistidos=estadios_asistidos,
							numero_estadios=len(estadios_asistidos),
							estadios_asistidos_fecha=estadios_asistidos_fecha,
							paises_asistidos=paises_asistidos,
							estadios_competiciones_asistidos=estadios_competiciones_asistidos,
							nombre_mapa_small=nombre_mapa_small,
							nombre_mapa_detalle=nombre_mapa_detalle,
							nombre_mapa_detalle_paises=nombre_mapa_detalle_paises,
							mapas_correcto=mapas_correcto,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_estadio.route("/estadios/mis_estadios/mapa/<nombre_mapa>")
@login_required
def visualizarMapaMisEstadios(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "mapas", "estadios", nombre_mapa)

	return send_file(ruta_mapa)

@bp_estadio.route("/estadios/mis_estadios/<codigo_pais>")
@login_required
def pagina_pais_mis_estadios(codigo_pais:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

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

	vaciarCarpetaMapasUsuario(os.path.join(ruta, "templates", "mapas", "estadios"), current_user.id)

	datos_coordenadas=con.obtenerDatosCoordenadasEstadiosPaisPartidosAsistidosUsuario(current_user.id, codigo_pais, numero_estadios)

	nombre_mapa_small=f"mapa_small_mis_estadios_pais_{codigo_pais}_user_{current_user.id}.html"

	nombre_mapa_detalle=f"mapa_detalle_mis_estadios_pais_{codigo_pais}_user_{current_user.id}.html"

	nombre_mapa_detalle_paises=f"mapa_detalle_paises_mis_estadios_pais_{codigo_pais}_user_{current_user.id}.html"

	mapas_correcto=True

	try:

		centroide=obtenerCentroide(datos_coordenadas)

		crearMapaMisEstadios(os.path.join(ruta, "templates", "mapas", "estadios"), datos_coordenadas, nombre_mapa_small, centroide, 3)

		crearMapaMisEstadiosDetalle(os.path.join(ruta, "templates", "mapas", "estadios"), datos_coordenadas, nombre_mapa_detalle, centroide, 4.5)

		coordenadas=[(dato[1], dato[2]) for dato in datos_coordenadas]

		crearMapaMisEstadiosDetallePaises(os.path.join(ruta, "templates", "mapas", "estadios"), coordenadas, nombre_mapa_detalle_paises, centroide, 4.5)
	
	except Exception as e:

		print(e)
		mapas_correcto=False

	ciudades_estadios_pais=con.obtenerCiudadesEstadiosPaisPartidosAsistidosUsuarioCantidad(current_user.id, codigo_pais, numero_estadios)

	con.cerrarConexion()

	return render_template("mis_estadios_pais.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							codigo_pais=codigo_pais,
							estadios_asistidos_pais=estadios_asistidos_pais,
							numero_estadios_pais=len(estadios_asistidos_pais),
							nombre_pais_seleccionado=nombre_pais_seleccionado,
							paises_no_seleccionados=paises_no_seleccionados,
							nombre_mapa_small=nombre_mapa_small,
							nombre_mapa_detalle=nombre_mapa_detalle,
							nombre_mapa_detalle_paises=nombre_mapa_detalle_paises,
							mapas_correcto=mapas_correcto,
							ciudades_estadios_pais=ciudades_estadios_pais,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_estadio.route("/estadios/mis_estadios_pais/mapa/<nombre_mapa>")
@login_required
def visualizarMapaMisEstadiosPais(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "mapas", "estadios", nombre_mapa)

	return send_file(ruta_mapa)

@bp_estadio.route("/estadios/mis_estadios/partidos_estadio/<estadio_id>")
@login_required
def pagina_mis_estadios_estadio_partidos_estadio(estadio_id:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	partidos_asistidos_estadio=con.obtenerPartidosAsistidosUsuarioEstadio(current_user.id, equipo, estadio_id)

	if not partidos_asistidos_estadio:

		con.cerrarConexion()

		return redirect("/partidos")

	estadio=con.obtenerEstadio(estadio_id)

	resultados_partidos_asistidos_estadio=limpiarResultadosPartidos(partidos_asistidos_estadio)

	con.cerrarConexion()

	return render_template("partidos_asistidos_estadio.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							estadio_id=estadio_id,
							partidos_asistidos_estadio=partidos_asistidos_estadio,
							estadio=estadio,
							numero_partidos_asistidos_estadio=len(partidos_asistidos_estadio),
							resultados_partidos_asistidos_estadio=resultados_partidos_asistidos_estadio,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_estadio.route("/estadios/mis_estadios/division/<codigo_division>")
@login_required
def pagina_division_mis_estadios(codigo_division:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	datos_estadios=con.obtenerDatosEstadios()

	numero_estadios=len(datos_estadios)

	estadios_division=con.obtenerEstadiosCompeticionPartidosAsistidosUsuario(current_user.id, codigo_division, numero_estadios)

	if not estadios_division:

		con.cerrarConexion()

		return redirect("/partidos")

	codigo_logo=con.obtenerCodigoLogoCompeticion(codigo_division)

	estadios_asistidos_division=list(filter(lambda estadio: estadio[5]==1, estadios_division))

	estadios_competiciones_asistidos=con.obtenerEstadiosPartidosAsistidosUsuarioCompeticionCantidad(current_user.id, numero_estadios)

	nombre_division_seleccionado=obtenerNombreDivisionSeleccionado(estadios_competiciones_asistidos, codigo_division)

	divisiones_no_seleccionados=obtenerDivisionesNoSeleccionados(estadios_competiciones_asistidos, codigo_division)

	con.cerrarConexion()

	return render_template("mis_estadios_division.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							codigo_logo=codigo_logo,
							estadios_division=estadios_division,
							numero_estadios=len(estadios_division),
							numero_estadios_asistidos=len(estadios_asistidos_division),
							nombre_division_seleccionado=nombre_division_seleccionado,
							divisiones_no_seleccionados=divisiones_no_seleccionados,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_estadio=URL_DATALAKE_ESTADIOS,
							url_imagen_competicion=URL_DATALAKE_COMPETICIONES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")

@bp_estadio.route("/estadios/mis_estadios/<codigo_pais>/<ciudad>")
@login_required
def pagina_ciudad_mis_estadios(codigo_pais:str, ciudad:str):

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	equipo=con.obtenerEquipo(current_user.id)

	estadio_equipo=con.estadio_equipo(equipo)

	partidos_asistidos_ciudad=con.obtenerPartidosAsistidosUsuarioCiudad(current_user.id, equipo, ciudad, codigo_pais)

	if not partidos_asistidos_ciudad:

		con.cerrarConexion()

		return redirect("/partidos")

	ciudad=con.obtenerCiudad(ciudad, codigo_pais)

	resultados_partidos_asistidos_ciudad=limpiarResultadosPartidos(partidos_asistidos_ciudad)

	con.cerrarConexion()

	return render_template("partidos_asistidos_ciudad.html",
							usuario=current_user.id,
							imagen_perfil=current_user.imagen_perfil,
							equipo=equipo,
							estadio_equipo=estadio_equipo,
							ciudad_id=ciudad,
							codigo_pais=codigo_pais,
							partidos_asistidos_ciudad=partidos_asistidos_ciudad,
							ciudad=ciudad,
							numero_partidos_asistidos_ciudad=len(partidos_asistidos_ciudad),
							resultados_partidos_asistidos_ciudad=resultados_partidos_asistidos_ciudad,
							url_imagen_escudo=URL_DATALAKE_ESCUDOS,
							url_imagen_pais=URL_DATALAKE_PAISES,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_USUARIOS}{current_user.id}/perfil/")