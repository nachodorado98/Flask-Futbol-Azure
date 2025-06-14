import os

def test_pagina_actualizar_imagen_perfil_usuario_sin_login(cliente):

	respuesta=cliente.post("/settings/actualizar_imagen_perfil", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_actualizar_imagen_perfil_usuario_con_imagen_no_valida(cliente, conexion_entorno_usuario, datalake, entorno):

	datalake.crearCarpeta(entorno, "usuarios/nacho98/perfil")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests_no_valida.txt")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests_no_valida.txt")

			respuesta=cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "Redirecting..." in contenido
		
		assert datalake.existe_carpeta(entorno, "usuarios/nacho98/perfil")

		objeto_archivo_imagen=datalake.obtenerFile(entorno, "usuarios/nacho98/perfil", "nacho98_perfil.txt")

		assert not objeto_archivo_imagen.exists()

		datalake.eliminarCarpeta(entorno, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "perfil", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_perfil.txt")

		assert not os.path.exists(ruta_imagen)

def test_pagina_actualizar_imagen_perfil_usuario_con_imagen(cliente, conexion_entorno_usuario, datalake, entorno):

	datalake.crearCarpeta(entorno, "usuarios/nacho98/perfil")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			respuesta=cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "Redirecting..." in contenido
		
		assert datalake.existe_carpeta(entorno, "usuarios/nacho98/perfil")

		objeto_archivo_imagen=datalake.obtenerFile(entorno, "usuarios/nacho98/perfil", "nacho98_perfil.jpeg")

		assert objeto_archivo_imagen.exists()

		datalake.eliminarCarpeta(entorno, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "perfil", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_perfil.jpeg")

		assert not os.path.exists(ruta_imagen)