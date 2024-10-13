import pytest

def test_pagina_anadir_partido_asistido_sin_login(cliente):

	respuesta=cliente.get("/anadir_partido_asistido", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_anadir_partido_asistido_partidos_no_existen(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno.c.execute("""DELETE FROM partidos""")

		conexion_entorno.confirmar()

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' not in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' not in contenido
		assert '<button type="button" class="boton-todos-partidos"' not in contenido
		assert 'recientes.png' not in contenido
		assert '?todos=True' not in contenido
		assert 'todos.png' not in contenido
		assert '<p class="etiqueta">' not in contenido
		assert "No hay partidos disponibles para añadir..." in contenido

def test_pagina_anadir_partido_asistido_partidos_no_existen_equipo_usuario(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno.c.execute("""DELETE FROM partidos""")

		conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival1'),('rival2')""")

		conexion_entorno.c.execute("""INSERT INTO partidos
										VALUES('20190622', 'rival1', 'rival2', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
												('20190623', 'rival2', 'rival2', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria'),
												('20190624', 'rival1', 'rival1', '2019-06-24', '22:00', 'Liga', '1-0', 'Victoria'),
												('20190625', 'rival2', 'rival1', '2019-06-25', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.confirmar()

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' not in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' not in contenido
		assert '<button type="button" class="boton-todos-partidos"' not in contenido
		assert 'recientes.png' not in contenido
		assert '?todos=True' not in contenido
		assert 'todos.png' not in contenido
		assert '<p class="etiqueta">' not in contenido
		assert "No hay partidos disponibles para añadir..." in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_existen_recientes(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' in contenido
		assert '<button type="button" class="boton-todos-partidos"' in contenido
		assert 'recientes.png' in contenido
		assert '?todos=True' in contenido
		assert 'todos.png' not in contenido
		assert '<p class="etiqueta">' in contenido
		assert "No hay partidos disponibles para añadir..." not in contenido

def test_pagina_anadir_partido_asistido_partido_no_asistidos_no_existen_recientes(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno.insertarPartidoAsistido("20190622", "nacho98", "comentario")

		conexion_entorno.confirmar()

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' not in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' not in contenido
		assert '<button type="button" class="boton-todos-partidos"' not in contenido
		assert 'recientes.png' not in contenido
		assert '?todos=True' not in contenido
		assert 'todos.png' not in contenido
		assert '<p class="etiqueta">' not in contenido
		assert "No hay partidos disponibles para añadir..." in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_existen_todos(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido?todos=True")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' in contenido
		assert '<button type="button" class="boton-todos-partidos"' in contenido
		assert 'recientes.png' not in contenido
		assert '?todos=True' not in contenido
		assert 'todos.png' in contenido
		assert '<p class="etiqueta">' in contenido
		assert "No hay partidos disponibles para añadir..." not in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_partido_no_defecto(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<option value="sin-seleccion" selected disabled hidden>' in contenido
		assert '<option value="sin-seleccion" disabled hidden>' not in contenido
		assert '<option value="20190622" selected>' not in contenido
		assert '<option value="20190622">' in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_partido_defecto(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido?partido_id=20190622&todos=True")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<option value="sin-seleccion" selected disabled hidden>' not in contenido
		assert '<option value="sin-seleccion" disabled hidden>' in contenido
		assert '<option value="20190622" selected>' in contenido
		assert '<option value="20190622">' not in contenido