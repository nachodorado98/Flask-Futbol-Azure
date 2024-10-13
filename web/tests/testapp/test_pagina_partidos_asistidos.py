import pytest

def test_pagina_partidos_asistidos_sin_login(cliente):

	respuesta=cliente.get("/partidos/asistidos", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_partidos_asistidos_sin_partidos(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/asistidos", follow_redirects=True)
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " in contenido
		assert '<div class="tarjetas-partidos-asistidos">' not in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido-asistidos"' not in contenido
		assert '<div class="info-partido-asistidos">' not in contenido

def test_pagina_partidos_asistidos_sin_partidos_asistidos(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/asistidos", follow_redirects=True)
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " in contenido
		assert '<div class="tarjetas-partidos-asistidos">' not in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido-asistidos"' not in contenido
		assert '<div class="info-partido-asistidos">' not in contenido

def test_pagina_partidos_asistidos_con_partido_asistido(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos", follow_redirects=True)
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " not in contenido
		assert '<div class="tarjetas-partidos-asistidos">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos"' in contenido
		assert '<div class="info-partido-asistidos">' in contenido