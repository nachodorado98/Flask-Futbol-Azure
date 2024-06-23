from flask import Blueprint

bp=Blueprint("blueprint", __name__)

# Vista de la pagina principal
@bp.route("/", methods=["GET"])
def inicio()->str:

	return f"<h1>Hola Mundo</h1>"