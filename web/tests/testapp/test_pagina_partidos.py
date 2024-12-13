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
	assert '<div class="tarjeta-partido"' not in contenido
	assert '<div class="info-partido">' not in contenido
	assert '<div class="tarjeta-partidos-asistidos">' not in contenido
	assert '<div class="tarjeta-proximos-partidos">' not in contenido
	assert '<div class="tarjeta-no-proximo-partido">' not in contenido
	assert '<div id="ventana-emergente" class="ventana-emergente">' not in contenido

def test_pagina_partidos_con_partido(cliente, conexion_entorno):

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Partidos del " in contenido
	assert 'alt="Total Filtrado"' in contenido
	assert 'alt="Local Filtrado"' not in contenido
	assert 'alt="Visitante Filtrado"' not in contenido
	assert '<img class="navbar-escudo" src="/static/imagenes/favoritos/atletico-madrid.png'in contenido
	assert "No hay ningun partido disponible del " not in contenido
	assert '<div class="tarjetas-partidos">' in contenido
	assert '<div class="tarjetas-partidos-wrapper">' in contenido
	assert '<div class="tarjeta-partido"' in contenido
	assert '<div class="info-partido">' in contenido
	assert '<div class="tarjeta-partidos-asistidos">' not in contenido
	assert '<div class="tarjeta-proximos-partidos">' in contenido
	assert '<div class="tarjeta-no-proximo-partido">' not in contenido
	assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido

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
	assert 'alt="Total Filtrado"' in contenido
	assert 'alt="Local Filtrado"' not in contenido
	assert 'alt="Visitante Filtrado"' not in contenido

def test_pagina_partidos_partido_casa_no_hay(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id) VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'rival', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio_rival')""")

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
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_partido_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id) VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'metropolitano')""")

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
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="tarjetas-partidos">' in contenido
		assert '<div class="tarjetas-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido"' in contenido
		assert '<div class="info-partido">' in contenido
		assert '<h4>atleti ' in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' in contenido

def test_pagina_partidos_partido_casa_local_fuera_de_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id) VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio_rival')""")

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
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_partido_casa_visitante_en_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id) VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'rival', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'metropolitano')""")

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
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="tarjetas-partidos">' in contenido
		assert '<div class="tarjetas-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido"' in contenido
		assert '<div class="info-partido">' in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' in contenido
		assert ' atleti</h4>' in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_partido_fuera_no_hay(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id) VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'metropolitano')""")

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
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_partido_fuera(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id) VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'rival', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio_rival')""")

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
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert '<div class="tarjetas-partidos">' in contenido
		assert '<div class="tarjetas-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido"' in contenido
		assert '<div class="info-partido">' in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' in contenido
		assert ' atleti</h4>' in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_partido_fuera_local_fuera_de_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id) VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio_rival')""")

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
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert '<div class="tarjetas-partidos">' in contenido
		assert '<div class="tarjetas-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido"' in contenido
		assert '<div class="info-partido">' in contenido
		assert '<h4>atleti ' in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' in contenido

