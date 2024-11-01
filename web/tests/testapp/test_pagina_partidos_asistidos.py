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

		respuesta=cliente_abierto.get("/partidos/asistidos")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' in contenido
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

		respuesta=cliente_abierto.get("/partidos/asistidos")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' in contenido
		assert '<div class="tarjetas-partidos-asistidos">' not in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido-asistidos"' not in contenido
		assert '<div class="info-partido-asistidos">' not in contenido

def test_pagina_partidos_asistidos_con_partido_asistido(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio', 10000)""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'estadio')""")

	conexion.c.execute("""INSERT INTO partidos VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " not in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' not in contenido
		assert 'alt="Total Filtrado"' in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="tarjetas-partidos-asistidos">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos"' in contenido
		assert '<div class="info-partido-asistidos">' in contenido

@pytest.mark.parametrize(["cantidad_partidos", "cantidad_partidos_asistidos"],
	[(1,1),(2,1),(10,6),(7,3),(22,15)]
)
def test_pagina_partidos_asistidos_partidos_asistidos(cliente, conexion, cantidad_partidos, cantidad_partidos_asistidos):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio', 10000)""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'estadio')""")

	for numero in range(cantidad_partidos):

		conexion.c.execute("""INSERT INTO partidos
							VALUES (%s, 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""",
							(f"2019{numero+1}",))

		conexion.c.execute("""INSERT INTO partido_estadio VALUES(%s, 'estadio')""", (f"2019{numero+1}",))

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

		respuesta=cliente_abierto.get("/partidos/asistidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<p class="titulo-circulo-partidos-asistidos-totales">' in contenido
		assert "Partidos Asistidos" in contenido
		assert f'<p class="valor-circulo-partidos-asistidos-totales"><strong>{cantidad_partidos_asistidos}</strong></p>' in contenido

def test_pagina_partidos_asistidos_partido_casa_no_hay(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('metropolitano', 100000),('estadio_rival', 100000)""")

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

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos?local=1")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="tarjetas-partidos-asistidos">' not in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido-asistidos"' not in contenido
		assert '<div class="info-partido-asistidos">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_asistidos_partido_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('metropolitano', 100000),('estadio_rival', 100000)""")

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

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos?local=1")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " not in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="tarjetas-partidos-asistidos">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos"' in contenido
		assert '<div class="info-partido-asistidos">' in contenido
		assert '<h4>atleti ' in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' in contenido

def test_pagina_partidos_asistidos_partido_casa_local_fuera_de_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('metropolitano', 100000),('estadio_rival', 100000)""")

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

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos?local=1")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="tarjetas-partidos-asistidos">' not in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido-asistidos"' not in contenido
		assert '<div class="info-partido-asistidos">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_asistidos_partido_casa_visitante_en_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('metropolitano', 100000),('estadio_rival', 100000)""")

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

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos?local=1")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " not in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="tarjetas-partidos-asistidos">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos"' in contenido
		assert '<div class="info-partido-asistidos">' in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' in contenido
		assert ' atleti</h4>' in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_asistidos_partido_fuera_no_hay(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('metropolitano', 100000),('estadio_rival', 100000)""")

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

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos?local=2")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert '<div class="tarjetas-partidos-asistidos">' not in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido-asistidos"' not in contenido
		assert '<div class="info-partido-asistidos">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_asistidos_partido_fuera(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('metropolitano', 100000),('estadio_rival', 100000)""")

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

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos?local=2")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " not in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert '<div class="tarjetas-partidos-asistidos">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos"' in contenido
		assert '<div class="info-partido-asistidos">' in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' in contenido
		assert ' atleti</h4>' in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_asistidos_partido_fuera_local_fuera_de_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('metropolitano', 100000),('estadio_rival', 100000)""")

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

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos?local=2")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " not in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' not in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert '<div class="tarjetas-partidos-asistidos">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos"' in contenido
		assert '<div class="info-partido-asistidos">' in contenido
		assert '<h4>atleti ' in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' in contenido

def test_pagina_partidos_asistidos_partido_fuera_visitante_en_casa(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'atleti'),('rival', 'rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('metropolitano', 100000),('estadio_rival', 100000)""")

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

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos?local=2")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos del " in contenido
		assert "No hay ningun partido asistido del " in contenido
		assert '<button class="boton-no-partidos-asistidos-anadir"' in contenido
		assert 'alt="Total Filtrado"' not in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' in contenido
		assert '<div class="tarjetas-partidos-asistidos">' not in contenido
		assert '<div class="tarjetas-partidos-asistidos-wrapper">' not in contenido
		assert '<div class="tarjeta-partido-asistidos"' not in contenido
		assert '<div class="info-partido-asistidos">' not in contenido
		assert '<h4>atleti ' not in contenido
		assert '<h4>rival ' not in contenido
		assert ' atleti</h4>' not in contenido
		assert ' rival</h4>' not in contenido

