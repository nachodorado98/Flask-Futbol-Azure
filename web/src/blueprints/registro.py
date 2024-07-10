from flask import Blueprint, render_template, request, redirect

from src.utilidades.utils import datos_correctos, generarHash

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

	if not datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, equipo):

		return redirect("/registro")

	con=Conexion()

	if con.existe_usuario(usuario):

		con.cerrarConexion()

		return redirect("/registro")

	con.insertarUsuario(usuario, generarHash(contrasena), nombre, apellido, fecha_nacimiento, equipo)

	con.cerrarConexion()

	return render_template("singin.html", nombre=nombre)