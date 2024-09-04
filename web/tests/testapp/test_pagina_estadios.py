def test_pagina_estadios_sin_login(cliente):

	respuesta=cliente.get("/estadios", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_estadios_estadios_no_existe(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM estadios")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-totales"' in contenido
		assert '<p class="titulo-pagina-estadios">' in contenido
		assert '<div class="tarjetas-estadios-totales">' not in contenido

def test_pagina_estadios_estadios(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-totales"' in contenido
		assert '<p class="titulo-pagina-estadios">' in contenido
		assert '<div class="tarjetas-estadios-totales">' in contenido
		assert '<div class="tarjeta-estadios-top-totales">' in contenido
		assert '<p class="titulo-top-estadios">' in contenido
		assert '<div class="tarjetas-estadios-top-totales">' in contenido

def test_pagina_estadios_estadios_top_no_existen(cliente, conexion_entorno):

	conexion_entorno.c.execute("""UPDATE estadios SET Capacidad=NULL""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-top-totales">' in contenido
		assert '<p class="titulo-top-estadios">' in contenido
		assert '<div class="tarjetas-estadios-top-totales">' not in contenido