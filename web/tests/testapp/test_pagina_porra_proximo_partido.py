def test_pagina_porra_proximo_partido_sin_login(cliente):

	respuesta=cliente.get("/partido/20200622/porra", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_proximo_partido_proximos_partidos_no_hay(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM proximos_partidos")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20200622/porra")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_porra_proximo_partido_equipo_distinto(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('betis')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO proximos_partidos
											VALUES('202006221', 'betis', 'betis', '2020-06-22', '22:00', 'Liga')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/202006221/porra")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_porra_proximo_partido_porra_disponible(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20200622/porra")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-proximo-partido-detalle">' in contenido
		assert '<div class="info-proximo-partido-detalle">' in contenido
		assert '<div class="porra-proximo-partido">' in contenido
		assert '<p class="competicion">Porra</p>' in contenido
		assert '<p class="competicion">Porra Aun No Disponible</p>' not in contenido

def test_pagina_porra_proximo_partido_porra_no_disponible(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO proximos_partidos
											VALUES ('20210622', 'atletico-madrid', 'atletico-madrid', '2021-06-22', '22:00', 'Liga'),
											('20190622', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga'),
											('20250622', 'atletico-madrid', 'atletico-madrid', '2025-06-22', '22:00', 'Liga')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20200622/porra")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-proximo-partido-detalle">' in contenido
		assert '<div class="info-proximo-partido-detalle">' in contenido
		assert '<div class="porra-proximo-partido">' in contenido
		assert '<p class="competicion">Porra</p>' not in contenido
		assert '<p class="competicion">Porra Aun No Disponible</p>' in contenido