def test_pagina_entrenador_sin_login(cliente):

	respuesta=cliente.get("/entrenador/entrenador", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_entrenador_entrenador_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)
		
		respuesta=cliente_abierto.get("/entrenador/entrenador")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_entrenador_entrenador(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)
		
		respuesta=cliente_abierto.get("/entrenador/diego-pablo")
		
		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-entrenador"' in contenido
		assert '<p class="nombre">' in contenido
		assert '<img class="pais-entrenador"' in contenido
		assert '<img class="entrenador"' in contenido
		assert '<div class="info-entrenador-imagenes">' in contenido
		assert '<div class="info-entrenador-equipo"' in contenido
		assert '<div class="info-entrenador-puntuacion">' in contenido
		assert '<div class="tarjeta-equipos-entrenador">' in contenido
		assert '<div class="tarjetas-equipos-entrenador-wrapper">' in contenido
		assert '<div class="tarjeta-palmares-entrenador">' in contenido
		assert '<p class="titulo-palmares-entrenador">' in contenido
		assert '<div class="tarjetas-palmares-entrenador">' in contenido

def test_pagina_entrenador_entrenador_sin_equipo(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE entrenadores SET equipo_id=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/entrenador/diego-pablo")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-entrenador-imagenes">' in contenido
		assert '<div class="info-entrenador-equipo"' not in contenido

def test_pagina_entrenador_entrenador_sin_puntuacion(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE entrenadores SET puntuacion=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/entrenador/diego-pablo")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-entrenador-imagenes">' in contenido
		assert '<div class="info-entrenador-puntuacion">' not in contenido

def test_pagina_entrenador_entrenador_sin_titulos(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM entrenador_titulo""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/entrenador/diego-pablo")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-palmares-entrenador">' not in contenido
		assert '<p class="titulo-palmares-entrenador">' not in contenido
		assert '<div class="tarjetas-palmares-entrenador">' not in contenido