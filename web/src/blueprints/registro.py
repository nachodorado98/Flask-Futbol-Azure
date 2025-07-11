from flask import Blueprint, render_template, request, redirect, jsonify, current_app
import os

from src.utilidades.utils import datos_correctos, generarHash, crearCarpeta

from src.database.conexion import Conexion

from src.kafka.kafka_utils import crearTopic, enviarMensajeKafka
from src.kafka.configkafka import TOPIC


bp_registro=Blueprint("registro", __name__)


@bp_registro.route("/registro")
def registro():

	entorno=current_app.config["ENVIROMENT"]

	con=Conexion(entorno)

	# paises=con.obtenerPaises()
	paises=["España"]

	con.cerrarConexion()

	return render_template("registro.html",
							paises=paises)

@bp_registro.route("/ciudades_pais")
def obtenerCiudadesPais():

	entorno=current_app.config["ENVIROMENT"]

	pais=request.args.get("pais")

	if not pais:
		return jsonify({"error": "No se especificó el pais"}), 400

	con=Conexion(entorno)

	ciudades=con.obtenerCiudadesPais(pais, 25000)

	con.cerrarConexion()

	return jsonify(ciudades) if ciudades else jsonify({"error": "Pais no encontrado"}), 404

@bp_registro.route("/singin", methods=["POST"])
def singin():

	entorno=current_app.config["ENVIROMENT"]

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

	con=Conexion(entorno)

	codigo_ciudad=con.obtenerCodigoCiudad(ciudad)

	if con.existe_usuario(usuario) or not con.existe_equipo(equipo) or not con.existe_codigo_ciudad(codigo_ciudad):

		con.cerrarConexion()

		return redirect("/registro")

	con.insertarUsuario(usuario, correo, generarHash(contrasena), nombre, apellido, fecha_nacimiento, codigo_ciudad, equipo)

	con.cerrarConexion()

	try:

		crearTopic(TOPIC)

		mensaje_correo={"categoria":"correo", "usuario":usuario, "nombre":nombre, "correo":correo}

		correo_correcto=enviarMensajeKafka(TOPIC, mensaje_correo)

	except Exception as e:
		
		print(f"Error en conexion con kafka: {e}")

		correo_correcto=False

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "templates", "imagenes", usuario))

	try:

		mensaje_datalake={"categoria":"datalake_usuario", "usuario":usuario, "entorno":entorno}

		enviarMensajeKafka(TOPIC, mensaje_datalake)

	except Exception as e:

		print(f"Error en conexion con kafka: {e}")

	return render_template("singin.html", nombre=nombre, correo_correcto=correo_correcto, equipo=equipo)