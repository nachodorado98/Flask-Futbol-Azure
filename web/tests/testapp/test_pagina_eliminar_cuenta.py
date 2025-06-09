import os
import time

from src.utilidades.utils import vaciarCarpeta

def test_pagina_eliminar_cuenta_sin_login(cliente, conexion):

	respuesta=cliente.get("/settings/eliminar_cuenta", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_eliminar_cuenta(cliente, conexion_entorno, datalake, entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.es", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1999-07-16", "ciudad":"Madrid", "equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.get("/settings/eliminar_cuenta", follow_redirects=True)

		conexion_entorno.c.execute("SELECT * FROM usuarios")

		assert not conexion_entorno.c.fetchall()

		time.sleep(12)

		assert not datalake.existe_carpeta(entorno, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

		vaciarCarpeta(ruta_carpeta_imagenes)