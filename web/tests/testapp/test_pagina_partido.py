import pytest

def test_pagina_partido_sin_login(cliente):

	respuesta=cliente.get("/partido/1", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_partido_partido_no_existe(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/1")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_equipo_no_pertenece(cliente, conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('equipo-no-partido')""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"equipo-no-partido"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_con_estadio(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-detalle"' in contenido
		assert '<p class="competicion">' in contenido
		assert '<div class="info-partido-detalle">' in contenido
		assert '<div class="info-partido-estadio"' in contenido

def test_pagina_partido_sin_estadio(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM estadios")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-detalle"' in contenido
		assert '<p class="competicion">' in contenido
		assert '<div class="info-partido-detalle">' in contenido
		assert '<div class="info-partido-estadio">' not in contenido

@pytest.mark.parametrize(["partido_id", "temporada"],
	[
		("20190622", 2019),
		("20150622", 2015),
		("20210738622", 2021),
		("2022", 2022),
		("2024fju0622", 2024),
		("201958458485496570622", 2019)
	]
)
def test_pagina_partido_temporada(cliente, conexion, partido_id, temporada):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES(%s, 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""",
						(partido_id,))

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/{partido_id}")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert f'/partidos?temporada={temporada}' in contenido

def test_pagina_partido_no_partido_anterior_no_partido_siguiente(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior"' not in contenido
		assert '<button class="button-partido-siguiente"' not in contenido

def test_pagina_partido_no_partido_anterior_si_partido_siguiente(cliente, conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior"' not in contenido
		assert '<button class="button-partido-siguiente"' in contenido

def test_pagina_partido_si_partido_anterior_no_partido_siguiente(cliente, conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior"' in contenido
		assert '<button class="button-partido-siguiente"' not in contenido

def test_pagina_partido_si_partido_anterior_si_partido_siguiente(cliente, conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('202454564', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior"' in contenido
		assert '<button class="button-partido-siguiente"' in contenido