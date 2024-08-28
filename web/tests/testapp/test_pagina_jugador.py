def test_pagina_jugador_sin_login(cliente):

	respuesta=cliente.get("/jugador/jugador", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_jugador_jugador_no_existe(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/jugador/jugador")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_jugador_jugador(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/jugador/julian-alvarez")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-jugador"' in contenido
		assert '<p class="nombre">' in contenido
		assert '<img class="pais-jugador"' in contenido
		assert '<img class="jugador"' in contenido
		assert '<div class="info-jugador-imagenes">' in contenido
		assert '<div class="info-jugador-equipo"' in contenido
		assert '<div class="info-jugador-puntuacion">' in contenido
		assert '<div class="info-jugador-dorsal">' in contenido
		assert '<div class="info-jugador-posicion">' in contenido

def test_pagina_jugador_jugador_sin_equipo(cliente, conexion_entorno):

	conexion_entorno.c.execute("""UPDATE jugadores SET equipo_id=NULL""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/jugador/julian-alvarez")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-jugador-imagenes">' in contenido
		assert '<div class="info-jugador-equipo"' not in contenido

def test_pagina_jugador_jugador_sin_puntuacion(cliente, conexion_entorno):

	conexion_entorno.c.execute("""UPDATE jugadores SET puntuacion=NULL""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/jugador/julian-alvarez")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-jugador-imagenes">' in contenido
		assert '<div class="info-jugador-puntuacion">' not in contenido

def test_pagina_jugador_jugador_sin_dorsal(cliente, conexion_entorno):

	conexion_entorno.c.execute("""UPDATE jugadores SET dorsal=NULL""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/jugador/julian-alvarez")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-jugador-imagenes">' in contenido
		assert '<div class="info-jugador-dorsal">' not in contenido

def test_pagina_jugador_jugador_sin_posicion(cliente, conexion_entorno):

	conexion_entorno.c.execute("""UPDATE jugadores SET posicion=NULL""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/jugador/julian-alvarez")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-jugador-imagenes">' in contenido
		assert '<div class="info-jugador-posicion">' not in contenido