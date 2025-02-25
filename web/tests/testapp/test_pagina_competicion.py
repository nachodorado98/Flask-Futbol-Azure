def test_pagina_competicion_sin_login(cliente):

	respuesta=cliente.get("/competicion/competicion", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_competicion_competicion_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competicion/competicion")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_competicion_competicion(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competicion/primera")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-competicion">' in contenido
		assert '<p class="nombre">' in contenido
		assert '<img class="pais-competicion"' in contenido
		assert '<img class="logo-competicion"' in contenido
		assert '<p class="titulo-equipos-competicion">' in contenido
		assert '<div class="tarjetas-equipos-competicion">' in contenido
		assert '<p class="titulo-campeones-competicion">' in contenido
		assert '<div class="tarjetas-campeones-competicion">' in contenido
		assert '<p class="titulo-partidos-competicion">' in contenido
		assert '<div class="tarjetas-partidos-competicion">' in contenido

def test_pagina_competicion_competicion_sin_equipos(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE equipos SET codigo_competicion='segunda'""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competicion/primera")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<p class="titulo-equipos-competicion">' not in contenido
		assert '<div class="tarjetas-equipos-competicion">' not in contenido

def test_pagina_competicion_competicion_sin_campeones(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM competiciones_campeones""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competicion/primera")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<p class="titulo-campeones-competicion">' not in contenido
		assert '<div class="tarjetas-campeones-competicion">' not in contenido

def test_pagina_competicion_competicion_sin_partidos(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM partido_competicion""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competicion/primera")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<p class="titulo-partidos-competicion">' not in contenido
		assert '<div class="tarjetas-partidos-competicion">' not in contenido