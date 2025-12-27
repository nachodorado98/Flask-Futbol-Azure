import os

def test_pagina_settings_sin_login(cliente):

	respuesta=cliente.get("/settings", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_settings_sin_imagen_perfil(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente.get("/settings", follow_redirects=True)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-configuracion">' in contenido
		assert '<p class="titulo-pagina-configuracion">' in contenido
		assert '<div class="contenedor-imagen-perfil">' in contenido
		assert '<div class="contenedor-subir-imagen">' in contenido
		assert '<div class="contenedor-imagen" id="contenedorImagen">' not in contenido
		assert '<div class="seccion-actualizar-imagen-perfil"' not in contenido
		assert '<div class="contenedor-configuracion">' in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido

def test_pagina_settings_con_imagen_perfil(cliente, conexion_entorno_usuario, datalake, entorno):

	# datalake.crearCarpeta(entorno, "usuarios/nacho98/perfil")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		respuesta=cliente.get("/settings", follow_redirects=True)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-configuracion">' in contenido
		assert '<p class="titulo-pagina-configuracion">' in contenido
		assert '<div class="contenedor-imagen-perfil">' in contenido
		assert '<div class="contenedor-subir-imagen">' in contenido
		assert '<div class="contenedor-imagen" id="contenedorImagen">' in contenido
		assert '<img class="imagen-perfil"' in contenido
		assert "/nacho98_perfil.jpeg" in contenido
		assert '<div class="seccion-actualizar-imagen-perfil"' in contenido
		assert '<div class="contenedor-configuracion">' in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido

		datalake.eliminarCarpeta(entorno, "usuarios/nacho98")

		datalake.cerrarConexion()