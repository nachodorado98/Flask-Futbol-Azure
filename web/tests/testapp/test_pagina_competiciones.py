def test_pagina_competiciones_sin_login(cliente):

	respuesta=cliente.get("/competiciones", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_competiciones_competiciones_no_existe(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM competiciones")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-competiciones-totales"' in contenido
		assert '<p class="titulo-pagina-competiciones">' in contenido
		assert '<div class="tarjetas-competiciones-totales">' not in contenido

def test_pagina_competiciones_competiciones(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-competiciones-totales"' in contenido
		assert '<p class="titulo-pagina-competiciones">' in contenido
		assert '<div class="tarjetas-competiciones-totales">' in contenido
		assert '<div class="tarjeta-competiciones-top-totales">' in contenido
		assert '<p class="titulo-top-competiciones">' in contenido
		assert '<div class="tarjetas-competiciones-top-totales">' in contenido

def test_pagina_competiciones_competiciones_top_no_existen(cliente, conexion_entorno):

	conexion_entorno.c.execute("""UPDATE equipos SET Puntuacion=NULL""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-competiciones-top-totales">' in contenido
		assert '<p class="titulo-top-competiciones">' in contenido
		assert '<div class="tarjetas-competiciones-top-totales">' not in contenido