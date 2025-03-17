import pytest
import os

from src.utilidades.utils import vaciarCarpeta
from src.config import CONTENEDOR

def test_pagina_partido_asistido_sin_login(cliente):

	respuesta=cliente.get("/partido/1/asistido", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_partido_asistido_partido_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/1/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_asistido_equipo_no_pertenece(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('equipo-no-partido')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_asistido_partido_no_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_asistido_con_comentario(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="info-partido-asistido-detalle">' in contenido
		assert '<div class="contenedor-comentario">' in contenido
		assert '<div class="comentario">' in contenido
		assert '<h2 class="no-comentario">' not in contenido
		assert '<div class="seccion-comentar-partido-asistido"' not in contenido
		assert "/no_favorito_asistido.png" in contenido
		assert "/favorito_asistido.png" not in contenido
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' not in contenido
		assert '<div class="seccion-on-tour-partido-asistido">' not in contenido

def test_pagina_partido_asistido_sin_comentario(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":""}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="info-partido-asistido-detalle">' in contenido
		assert '<div class="contenedor-comentario">' in contenido
		assert '<div class="comentario">' not in contenido
		assert '<h2 class="no-comentario">' in contenido
		assert '<div class="seccion-comentar-partido-asistido"' in contenido
		assert "/no_favorito_asistido.png" in contenido
		assert "/favorito_asistido.png" not in contenido
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' not in contenido
		assert '<div class="seccion-on-tour-partido-asistido">' not in contenido

def test_pagina_partido_asistido_sin_imagen(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="info-partido-asistido-detalle">' in contenido
		assert '<div class="contenedor-imagen">' in contenido
		assert '<div class="imagen">' not in contenido
		assert '<div class="contenedor-subir-imagen">' in contenido
		assert '<div class="botones-anadir-imagen-partido-asistido">' in contenido

def test_pagina_partido_asistido_con_imagen(cliente, conexion_entorno, datalake):

	datalake.crearCarpeta(CONTENEDOR, "usuarios/nacho98/imagenes")

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad": "Madrid", "equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/insertar_partido_asistido", data=data, buffered=True, content_type="multipart/form-data")

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="info-partido-asistido-detalle">' in contenido
		assert '<div class="contenedor-imagen">' in contenido
		assert '<div class="imagen">' in contenido
		assert '<div class="contenedor-subir-imagen">' not in contenido
		assert '<div class="botones-anadir-imagen-partido-asistido">' not in contenido
		assert "/nacho98_20190622.jpeg" in contenido

		datalake.eliminarCarpeta(CONTENEDOR, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		vaciarCarpeta(ruta_carpeta_imagenes)

@pytest.mark.parametrize(["fecha_ida", "fecha_vuelta", "fecha_ida_on_tour", "fecha_vuelta_on_tour"],
	[
		("2019-06-21", "2019-06-23", "21-06-2019", "23-06-2019"),
		("2019-06-22", "2019-06-22", "22-06-2019", "22-06-2019"),
		("2019-04-13", "2019-06-23", "13-04-2019", "23-06-2019"),
		("2019-06-21", "2019-07-22", "21-06-2019", "22-07-2019"),
		("2009-06-21", "2029-06-23", "21-06-2009", "23-06-2029")
	]
)
def test_pagina_partido_asistido_con_on_tour(cliente, conexion_entorno_usuario, fecha_ida, fecha_vuelta, fecha_ida_on_tour, fecha_vuelta_on_tour):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "fecha-ida":fecha_ida, "fecha-vuelta":fecha_vuelta}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="seccion-on-tour-partido-asistido">' in contenido
		assert '<div class="contenedor-titulo-on-tour-partido-asistido">' in contenido
		assert '<div class="contenedor-fechas-on-tour-partido-asistido">' in contenido
		assert f"Fecha Ida: {fecha_ida_on_tour}" in contenido
		assert f"Fecha Vuelta: {fecha_vuelta_on_tour}" in contenido
		assert '<p class="teletrabajo-on-tour">' in contenido

def test_pagina_partido_asistido_con_on_tour_sin_teletrabajo(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "fecha-ida":"2019-06-21", "fecha-vuelta":"2019-06-23"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="seccion-on-tour-partido-asistido">' in contenido
		assert '<div class="contenedor-titulo-on-tour-partido-asistido">' in contenido
		assert '<div class="contenedor-fechas-on-tour-partido-asistido">' in contenido
		assert '<p class="teletrabajo-on-tour">' in contenido
		assert "Teletrabajo No" in contenido
		assert "Teletrabajo Si" not in contenido

def test_pagina_partido_asistido_con_on_tour_con_teletrabajo(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "fecha-ida":"2019-06-21", "fecha-vuelta":"2019-06-23", "teletrabajo":True}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="seccion-on-tour-partido-asistido">' in contenido
		assert '<div class="contenedor-titulo-on-tour-partido-asistido">' in contenido
		assert '<div class="contenedor-fechas-on-tour-partido-asistido">' in contenido
		assert '<p class="teletrabajo-on-tour">' in contenido
		assert "Teletrabajo No" not in contenido
		assert "Teletrabajo Si" in contenido

def test_pagina_partido_asistido_no_partido_anterior_no_partido_siguiente(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":""})

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior-asistido"' not in contenido
		assert '<button class="button-partido-siguiente-asistido"' not in contenido

def test_pagina_partido_asistido_no_partido_anterior_si_partido_siguiente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":""})

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20245964", "comentario":""})

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior-asistido"' not in contenido
		assert '<button class="button-partido-siguiente-asistido"' in contenido

def test_pagina_partido_asistido_si_partido_anterior_no_partido_siguiente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":""})

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20245964", "comentario":""})

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior-asistido"' in contenido
		assert '<button class="button-partido-siguiente-asistido"' not in contenido

def test_pagina_partido_asistido_si_partido_anterior_si_partido_siguiente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
									VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria'),
										('202454564', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":""})

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20245964", "comentario":""})

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"202454564", "comentario":""})

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior-asistido"' in contenido
		assert '<button class="button-partido-siguiente-asistido"' in contenido

def test_pagina_partido_asistido_partido_asistido_favorito(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "partido-favorito":"on"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "/no_favorito_asistido.png" not in contenido
		assert "/favorito_asistido.png" in contenido
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' in contenido

def test_pagina_partido_asistido_ventana_emergente_papelera_disponible(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "partido-favorito":"on"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="papelera-partido-asistido"' in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert "/partido/20190622/asistido/eliminar" in contenido