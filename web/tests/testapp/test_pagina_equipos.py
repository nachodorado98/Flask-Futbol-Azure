def test_pagina_equipos_sin_login(cliente):

	respuesta=cliente.get("/equipos", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_equipos_equipos_no_existe(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno.c.execute("""DELETE FROM equipos""")

		conexion_entorno.confirmar()

		respuesta=cliente_abierto.get("/equipos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location==r"/login?next=%2Fequipos"
		assert "Redirecting..." in contenido

def test_pagina_equipos_equipos(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-equipos-totales' in contenido
		assert '<p class="titulo-pagina-equipos">' in contenido
		assert '<div class="tarjetas-equipos-totales">' in contenido
		assert '<div class="tarjeta-equipos-top-totales">' in contenido
		assert '<p class="titulo-top-equipos">' in contenido
		assert '<div class="tarjetas-equipos-top-totales">' in contenido

def test_pagina_equipos_equipos_top_no_existen(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""UPDATE equipos SET Puntuacion=NULL""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-equipos-totales' in contenido
		assert '<p class="titulo-pagina-equipos">' in contenido
		assert '<div class="tarjetas-equipos-totales">' in contenido
		assert '<div class="tarjeta-equipos-top-totales">' in contenido
		assert '<p class="titulo-top-equipos">' in contenido
		assert '<div class="tarjetas-equipos-top-totales">' not in contenido