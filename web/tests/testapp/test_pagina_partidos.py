import pytest

def test_pagina_partidos_sin_partidos(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.confirmar()

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Partidos del " in contenido
	assert f'<img class="navbar-escudo" src="/static/imagenes/favoritos/atletico-madrid.png'in contenido
	assert "No hay ningun partido disponible del " in contenido
	assert '<div class="tarjetas-partidos">' not in contenido
	assert '<div class="tarjetas-partidos-wrapper">' not in contenido
	assert '<div class="tarjeta-partido">' not in contenido
	assert '<div class="info-partido">' not in contenido

def test_pagina_partidos_con_partido(cliente, conexion_entorno):

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Partidos del " in contenido
	assert f'<img class="navbar-escudo" src="/static/imagenes/favoritos/atletico-madrid.png'in contenido
	assert "No hay ningun partido disponible del " not in contenido
	assert '<div class="tarjetas-partidos">' in contenido
	assert '<div class="tarjetas-partidos-wrapper">' in contenido
	assert '<div class="tarjeta-partido"' in contenido
	assert '<div class="info-partido">' in contenido

@pytest.mark.parametrize(["nombre_completo"],
	[("atleti",),("atm",),("Club Atletico de Madrid",)]
)
def test_pagina_partidos_con_nombre_equipo(cliente, conexion, nombre_completo):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre_Completo)
						VALUES('atletico-madrid', %s)""", (nombre_completo,))

	conexion.confirmar()

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f"Partidos del {nombre_completo}" in contenido

def test_pagina_partidos_partido_local_no_hay(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'rival', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos?local=1")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_partido_local(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos?local=1")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." not in contenido
		assert '<div class="tarjetas-partidos">' in contenido
		assert '<div class="tarjetas-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido"' in contenido
		assert '<div class="info-partido">' in contenido
		assert '<h4>atleti ' in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' in contenido

def test_pagina_partidos_partido_visitante_no_hay(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos?local=2")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_partido_visitante(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'rival', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos?local=2")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." not in contenido
		assert '<div class="tarjetas-partidos">' in contenido
		assert '<div class="tarjetas-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido"' in contenido
		assert '<div class="info-partido">' in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' in contenido
		assert ' atleti</h4>' in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_temporada_no_hay(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'rival', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos?temporada=2020")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert "Temporada 2018 - 2019" not in contenido
		assert "22/06/2019" not in contenido

def test_pagina_partidos_temporada(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'rival', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos?temporada=2019")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." not in contenido
		assert '<div class="tarjetas-partidos">' in contenido
		assert '<div class="tarjetas-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido"' in contenido
		assert '<div class="info-partido">' in contenido
		assert "Temporada 2018 - 2019" in contenido
		assert "22/06/2019" in contenido

@pytest.mark.parametrize(["temporada", "temporadas_no"],
	[
		(2020, [2015, 2016, 2019, 2024]),
		(2019, [2015, 2016, 2020, 2024]),
		(2016, [2015, 2019, 2020, 2024]),
		(2015, [2016, 2019, 2020, 2024]),
		(2024, [2015, 2016, 2019, 2020])
	]
)
def test_pagina_partidos_temporada_varios(cliente, conexion, temporada, temporadas_no):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20160622', 'atletico-madrid', 'rival', '2016-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20150622', 'rival', 'atletico-madrid', '2015-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20240622', 'atletico-madrid', 'rival', '2024-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('19980622', 'rival', 'atletico-madrid', '1998-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?temporada={temporada}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert f"Temporada {temporada-1} - {temporada}" in contenido
		assert f"22/06/{temporada}" in contenido

		for temporada_no in temporadas_no:

			assert f"Temporada {temporada_no-1} - {temporada_no}" not in contenido
			assert f"22/06/{temporada_no}" not in contenido

@pytest.mark.parametrize(["temporada", "temporadas_no"],
	[
		(2024, [2016, 2019]),
		(2019, [2016, 2024]),
		(2016, [2019, 2024])
	]
)
def test_pagina_partidos_local_temporada(cliente, conexion, temporada, temporadas_no):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20160622', 'atletico-madrid', 'rival', '2016-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20150622', 'rival', 'atletico-madrid', '2015-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20240622', 'atletico-madrid', 'rival', '2024-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('19980622', 'rival', 'atletico-madrid', '1998-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?local=1&temporada={temporada}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h4>atleti ' in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' in contenido
		assert f"Temporada {temporada-1} - {temporada}" in contenido
		assert f"22/06/{temporada}" in contenido

		for temporada_no in temporadas_no:

			assert f"Temporada {temporada_no-1} - {temporada_no}" not in contenido
			assert f"22/06/{temporada_no}" not in contenido

@pytest.mark.parametrize(["temporada", "temporadas_no"],
	[
		(2020, [1998, 2015]),
		(2015, [1998, 2020]),
		(1998, [2015, 2020])
	]
)
def test_pagina_partidos_visitante_temporada(cliente, conexion, temporada, temporadas_no):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20160622', 'atletico-madrid', 'rival', '2016-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20150622', 'rival', 'atletico-madrid', '2015-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20240622', 'atletico-madrid', 'rival', '2024-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('19980622', 'rival', 'atletico-madrid', '1998-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?loca2=1&temporada={temporada}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' in contenido
		assert ' atleti</h4>' in contenido
		assert ' rival</h4>' not in contenido
		assert f"Temporada {temporada-1} - {temporada}" in contenido
		assert f"22/06/{temporada}" in contenido

		for temporada_no in temporadas_no:

			assert f"Temporada {temporada_no-1} - {temporada_no}" not in contenido
			assert f"22/06/{temporada_no}" not in contenido