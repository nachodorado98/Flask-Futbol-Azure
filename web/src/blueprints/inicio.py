from flask import Blueprint

from src.database.conexion import Conexion

bp_inicio=Blueprint("inicio", __name__)


@bp_inicio.route("/")
def inicio():

	con=Conexion()

	con.c.execute("SELECT * FROM usuarios")

	usuarios=con.c.fetchall()

	print(usuarios)

	con.cerrarConexion()

	return f"<h1>Hola Mundo</h1>"