def test_pagina_proximos_partidos_sin_login(cliente):

	respuesta=cliente.get("/partidos/proximos", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_proximos_partidos_proximos_partidos_no_hay(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM proximos_partidos")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/proximos")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_proximos_partidos_proximo_partido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/proximos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "Proximos Partidos del " in contenido
		assert '<div class="tarjetas-proximos-partidos">' in contenido
		assert '<div class="tarjetas-proximos-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-proximo-partido"' in contenido
		assert '<div class="info-proximo-partido">' in contenido
		assert '<a href="/partidos/calendario/2020-06?proximos_partidos=True" class="tipo-partidos-calendario">' in contenido

def test_pagina_proximos_partidos_calendario_solo_un_proximo_partido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/proximos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<a href="/partidos/calendario/2020-06?proximos_partidos=True" class="tipo-partidos-calendario">' in contenido

def test_pagina_proximos_partidos_calendario_varios(cliente, conexion, password_hash):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO proximos_partidos
							VALUES ('20190502', 'atletico-madrid', 'rival', '2019-06-02', '22:00', 'Primera'),
									('20190101', 'rival', 'atletico-madrid', '2019-07-01', '22:00', 'Liga'),
									('20190703', 'rival', 'atletico-madrid', '2019-06-03', '22:00', 'Liga'),
									('20191222', 'rival', 'atletico-madrid', '2020-06-12', '22:00', 'Liga'),
									('20190601', 'rival', 'atletico-madrid', '2021-06-21', '22:00', 'Liga'),
									('20190806', 'rival', 'atletico-madrid', '2019-06-26', '22:00', 'Liga')""")
	
	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/proximos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<a href="/partidos/calendario/2019-06?proximos_partidos=True" class="tipo-partidos-calendario">' in contenido