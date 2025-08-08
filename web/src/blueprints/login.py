from flask import Blueprint, request, redirect, render_template, current_app
from flask_login import login_user, login_required, current_user, logout_user
from typing import Optional
import datetime

from src.extensiones.manager import login_manager

from src.modelos.usuario import Usuario

from src.database.conexion import Conexion

from src.utilidades.utils import comprobarHash


bp_login=Blueprint("login", __name__)


# Funcion para comprobar y cargar  el usuario 
@login_manager.user_loader
def cargarUsuario(usuario:str)->Optional[Usuario]:

	entorno=current_app.config["ENVIROMENT"]	

	con=Conexion(entorno)

	if not con.existe_usuario(usuario):

		con.cerrarConexion()

		return None

	nombre=con.obtenerNombre(usuario)

	imagen_perfil=con.obtenerImagenPerfilUsuario(usuario)

	con.cerrarConexion()

	return Usuario(usuario, nombre, imagen_perfil)

@bp_login.route("/login", methods=["GET", "POST"])
def login():

	entorno=current_app.config["ENVIROMENT"]

	usuario=request.form.get("usuario")
	contrasena=request.form.get("contrasena")

	con=Conexion(entorno)

	if not con.existe_usuario(usuario):

		con.cerrarConexion()

		return redirect("/")

	contrasena_hash_usuario=con.obtenerContrasenaUsuario(usuario)

	if not comprobarHash(contrasena, contrasena_hash_usuario):

		con.cerrarConexion()

		return redirect("/")

	nombre=con.obtenerNombre(usuario)

	imagen_perfil=con.obtenerImagenPerfilUsuario(usuario)

	con.cerrarConexion()

	usuario=Usuario(usuario, nombre, imagen_perfil)

	login_user(usuario)

	siguiente=request.args.get("next")

	return redirect(siguiente or "/partidos?login=True")

@bp_login.route("/logout")
@login_required
def logout():

	logout_user()

	return redirect("/")