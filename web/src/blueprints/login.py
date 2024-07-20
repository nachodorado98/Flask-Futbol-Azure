from flask import Blueprint, request, redirect, render_template
from flask_login import login_user, login_required, current_user, logout_user
from typing import Optional

from src.extensiones.manager import login_manager

from src.modelos.usuario import Usuario

from src.database.conexion import Conexion

from src.utilidades.utils import comprobarHash


bp_login=Blueprint("login", __name__)


# Funcion para comprobar y cargar  el usuario 
@login_manager.user_loader
def cargarUsuario(usuario:str)->Optional[Usuario]:

	con=Conexion()

	if not con.existe_usuario(usuario):

		con.cerrarConexion()

		return None

	nombre=con.obtenerNombre(usuario)

	con.cerrarConexion()

	return Usuario(usuario, nombre)


@bp_login.route("/login", methods=["GET", "POST"])
def login():

	usuario=request.form.get("usuario")
	contrasena=request.form.get("contrasena")

	con=Conexion()

	if not con.existe_usuario(usuario):

		con.cerrarConexion()

		return redirect("/")

	contrasena_hash_usuario=con.obtenerContrasenaUsuario(usuario)

	if not comprobarHash(contrasena, contrasena_hash_usuario):

		con.cerrarConexion()

		return redirect("/")

	nombre=con.obtenerNombre(usuario)

	con.cerrarConexion()

	usuario=Usuario(usuario, nombre)

	login_user(usuario)

	siguiente=request.args.get("next")

	return redirect(siguiente or "/partidos")


@bp_login.route("/partidos")
@login_required
def pagina_partidos():

	con=Conexion()

	equipo=con.obtenerEquipo(current_user.id)

	nombre_equipo=con.obtenerNombreEquipo(equipo)

	partidos=con.obtenerPartidosEquipo(equipo)

	con.cerrarConexion()

	return render_template("partidos.html",
							usuario=current_user.id,
							equipo=equipo,
							nombre_equipo=nombre_equipo,
							partidos=partidos)


@bp_login.route("/logout")
@login_required
def logout():

	logout_user()

	return redirect("/")