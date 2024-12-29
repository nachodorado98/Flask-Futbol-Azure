import pytest

def test_pagina_mis_equipos_sin_login(cliente):

	respuesta=cliente.get("/equipos/mis_equipos", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mis_equipos_equipos_no_existen(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno.c.execute("""DELETE FROM equipos""")

		conexion_entorno.confirmar()

		respuesta=cliente_abierto.get("/equipos/mis_equipos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location==r"/login?next=%2Fequipos%2Fmis_equipos"
		assert "Redirecting..." in contenido

def test_pagina_mis_equipos_partidos_asistidos_no_existen(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipos/mis_equipos")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_equipos_equipos_enfrentados_no_existen(cliente, conexion, password_hash):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		conexion.c.execute("""DELETE FROM equipos WHERE equipo_id='rival'""")

		conexion.confirmar()

		respuesta=cliente_abierto.get("/equipos/mis_equipos")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_equipos(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos VALUES('20190623', 'rival', 'atletico-madrid', '2019-06-23', '20:00', 'Liga', '1-0', 'Victoria Local')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190623", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/equipos/mis_equipos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-equipos-enfrentados"' in contenido
		assert '<p class="titulo-pagina-equipos-enfrentados">' in contenido
		assert '<div class="tarjetas-equipos-enfrentados">' in contenido
		assert '<div class="tarjeta-equipo-enfrentado"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-equipos-enfrentados">' in contenido
		assert "Equipos Enfrentados" in contenido
		assert '<p class="valor-circulo-equipos-enfrentados"><strong>1</strong></p>' in contenido

@pytest.mark.parametrize(["veces"],
	[(1,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_equipos_varias_veces(cliente, conexion_entorno, password_hash, veces):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'rival', 'atletico-madrid', '2019-06-23', '20:00', 'Liga', '1-0', 'Victoria Local')""")

			conexion_entorno.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/equipos/mis_equipos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-equipos-enfrentados"' in contenido
		assert '<p class="titulo-pagina-equipos-enfrentados">' in contenido
		assert '<div class="tarjetas-equipos-enfrentados">' in contenido
		assert '<div class="tarjeta-equipo-enfrentado"' in contenido
		assert f"<h4>{veces} veces</h4>" in contenido

def test_pagina_mis_equipos_equipo_enfrentado(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos VALUES('20190623', 'rival', 'atletico-madrid', '2019-06-23', '20:00', 'Liga', '1-0', 'Victoria Local')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190623", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/equipos/mis_equipos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-equipos-enfrentados">' in contenido
		assert "Equipos Enfrentados" in contenido
		assert '<p class="valor-circulo-equipos-enfrentados"><strong>1</strong></p>' in contenido

@pytest.mark.parametrize(["veces"],
	[(1,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_equipos_equipo_enfrentado_varias_veces(cliente, conexion_entorno, password_hash, veces):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'rival', 'atletico-madrid', '2019-06-23', '20:00', 'Liga', '1-0', 'Victoria Local')""")

			conexion_entorno.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/equipos/mis_equipos")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert f"<h4>{veces} veces</h4>" in contenido
		assert '<p class="titulo-circulo-equipos-enfrentados">' in contenido
		assert "Equipos Enfrentados" in contenido
		assert '<p class="valor-circulo-equipos-enfrentados"><strong>1</strong></p>' in contenido