def test_pagina_partidos_asistidos_partidos_asistidos_estadisticas(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio', 10000)""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'estadio')""")

	conexion.c.execute("""INSERT INTO partidos VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<div class="circulo-estadisticas-partidos-asistidos">' in contenido
		assert '<canvas id="grafico_tarta">' in contenido
		assert "var datos_grafica_tarta=" in contenido

def test_pagina_partidos_asistidos_equipo_mas_enfrentado(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'ATM'),('rival', 'Rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio', 10000)""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'estadio')""")

	conexion.c.execute("""INSERT INTO partidos VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<p class="titulo-circulo-equipo-mas-enfrentado">' in contenido
		assert "Rival" in contenido
		assert '<p class="valor-circulo-equipo-mas-enfrentado"><strong>1 veces</strong></p>' in contenido

@pytest.mark.parametrize(["partidos_equipos", "equipo_mas_enfrentado", "veces"],
	[
		([2, 4, 6, 5], 3, 6),
		([2, 4, 6, 5, 7, 11], 6, 11),
		([10, 2, 4, 6, 5], 1, 10),
		([2, 4, 6, 5, 5, 4, 5, 5], 3, 6),
		([2, 4, 2, 13, 6, 5], 4, 13)
	]
)
def test_pagina_partidos_asistidos_equipo_mas_enfrentado_varios(cliente, conexion, partidos_equipos, equipo_mas_enfrentado, veces):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'ATM')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio', 10000)""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'estadio')""")

	for numero, cantidad_partidos in enumerate(partidos_equipos):

		conexion.c.execute(f"""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('rival{numero+1}', 'Rival{numero+1}')""")

		conexion.confirmar()

		for cantidad in range(cantidad_partidos):

			conexion.c.execute(f"""INSERT INTO partidos
								VALUES ('20190622{numero+1}{cantidad}', 'atletico-madrid', 'rival{numero+1}', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

			conexion.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero+1}{cantidad}', 'estadio')""")

			conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero, cantidad_partidos in enumerate(partidos_equipos):

			for cantidad in range(cantidad_partidos):

				data={"partido_anadir":f"20190622{numero+1}{cantidad}", "comentario":"comentario"}

				cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<p class="titulo-circulo-equipo-mas-enfrentado">' in contenido
		assert f"Rival{equipo_mas_enfrentado}" in contenido
		assert f'<p class="valor-circulo-equipo-mas-enfrentado"><strong>{veces} veces</strong></p>' in contenido

def test_pagina_partidos_asistidos_equipo_mas_enfrentado_contra_tu_equipo(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<p class="titulo-circulo-equipo-mas-enfrentado">' not in contenido
		assert '<h2 class="mensaje-error">Error en la peticion. Not found</h2>' in contenido

def test_pagina_partidos_asistidos_estadio_mas_visitado(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'ATM'),('rival', 'Rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Nombre, Capacidad) VALUES('estadio', 'Estadio', 10000)""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'estadio')""")

	conexion.c.execute("""INSERT INTO partidos VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<p class="titulo-circulo-estadio-mas-visitado">' in contenido
		assert "Estadio" in contenido
		assert '<p class="valor-circulo-estadio-mas-visitado"><strong>1 veces</strong></p>' in contenido

@pytest.mark.parametrize(["partidos_equipos", "estadio_mas_visitado", "veces"],
	[
		([2, 4, 6, 5], 3, 6),
		([2, 4, 6, 5, 7, 11], 6, 11),
		([10, 2, 4, 6, 5], 1, 10),
		([2, 4, 6, 5, 5, 4, 5, 5], 3, 6),
		([2, 4, 2, 13, 6, 5], 4, 13)
	]
)
def test_pagina_partidos_asistidos_estadio_mas_visitado_varios(cliente, conexion, partidos_equipos, estadio_mas_visitado, veces):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'ATM')""")

	for numero, cantidad_partidos in enumerate(partidos_equipos):

		conexion.c.execute(f"""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('rival{numero+1}', 'Rival')""")

		conexion.c.execute(f"""INSERT INTO estadios (Estadio_Id, Nombre, Capacidad) VALUES('estadio{numero+1}', 'Estadio{numero+1}', 10000)""")

		conexion.c.execute(f"""INSERT INTO equipo_estadio VALUES('rival{numero+1}', 'estadio{numero+1}')""")

		conexion.confirmar()

		for cantidad in range(cantidad_partidos):

			conexion.c.execute(f"""INSERT INTO partidos
								VALUES ('20190622{numero+1}{cantidad}', 'atletico-madrid', 'rival{numero+1}', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

			conexion.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero+1}{cantidad}', 'estadio{numero+1}')""")

			conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero, cantidad_partidos in enumerate(partidos_equipos):

			for cantidad in range(cantidad_partidos):

				data={"partido_anadir":f"20190622{numero+1}{cantidad}", "comentario":"comentario"}

				cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'alt="Total Filtrado"' in contenido
		assert 'alt="Local Filtrado"' not in contenido
		assert 'alt="Visitante Filtrado"' not in contenido
		assert '<p class="titulo-circulo-estadio-mas-visitado">' in contenido
		assert f"Estadio{estadio_mas_visitado}" in contenido
		assert f'<p class="valor-circulo-estadio-mas-visitado"><strong>{veces} veces</strong></p>' in contenido

def test_pagina_partidos_asistidos_sin_partido_asistido_favorito(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'ATM'),('rival', 'Rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio', 10000)""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'estadio')""")

	conexion.c.execute("""INSERT INTO partidos VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partidos/asistidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="circulo-partido-asistido-favorito">' not in contenido
		assert '<div class="tarjeta-partido-asistido-favorito"' not in contenido
		assert '<p class="titulo-circulo-partido-asistido-favorito"><strong>Partido Favorito</strong></p>' not in contenido
		assert '<div class="info-partido-asistido-favorito">' not in contenido

def test_pagina_partidos_asistidos_partido_asistido_favorito(cliente, conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre) VALUES('atletico-madrid', 'ATM'),('rival', 'Rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio', 10000)""")

	conexion.c.execute("""INSERT INTO equipo_estadio VALUES('atletico-madrid', 'estadio')""")

	conexion.c.execute("""INSERT INTO partidos VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

	conexion.c.execute("""INSERT INTO partido_estadio VALUES('20190622', 'estadio')""")

	conexion.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		conexion.insertarPartidoAsistidoFavorito("20190622", "nacho98")

		respuesta=cliente_abierto.get("/partidos/asistidos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="circulo-partido-asistido-favorito">' in contenido
		assert '<div class="tarjeta-partido-asistido-favorito"' in contenido
		assert '<p class="titulo-circulo-partido-asistido-favorito"><strong>Partido Favorito</strong></p>' in contenido
		assert '<div class="info-partido-asistido-favorito">' in contenido