def test_pagina_partidos_partido_fuera_visitante_en_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id) VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'rival', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'metropolitano')""")

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
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
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
		assert "2019/2020" in contenido
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
		assert "2018/2019" in contenido
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
		assert f"{temporada-1}/{temporada}" in contenido
		assert f"Temporada {temporada-1} - {temporada}" in contenido
		assert f"22/06/{temporada}" in contenido

		for temporada_no in temporadas_no:

			assert f"Temporada {temporada_no-1} - {temporada_no}" not in contenido
			assert f"22/06/{temporada_no}" not in contenido

@pytest.mark.parametrize(["temporada"],
	[(2020,),(2015,),(1998,)]
)
def test_pagina_partidos_local_temporada_no_hay(cliente, conexion, temporada):

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
		assert "No hay ningun partido disponible del None..." in contenido
		assert f"{temporada-1}/{temporada}" in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert f"Temporada {temporada-1} - {temporada}" not in contenido
		assert f"22/06/{temporada}" not in contenido

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
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert f"{temporada-1}/{temporada}" in contenido
		assert '<h4>atleti ' in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' in contenido
		assert f"Temporada {temporada-1} - {temporada}" in contenido
		assert f"22/06/{temporada}" in contenido

		for temporada_no in temporadas_no:

			assert f"Temporada {temporada_no-1} - {temporada_no}" not in contenido
			assert f"22/06/{temporada_no}" not in contenido

@pytest.mark.parametrize(["temporada"],
	[(2019,),(2016,),(2024,)]
)
def test_pagina_partidos_visitante_temporada_no_hay(cliente, conexion, temporada):

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

		respuesta=cliente_abierto.get(f"/partidos?local=2&temporada={temporada}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert f"{temporada-1}/{temporada}" in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert f"Temporada {temporada-1} - {temporada}" not in contenido
		assert f"22/06/{temporada}" not in contenido

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

		respuesta=cliente_abierto.get(f"/partidos?local=2&temporada={temporada}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert f"{temporada-1}/{temporada}" in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' in contenido
		assert ' atleti</h4>' in contenido
		assert ' rival</h4>' not in contenido
		assert f"Temporada {temporada-1} - {temporada}" in contenido
		assert f"22/06/{temporada}" in contenido

		for temporada_no in temporadas_no:

			assert f"Temporada {temporada_no-1} - {temporada_no}" not in contenido
			assert f"22/06/{temporada_no}" not in contenido

@pytest.mark.parametrize(["cantidad_partidos"],
	[(1,),(2,),(10,),(7,),(22,)]
)
def test_pagina_partidos_partidos_totales(cliente, conexion, cantidad_partidos):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	for numero in range(cantidad_partidos):

		conexion.c.execute("""INSERT INTO partidos
							VALUES (%s, 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""",
							(f"2019{numero+1}",))

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<p class="titulo-circulo-partidos-totales">' in contenido
		assert "Partidos Jugados" in contenido
		assert f'<p class="valor-circulo-partidos-totales"><strong>{cantidad_partidos}</strong></p>' in contenido

def test_pagina_partidos_partidos_estadisticas(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20191', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria Local')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="circulo-estadisticas-partidos-disputados">' in contenido
		assert '<canvas id="grafico_tarta">' in contenido
		assert "var datos_grafica_tarta=" in contenido

def test_pagina_partidos_sin_partido_asistido(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-partidos-asistidos">' not in contenido
		assert '<p class="titulo-partidos-asistidos">' not in contenido
		assert '<div class="tarjeta-partido-asistido"' not in contenido
		assert '<div class="info-partido-asistido">' not in contenido

def test_pagina_partidos_con_partido_asistido(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":"comentario"})

		respuesta=cliente_abierto.get("/partidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-partidos-asistidos">' in contenido
		assert '<p class="titulo-partidos-asistidos">' in contenido
		assert '<div class="tarjeta-partido-asistido"' in contenido
		assert '<div class="info-partido-asistido">' in contenido

def test_pagina_partidos_con_partido_asistido_temporada_no_hay(cliente, conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
						VALUES ('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":"comentario"})

		respuesta=cliente_abierto.get("/partidos?temporada=2020")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-partidos-asistidos">' not in contenido
		assert '<p class="titulo-partidos-asistidos">' not in contenido
		assert '<div class="tarjeta-partido-asistido"' not in contenido
		assert '<div class="info-partido-asistido">' not in contenido

def test_pagina_partidos_con_partido_asistido_temporada(cliente, conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
						VALUES ('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20200622", "comentario":"comentario"})

		respuesta=cliente_abierto.get("/partidos?temporada=2020")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-partidos-asistidos">' in contenido
		assert '<p class="titulo-partidos-asistidos">' in contenido
		assert '<div class="tarjeta-partido-asistido"' in contenido
		assert '<div class="info-partido-asistido">' in contenido

@pytest.mark.parametrize(["cantidad_partidos", "cantidad_partidos_asistidos"],
	[(1,1),(2,1),(10,6),(7,3),(22,15)]
)
def test_pagina_partidos_partidos_asistidos(cliente, conexion, cantidad_partidos, cantidad_partidos_asistidos):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	for numero in range(cantidad_partidos):

		conexion.c.execute("""INSERT INTO partidos
							VALUES (%s, 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""",
							(f"2019{numero+1}",))

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero_asistidos in range(cantidad_partidos_asistidos):

			data={"partido_anadir":f"2019{numero_asistidos+1}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<p class="titulo-circulo-partidos-asistidos">' in contenido
		assert "Partidos Asistidos" in contenido
		assert f'<p class="valor-circulo-partidos-asistidos"><strong>{cantidad_partidos_asistidos}</strong></p>' in contenido

def test_pagina_partidos_sin_proximos_partidos(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM proximos_partidos")

	conexion_entorno.confirmar()

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<div class="tarjetas-proximos-partidos">' not in contenido
	assert '<div class="tarjetas-proximos-partidos-wrapper">' not in contenido
	assert '<div class="tarjeta-proximo-partido">' not in contenido
	assert '<div class="info-proximo-partido">' not in contenido
	assert '<div class="tarjeta-no-proximo-partido">' in contenido

def test_pagina_partidos_con_proximo_partido(cliente, conexion_entorno):

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<div class="tarjetas-proximos-partidos">' in contenido
	assert '<div class="tarjetas-proximos-partidos-wrapper">' in contenido
	assert '<div class="tarjeta-proximo-partido">' in contenido
	assert '<div class="info-proximo-partido">' in contenido
	assert '<div class="tarjeta-no-proximo-partido">' not in contenido

def test_pagina_partidos_competicion_no_hay(cliente, conexion):

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

		respuesta=cliente_abierto.get("/partidos?competicion=Primera")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert "- Primera" not in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' not in contenido
		assert '<option value="Primera">Primera</option>' not in contenido
		assert '<option value="Todo">Todo</option>' not in contenido

def test_pagina_partidos_competicion(cliente, conexion):

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

		respuesta=cliente_abierto.get("/partidos?competicion=Liga")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." not in contenido
		assert "- Liga" in contenido
		assert '<div class="tarjetas-partidos">' in contenido
		assert '<div class="tarjetas-partidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido"' in contenido
		assert '<div class="info-partido">' in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert '<option value="Liga">Liga</option>' in contenido
		assert '<option value="Todo">Todo</option>' in contenido

@pytest.mark.parametrize(["competicion", "competiciones_no"],
	[
		("Liga", ["Primera", "Copa", "Champions", "Mundial", "Supercopa"]),
		("Primera", ["Liga", "Copa", "Champions", "Mundial", "Supercopa"]),
		("Copa", ["Primera", "Liga", "Champions", "Mundial", "Supercopa"]),
		("Champions", ["Primera", "Copa", "Liga", "Mundial", "Supercopa"]),
		("Supercopa", ["Primera", "Copa", "Champions", "Mundial", "Liga"])
	]
)
def test_pagina_partidos_competicion_varios(cliente, conexion, competicion, competiciones_no):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20240622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20240623', 'rival', 'atletico-madrid', '2020-06-23', '22:00', 'Primera', '1-0', 'Victoria'),
								('20240624', 'atletico-madrid', 'rival', '2016-06-24', '22:00', 'Copa', '1-0', 'Victoria'),
								('20240625', 'rival', 'atletico-madrid', '2015-06-25', '22:00', 'Champions', '1-0', 'Victoria'),
								('20240626', 'atletico-madrid', 'rival', '2024-06-26', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240627', 'rival', 'atletico-madrid', '1998-06-27', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert f"- {competicion}" in contenido
		assert f'<option value="{competicion}">{competicion}</option>' in contenido
		assert '<option value="Todo">Todo</option>' in contenido

		for competicion_no in competiciones_no:

			assert f"- {competicion_no}" not in contenido
			assert f'<option value="{competicion_no}">{competicion_no}</option>' in contenido

@pytest.mark.parametrize(["competicion"],
	[("Liga",),("Mundial",),("Supercopa",)]
)
def test_pagina_partidos_local_competicion_no_hay(cliente, conexion, competicion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20240622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Primera', '1-0', 'Victoria'),
								('20240623', 'rival', 'atletico-madrid', '2020-06-23', '22:00', 'Liga', '1-0', 'Victoria'),
								('20240624', 'atletico-madrid', 'rival', '2016-06-24', '22:00', 'Copa', '1-0', 'Victoria'),
								('20240625', 'rival', 'atletico-madrid', '2015-06-25', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240626', 'atletico-madrid', 'rival', '2024-06-26', '22:00', 'Champions', '1-0', 'Victoria'),
								('20240627', 'rival', 'atletico-madrid', '1998-06-27', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?local=1&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert f"- {competicion}" not in contenido
		assert f'<option value="{competicion}">{competicion}</option>' not in contenido
		assert '<option value="Todo">Todo</option>' not in contenido

@pytest.mark.parametrize(["competicion", "competiciones_no"],
	[
		("Primera", ["Copa", "Champions"]),
		("Copa", ["Primera", "Champions"]),
		("Champions", ["Primera", "Copa"])
	]
)
def test_pagina_partidos_local_competicion(cliente, conexion, competicion, competiciones_no):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20240622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Primera', '1-0', 'Victoria'),
								('20240623', 'rival', 'atletico-madrid', '2020-06-23', '22:00', 'Liga', '1-0', 'Victoria'),
								('20240624', 'atletico-madrid', 'rival', '2016-06-24', '22:00', 'Copa', '1-0', 'Victoria'),
								('20240625', 'rival', 'atletico-madrid', '2015-06-25', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240626', 'atletico-madrid', 'rival', '2024-06-26', '22:00', 'Champions', '1-0', 'Victoria'),
								('20240627', 'rival', 'atletico-madrid', '1998-06-27', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?local=1&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert f"- {competicion}" in contenido
		assert '<h4>atleti ' in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' in contenido
		assert f'<option value="{competicion}">{competicion}</option>' in contenido
		assert '<option value="Todo">Todo</option>' in contenido

		for competicion_no in competiciones_no:

			assert f"- {competicion_no}" not in contenido
			assert f'<option value="{competicion_no}">{competicion_no}</option>' in contenido

@pytest.mark.parametrize(["competicion"],
	[("Primera",),("Copa",),("Champions",)]
)
def test_pagina_partidos_visitante_competicion_no_hay(cliente, conexion, competicion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20240622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Primera', '1-0', 'Victoria'),
								('20240623', 'rival', 'atletico-madrid', '2020-06-23', '22:00', 'Liga', '1-0', 'Victoria'),
								('20240624', 'atletico-madrid', 'rival', '2016-06-24', '22:00', 'Copa', '1-0', 'Victoria'),
								('20240625', 'rival', 'atletico-madrid', '2015-06-25', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240626', 'atletico-madrid', 'rival', '2024-06-26', '22:00', 'Champions', '1-0', 'Victoria'),
								('20240627', 'rival', 'atletico-madrid', '1998-06-27', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?local=2&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert f"- {competicion}" not in contenido
		assert f'<option value="{competicion}">{competicion}</option>' not in contenido
		assert '<option value="Todo">Todo</option>' not in contenido

@pytest.mark.parametrize(["competicion", "competiciones_no"],
	[
		("Primera", ["Copa", "Champions"]),
		("Copa", ["Primera", "Champions"]),
		("Champions", ["Primera", "Copa"])
	]
)
def test_pagina_partidos_visitante_competicion(cliente, conexion, competicion, competiciones_no):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20240622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20240623', 'rival', 'atletico-madrid', '2020-06-23', '22:00', 'Primera', '1-0', 'Victoria'),
								('20240624', 'atletico-madrid', 'rival', '2016-06-24', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240625', 'rival', 'atletico-madrid', '2015-06-25', '22:00', 'Copa', '1-0', 'Victoria'),
								('20240626', 'atletico-madrid', 'rival', '2024-06-26', '22:00', 'Supercopa', '1-0', 'Victoria'),
								('20240627', 'rival', 'atletico-madrid', '1998-06-27', '22:00', 'Champions', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?local=2&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert f"- {competicion}" in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' in contenido
		assert ' atleti</h4>' in contenido
		assert ' rival</h4>' not in contenido
		assert f'<option value="{competicion}">{competicion}</option>' in contenido
		assert '<option value="Todo">Todo</option>' in contenido

		for competicion_no in competiciones_no:

			assert f"- {competicion_no}" not in contenido
			assert f'<option value="{competicion_no}">{competicion_no}</option>' in contenido

@pytest.mark.parametrize(["temporada", "competicion"],
	[(2024, "Primera"),(2019, "Copa"),(2016, "Champions")]
)
def test_pagina_partidos_temporada_competicion_no_hay(cliente, conexion, temporada, competicion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Primera', '1-0', 'Victoria'),
								('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20160622', 'atletico-madrid', 'rival', '2016-06-22', '22:00', 'Copa', '1-0', 'Victoria'),
								('20150622', 'rival', 'atletico-madrid', '2015-06-22', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240622', 'atletico-madrid', 'rival', '2024-06-22', '22:00', 'Champions', '1-0', 'Victoria'),
								('19980622', 'rival', 'atletico-madrid', '1998-06-22', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?temporada={temporada}&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert f"{temporada-1}/{temporada}" in contenido
		assert f"- {competicion}" not in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert f"Temporada {temporada-1} - {temporada}" not in contenido
		assert f"22/06/{temporada}" not in contenido
		assert f'<option value="{competicion}">{competicion}</option>' not in contenido
		assert '<option value="Todo">Todo</option>' not in contenido

@pytest.mark.parametrize(["temporada", "temporadas_no", "competicion", "competiciones_no"],
	[
		(2024, [2016, 2019], "Champions", ["Primera", "Copa"]),
		(2019, [2016, 2024], "Primera", ["Copa", "Champions"]),
		(2016, [2019, 2024], "Copa", ["Primera", "Champions"])
	]
)
def test_pagina_partidos_temporada_competicion(cliente, conexion, temporada, temporadas_no, competicion, competiciones_no):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Primera', '1-0', 'Victoria'),
								('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20160622', 'atletico-madrid', 'rival', '2016-06-22', '22:00', 'Copa', '1-0', 'Victoria'),
								('20150622', 'rival', 'atletico-madrid', '2015-06-22', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240622', 'atletico-madrid', 'rival', '2024-06-22', '22:00', 'Champions', '1-0', 'Victoria'),
								('19980622', 'rival', 'atletico-madrid', '1998-06-22', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?temporada={temporada}&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert f"{temporada-1}/{temporada}" in contenido
		assert f"- {competicion}" in contenido
		assert f"Temporada {temporada-1} - {temporada}" in contenido
		assert f"22/06/{temporada}" in contenido
		assert f'<option value="{competicion}">{competicion}</option>' in contenido
		assert '<option value="Todo">Todo</option>' in contenido

		for temporada_no in temporadas_no:

			assert f"Temporada {temporada_no-1} - {temporada_no}" not in contenido
			assert f"22/06/{temporada_no}" not in contenido

		for competicion_no in competiciones_no:

			assert f"- {competicion_no}" not in contenido
			assert f'<option value="{competicion_no}">{competicion_no}</option>' not in contenido

@pytest.mark.parametrize(["temporada", "competicion"],
	[(2024, "Primera"),(2019, "Copa"),(2016, "Champions")]
)
def test_pagina_partidos_local_temporada_competicion_no_hay(cliente, conexion, temporada, competicion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Primera', '1-0', 'Victoria'),
								('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20160622', 'atletico-madrid', 'rival', '2016-06-22', '22:00', 'Copa', '1-0', 'Victoria'),
								('20150622', 'rival', 'atletico-madrid', '2015-06-22', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240622', 'atletico-madrid', 'rival', '2024-06-22', '22:00', 'Champions', '1-0', 'Victoria'),
								('19980622', 'rival', 'atletico-madrid', '1998-06-22', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?local=1&temporada={temporada}&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert f"{temporada-1}/{temporada}" in contenido
		assert f"- {competicion}" not in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert f"Temporada {temporada-1} - {temporada}" not in contenido
		assert f"22/06/{temporada}" not in contenido
		assert f'<option value="{competicion}">{competicion}</option>' not in contenido
		assert '<option value="Todo">Todo</option>' not in contenido

@pytest.mark.parametrize(["temporada", "temporadas_no", "competicion", "competiciones_no"],
	[
		(2024, [2016, 2019], "Champions", ["Primera", "Copa"]),
		(2019, [2016, 2024], "Primera", ["Copa", "Champions"]),
		(2016, [2019, 2024], "Copa", ["Primera", "Champions"])
	]
)
def test_pagina_partidos_local_temporada_competicion(cliente, conexion, temporada, temporadas_no, competicion, competiciones_no):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Primera', '1-0', 'Victoria'),
								('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20160622', 'atletico-madrid', 'rival', '2016-06-22', '22:00', 'Copa', '1-0', 'Victoria'),
								('20150622', 'rival', 'atletico-madrid', '2015-06-22', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240622', 'atletico-madrid', 'rival', '2024-06-22', '22:00', 'Champions', '1-0', 'Victoria'),
								('19980622', 'rival', 'atletico-madrid', '1998-06-22', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?local=1&temporada={temporada}&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert f"{temporada-1}/{temporada}" in contenido
		assert f"- {competicion}" in contenido
		assert '<h4>atleti ' in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' in contenido
		assert f"Temporada {temporada-1} - {temporada}" in contenido
		assert f"22/06/{temporada}" in contenido
		assert f'<option value="{competicion}">{competicion}</option>' in contenido
		assert '<option value="Todo">Todo</option>' in contenido

		for temporada_no in temporadas_no:

			assert f"Temporada {temporada_no-1} - {temporada_no}" not in contenido
			assert f"22/06/{temporada_no}" not in contenido

		for competicion_no in competiciones_no:

			assert f"- {competicion_no}" not in contenido
			assert f'<option value="{competicion_no}">{competicion_no}</option>' not in contenido

@pytest.mark.parametrize(["temporada", "competicion"],
	[(2020, "Primera"),(2015, "Copa"),(1998, "Champions")]
)
def test_pagina_partidos_visitante_temporada_competicion_no_hay(cliente, conexion, temporada, competicion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Primera', '1-0', 'Victoria'),
								('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20160622', 'atletico-madrid', 'rival', '2016-06-22', '22:00', 'Copa', '1-0', 'Victoria'),
								('20150622', 'rival', 'atletico-madrid', '2015-06-22', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240622', 'atletico-madrid', 'rival', '2024-06-22', '22:00', 'Champions', '1-0', 'Victoria'),
								('19980622', 'rival', 'atletico-madrid', '1998-06-22', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?local=2&temporada={temporada}&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "No hay ningun partido disponible del None..." in contenido
		assert f"{temporada-1}/{temporada}" in contenido
		assert f"- {competicion}" not in contenido
		assert '<div class="tarjetas-partidos">' not in contenido
		assert '<div class="tarjetas-partidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido"' not in contenido
		assert '<div class="info-partido">' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert f"Temporada {temporada-1} - {temporada}" not in contenido
		assert f"22/06/{temporada}" not in contenido
		assert f'<option value="{competicion}">{competicion}</option>' not in contenido
		assert '<option value="Todo">Todo</option>' not in contenido

@pytest.mark.parametrize(["temporada", "temporadas_no", "competicion", "competiciones_no"],
	[
		(2020, [1998, 2015], "Liga", ["Mundial", "Supercopa"]),
		(2015, [1998, 2020], "Mundial", ["Liga", "Supercopa"]),
		(1998, [2015, 2020], "Supercopa", ["Liga", "Mundial"])
	]
)
def test_pagina_partidos_visitante_temporada_competicion(cliente, conexion, temporada, temporadas_no, competicion, competiciones_no):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Primera', '1-0', 'Victoria'),
								('20200622', 'rival', 'atletico-madrid', '2020-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
								('20160622', 'atletico-madrid', 'rival', '2016-06-22', '22:00', 'Copa', '1-0', 'Victoria'),
								('20150622', 'rival', 'atletico-madrid', '2015-06-22', '22:00', 'Mundial', '1-0', 'Victoria'),
								('20240622', 'atletico-madrid', 'rival', '2024-06-22', '22:00', 'Champions', '1-0', 'Victoria'),
								('19980622', 'rival', 'atletico-madrid', '1998-06-22', '22:00', 'Supercopa', '1-0', 'Victoria')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos?local=2&temporada={temporada}&competicion={competicion}")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert f"{temporada-1}/{temporada}" in contenido
		assert f"- {competicion}" in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' in contenido
		assert ' atleti</h4>' in contenido
		assert ' rival</h4>' not in contenido
		assert f"Temporada {temporada-1} - {temporada}" in contenido
		assert f"22/06/{temporada}" in contenido
		assert f'<option value="{competicion}">{competicion}</option>' in contenido
		assert '<option value="Todo">Todo</option>' in contenido

		for temporada_no in temporadas_no:

			assert f"Temporada {temporada_no-1} - {temporada_no}" not in contenido
			assert f"22/06/{temporada_no}" not in contenido

		for competicion_no in competiciones_no:

			assert f"- {competicion_no}" not in contenido
			assert f'<option value="{competicion_no}">{competicion_no}</option>' not in contenido