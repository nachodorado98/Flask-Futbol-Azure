import time
import os

def test_pagina_eliminar_partido_asistido_sin_login(cliente):

	respuesta=cliente.get("/partido/1/asistido/eliminar", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_eliminar_partido_asistido_partido_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/1/asistido/eliminar")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_eliminar_partido_asistido_equipo_no_pertenece(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('equipo-no-partido')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622/asistido/eliminar")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_eliminar_partido_asistido_partido_no_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622/asistido/eliminar")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_eliminar_partido_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		assert conexion_entorno_usuario.obtenerPartidosAsistidosUsuario("nacho98")

		respuesta=cliente_abierto.get("/partido/20190622/asistido/eliminar")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido
		assert not conexion_entorno_usuario.obtenerPartidosAsistidosUsuario("nacho98")

def test_pagina_eliminar_partido_asistido_partido_favorito(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "partido-favorito":"on"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		assert conexion_entorno_usuario.obtenerPartidosAsistidosUsuario("nacho98")
		assert conexion_entorno_usuario.obtenerPartidoAsistidoFavorito("nacho98")

		respuesta=cliente_abierto.get("/partido/20190622/asistido/eliminar")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido
		assert not conexion_entorno_usuario.obtenerPartidosAsistidosUsuario("nacho98")
		assert not conexion_entorno_usuario.obtenerPartidoAsistidoFavorito("nacho98")

def test_pagina_eliminar_partido_asistido_trayectos_partido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Pie", "ciudad-vuelta":"Madrid", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Metro", "teletrabajo":True}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		assert conexion_entorno_usuario.obtenerPartidosAsistidosUsuario("nacho98")

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		trayectos_partido_asistido=conexion_entorno_usuario.c.fetchall()

		assert len(trayectos_partido_asistido)==2

		respuesta=cliente_abierto.get("/partido/20190622/asistido/eliminar")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido
		assert not conexion_entorno_usuario.obtenerPartidosAsistidosUsuario("nacho98")
		
		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_eliminar_partido_asistido_imagen_eliminada(cliente, conexion_entorno_usuario, datalake, entorno):

	datalake.crearCarpeta(entorno, "usuarios/nacho98/imagenes")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/insertar_partido_asistido", data=data, buffered=True, content_type="multipart/form-data")
		
		archivos_datalake=datalake.obtenerArchivosCarpeta(entorno, "usuarios/nacho98/imagenes")
		
		assert "nacho98_20190622.jpeg" in archivos_datalake

		respuesta=cliente_abierto.get("/partido/20190622/asistido/eliminar")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido
		assert not conexion_entorno_usuario.obtenerPartidosAsistidosUsuario("nacho98")

		time.sleep(12)

		archivos_datalake_nuevos=datalake.obtenerArchivosCarpeta(entorno, "usuarios/nacho98/imagenes")
		
		assert "nacho98_20190622.jpeg" not  in archivos_datalake_nuevos

		datalake.eliminarCarpeta(entorno, "usuarios/nacho98")

		datalake.cerrarConexion()