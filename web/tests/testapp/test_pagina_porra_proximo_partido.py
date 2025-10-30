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
		assert '<div class="porra-proximo-partido">' in contenido
		assert '<h4 class="titulo-porra">LA PORRA</h4>' in contenido
		assert '<div class="resultado-container">' in contenido
		assert '<div class="resultado-container-porra-hecha">' not in contenido
		assert '<input type="number" id="goles_local" name="goles_local" value="1"' not in contenido
		assert '<input type="number" id="goles_visitante" name="goles_visitante" value="0"' not in contenido
		assert '<div id="goleadores-container"' in contenido
		assert '<div class="contenedor-lateral contenedor-lateral-izq">' not in contenido
		assert '<div class="tarjeta-mas-porras">' not in contenido
		assert '<div class="tarjetas-mas-porras">' not in contenido
		assert '<div class="tarjeta-porra-usuario">' not in contenido

def test_pagina_porra_proximo_partido_porra_existente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.insertarPorraPartido("nacho98", "20200622", 1, 0)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20200622/porra")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-proximo-partido-detalle">' in contenido
		assert '<div class="porra-proximo-partido">' in contenido
		assert '<h4 class="titulo-porra">LA PORRA</h4>' in contenido
		assert '<div class="resultado-container">' not in contenido
		assert '<div class="resultado-container-porra-hecha">' in contenido
		assert '<input type="number" id="goles_local" name="goles_local" value="1"' in contenido
		assert '<input type="number" id="goles_visitante" name="goles_visitante" value="0"' in contenido
		assert '<div id="goleadores-container"' not in contenido
		assert '<div class="contenedor-lateral contenedor-lateral-izq">' not in contenido
		assert '<div class="tarjeta-mas-porras">' not in contenido
		assert '<div class="tarjetas-mas-porras">' not in contenido
		assert '<div class="tarjeta-porra-usuario">' not in contenido

def test_pagina_porra_proximo_partido_mas_porras(cliente, conexion_entorno_usuario, password_hash):

	conexion_entorno_usuario.insertarUsuario("amanda", "amanda@gmail.com", password_hash, "amanda", "aranda", "1999-08-06", 103, "atletico-madrid")

	conexion_entorno_usuario.insertarPorraPartido("nacho98", "20200622", 1, 0)

	conexion_entorno_usuario.insertarPorraPartido("amanda", "20200622", 3, 0)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20200622/porra")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="contenedor-lateral contenedor-lateral-izq">' in contenido
		assert '<div class="tarjeta-mas-porras">' in contenido
		assert '<div class="tarjetas-mas-porras">' in contenido
		assert '<div class="tarjeta-porra-usuario">' in contenido
		assert '<strong>amanda</strong>' in contenido
		assert '<h4>3 - 0</h4>' in contenido