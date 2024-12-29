def test_pagina_anadir_partido_asistido_favorito_sin_login(cliente):

	respuesta=cliente.get("/partido/1/asistido/anadir_partido_favorito", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_anadir_partido_asistido_favorito_partido_no_existe(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/1/asistido/anadir_partido_favorito")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_anadir_partido_asistido_favorito_equipo_no_pertenece(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('equipo-no-partido')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622/asistido/anadir_partido_favorito")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_anadir_partido_asistido_favorito_partido_no_asistido(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622/asistido/anadir_partido_favorito")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_anadir_partido_asistido_favorito(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		assert "/no_favorito_asistido.png" in contenido
		assert "/favorito_asistido.png" not in contenido
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' not in contenido

		cliente_abierto.get("/partido/20190622/asistido/anadir_partido_favorito")

		respuesta2=cliente_abierto.get("/partido/20190622/asistido")

		contenido2=respuesta2.data.decode()

		assert "/no_favorito_asistido.png" not in contenido2
		assert "/favorito_asistido.png" in contenido2
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' in contenido2

def test_pagina_anadir_partido_asistido_favorito_partido_favorito_existe(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190623", "comentario":"Comentario", "partido-favorito":"on"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		assert "/no_favorito_asistido.png" in contenido
		assert "/favorito_asistido.png" not in contenido
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' not in contenido

		cliente_abierto.get("/partido/20190622/asistido/anadir_partido_favorito")

		respuesta2=cliente_abierto.get("/partido/20190622/asistido")

		contenido2=respuesta2.data.decode()

		assert "/no_favorito_asistido.png" not in contenido2
		assert "/favorito_asistido.png" in contenido2
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' in contenido2

		respuesta3=cliente_abierto.get("/partido/20190623/asistido")

		contenido3=respuesta3.data.decode()

		assert "/no_favorito_asistido.png" in contenido3
		assert "/favorito_asistido.png" not in contenido3
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' not in contenido3