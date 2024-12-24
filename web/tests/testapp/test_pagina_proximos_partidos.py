def test_pagina_proximos_partidos_sin_login(cliente):

	respuesta=cliente.get("/partidos/proximos", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_proximos_partidos_proximos_partidos_no_hay(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM proximos_partidos")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/proximos")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_proximos_partidos_proximos_partidos(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/proximos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "Proximos Partidos del " in contenido
		assert '<div class="tarjetas-proximos-partidos">' in contenido
		assert '<div class="tarjetas-proximos-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-proximo-partido"' in contenido
		assert '<div class="info-proximo-partido">' in contenido