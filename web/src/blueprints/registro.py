from flask import Blueprint, render_template, request, redirect, jsonify
import os

from src.utilidades.utils import datos_correctos, generarHash, correo_enviado, crearCarpeta

from src.database.conexion import Conexion

from src.datalake.conexion_data_lake import ConexionDataLake

from src.config import CONTENEDOR

bp_registro=Blueprint("registro", __name__)


@bp_registro.route("/registro")
def registro():

	con=Conexion()

	# paises=con.obtenerPaises()
	paises=["España"]

	con.cerrarConexion()

	return render_template("registro.html",
							paises=paises)

@bp_registro.route("/ciudades_pais")
def obtenerCiudadesPais():

	pais=request.args.get("pais")

	con=Conexion()

	ciudades=con.obtenerCiudadesPais(pais, 25000)

	con.cerrarConexion()

	return jsonify(ciudades)

@bp_registro.route("/singin", methods=["POST"])
def singin():

	usuario=request.form.get("usuario")
	nombre=request.form.get("nombre")
	apellido=request.form.get("apellido")
	contrasena=request.form.get("contrasena")
	fecha_nacimiento=request.form.get("fecha-nacimiento")
	equipo=request.form.get("equipo")
	correo=request.form.get("correo")
	pais=request.form.get("pais")
	ciudad=request.form.get("ciudad")

	if not datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, equipo, correo):

		return redirect("/registro")

	con=Conexion()

	codigo_ciudad=con.obtenerCodigoCiudad(ciudad)

	if con.existe_usuario(usuario) or not con.existe_equipo(equipo) or not con.existe_codigo_ciudad(codigo_ciudad):

		con.cerrarConexion()

		return redirect("/registro")

	con.insertarUsuario(usuario, correo, generarHash(contrasena), nombre, apellido, fecha_nacimiento, codigo_ciudad, equipo)

	con.cerrarConexion()

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "templates", "imagenes", usuario))

	try:

		dl=ConexionDataLake()

		if not dl.existe_carpeta(CONTENEDOR, "usuarios"):

			dl.crearCarpeta(CONTENEDOR, "usuarios")

		dl.crearCarpeta(CONTENEDOR, f"usuarios/{usuario}/perfil")

		dl.crearCarpeta(CONTENEDOR, f"usuarios/{usuario}/imagenes")

		dl.cerrarConexion()

	except Exception as e:

		print(f"Error en conexion con datalake: {e}")

	return render_template("singin.html", nombre=nombre, correo_correcto=correo_enviado(correo, nombre), equipo=equipo)