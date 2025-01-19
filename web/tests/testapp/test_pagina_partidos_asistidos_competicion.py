def test_pagina_partidos_asistidos_competicion_sin_login(cliente):

	respuesta=cliente.get("/competiciones/mis_competiciones/partidos_competicion/primera", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_partidos_asistidos_competicion_sin_partidos(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_asistidos_competicion_sin_partidos_asistidos(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_asistidos_competicion_sin_competiciones(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("DELETE FROM competiciones")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_asistidos_competicion_con_partido_asistido(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos en " in contenido
		assert '<div class="contenedor-titulo-partidos-asistidos-competicion">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-partidos-asistidos-competicion">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-competicion-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos-competicion"' in contenido
		assert '<div class="info-partido-asistidos-competicion">' in contenido