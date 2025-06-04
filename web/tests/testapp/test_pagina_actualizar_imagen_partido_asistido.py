import os

from src.utilidades.utils import vaciarCarpeta

def test_pagina_actualizar_imagen_partido_asistido_sin_login(cliente):

	ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

	data={}

	with open(ruta_imagen_test, "rb") as imagen_file:
		
		data["imagen"]=(imagen_file, "imagen_tests.jpeg")

		respuesta=cliente.post("/actualizar_imagen_partido_asistido/20190622", data=data, buffered=True, content_type="multipart/form-data", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_actualizar_imagen_partido_asistido_partido_no_existente(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			respuesta=cliente_abierto.post("/actualizar_imagen_partido_asistido/no_existo", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

def test_pagina_actualizar_imagen_partido_asistido_partido_asistido_no_existente(cliente, conexion_entorno_usuario):
	
	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			respuesta=cliente_abierto.post("/actualizar_imagen_partido_asistido/no_existo", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_actualizar_imagen_partido_asistido_imagen_no_valida(cliente, conexion_entorno_usuario, datalake, entorno):

	datalake.crearCarpeta(entorno, "usuarios/nacho98/imagenes")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":"Comentario"})

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests_no_valida.txt")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests_no_valida.txt")

			respuesta=cliente_abierto.post("/actualizar_imagen_partido_asistido/20190622", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partido/20190622/asistido"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		partidos=conexion_entorno_usuario.c.fetchall()

		assert len(partidos)==1
		assert partidos[0]["imagen"] is None
		
		assert datalake.existe_carpeta(entorno, "usuarios/nacho98/imagenes")

		objeto_archivo_imagen=datalake.obtenerFile(entorno, "usuarios/nacho98/imagenes", "nacho98_20190622.txt")

		assert not objeto_archivo_imagen.exists()

		datalake.eliminarCarpeta(entorno, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.txt")

		assert not os.path.exists(ruta_imagen)

def test_pagina_actualizar_imagen_partido_asistido(cliente, conexion_entorno_usuario, datalake, entorno):

	datalake.crearCarpeta(entorno, "usuarios/nacho98/imagenes")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":"Comentario"})

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			respuesta=cliente_abierto.post("/actualizar_imagen_partido_asistido/20190622", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partido/20190622/asistido"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		partidos=conexion_entorno_usuario.c.fetchall()

		assert len(partidos)==1
		assert partidos[0]["imagen"]=="nacho98_20190622.jpeg"
		
		assert datalake.existe_carpeta(entorno, "usuarios/nacho98/imagenes")

		objeto_archivo_imagen=datalake.obtenerFile(entorno, "usuarios/nacho98/imagenes", "nacho98_20190622.jpeg")

		assert objeto_archivo_imagen.exists()

		datalake.eliminarCarpeta(entorno, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.jpeg")

		assert not os.path.exists(ruta_imagen)

def test_pagina_actualizar_imagen_partido_asistido_sin_imagen(cliente, conexion_entorno_usuario, datalake, entorno):

	datalake.crearCarpeta(entorno, "usuarios/nacho98/imagenes")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":"Comentario"})

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={}

		respuesta=cliente_abierto.post("/actualizar_imagen_partido_asistido/20190622", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partido/20190622/asistido"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		partidos=conexion_entorno_usuario.c.fetchall()

		assert len(partidos)==1
		assert partidos[0]["imagen"] is None
		
		assert datalake.existe_carpeta(entorno, "usuarios/nacho98/imagenes")

		objeto_archivo_imagen=datalake.obtenerFile(entorno, "usuarios/nacho98/imagenes", "nacho98_20190622.jpeg")

		assert not objeto_archivo_imagen.exists()

		datalake.eliminarCarpeta(entorno, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.jpeg")

		assert not os.path.exists(ruta_imagen)