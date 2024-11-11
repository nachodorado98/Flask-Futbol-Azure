import pytest

def test_pagina_mis_estadios_pais_sin_login(cliente):

	respuesta=cliente.get("/estadios/mis_estadios/es", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mis_estadios_pais_estadios_no_existen(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM estadios")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/pais")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_pais_partidos_asistidos_no_existen(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/pais")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_pais_estadios_asistidos_no_existen(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM estadios")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_pais_codigos_pais_estadio_equipo_nulos(cliente, conexion_entorno):

	conexion_entorno.c.execute("UPDATE estadios SET Codigo_Pais=NULL")

	conexion_entorno.c.execute("UPDATE equipos SET Codigo_Pais=NULL")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

@pytest.mark.parametrize(["pais"],
	[("se",),("ese",),("p",),("nl",),("pt",)]
)
def test_pagina_mis_estadios_pais_codigo_pais_no_existe(cliente, conexion_entorno, pais):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get(f"/estadios/mis_estadios/{pais}")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_pais(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-pais"><strong>1</strong></p>' in contenido

def test_pagina_mis_estadios_pais_codigo_pais_estadio_nulo(cliente, conexion_entorno):

	conexion_entorno.c.execute("UPDATE estadios SET Codigo_Pais=NULL")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-pais"><strong>1</strong></p>' in contenido

def test_pagina_mis_estadios_pais_codigo_pais_equipo_nulo(cliente, conexion_entorno):

	conexion_entorno.c.execute("UPDATE equipos SET Codigo_Pais=NULL")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-pais"><strong>1</strong></p>' in contenido

@pytest.mark.parametrize(["veces"],
	[(1,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_estadios_pais_varias_veces(cliente, conexion_entorno, veces):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

			conexion_entorno.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero}', 'metropolitano')""")

			conexion_entorno.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert f"<h4>{veces} veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-pais"><strong>1</strong></p>' in contenido

@pytest.mark.parametrize(["veces"],
	[(2,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_estadios_pais_varios(cliente, conexion_entorno, veces):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno.c.execute(f"""INSERT INTO estadios (Estadio_Id, Capacidad, Pais, Codigo_Pais) VALUES('estadio{numero}', 100000, 'España', 'es')""")

			conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

			conexion_entorno.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero}', 'estadio{numero}')""")

			conexion_entorno.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert f"<h4>{veces} veces</h4>" not in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert f'<p class="valor-circulo-estadios-asistidos-pais"><strong>{veces}</strong></p>' in contenido