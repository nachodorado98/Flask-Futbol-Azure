def test_pagina_entrenador_sin_login(cliente):

	respuesta=cliente.get("/entrenador/entrenador", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_entrenador_entrenador_no_existe(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)
		
		respuesta=cliente_abierto.get("/entrenador/entrenador")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_entrenador_entrenador(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

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

def test_pagina_entrenador_entrenador_sin_equipo(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""UPDATE entrenadores SET equipo_id=NULL""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/entrenador/diego-pablo")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-entrenador-imagenes">' in contenido
		assert '<div class="info-entrenador-equipo"' not in contenido

def test_pagina_entrenador_entrenador_sin_puntuacion(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""UPDATE entrenadores SET puntuacion=NULL""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/entrenador/diego-pablo")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-entrenador-imagenes">' in contenido
		assert '<div class="info-entrenador-puntuacion">' not in contenido