from flask import Blueprint, render_template, request, redirect

from src.utilidades.utils import datos_correctos, generarHash, correo_enviado

from src.database.conexion import Conexion

bp_registro=Blueprint("registro", __name__)


@bp_registro.route("/registro")
def registro():

	return render_template("registro.html")

@bp_registro.route("/singin", methods=["POST"])
def singin():

	usuario=request.form.get("usuario")
	nombre=request.form.get("nombre")
	apellido=request.form.get("apellido")
	contrasena=request.form.get("contrasena")
	fecha_nacimiento=request.form.get("fecha-nacimiento")
	equipo=request.form.get("equipo")
	correo=request.form.get("correo")

	if not datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, equipo, correo):

		return redirect("/registro")

	con=Conexion()

	if con.existe_usuario(usuario):

		con.cerrarConexion()

		return redirect("/registro")

	con.insertarUsuario(usuario, correo, generarHash(contrasena), nombre, apellido, fecha_nacimiento, equipo)

	con.cerrarConexion()

	return render_template("singin.html", nombre=nombre, correo_correcto=correo_enviado(correo, nombre), equipo=equipo)