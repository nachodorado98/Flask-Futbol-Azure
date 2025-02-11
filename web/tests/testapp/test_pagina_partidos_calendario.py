import pytest

def test_pagina_partidos_calendario_sin_login(cliente):

	respuesta=cliente.get("/partidos/calendario/2019-06", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_partidos_calendario_sin_partidos(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-06")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_calendario_ano_mes_error(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-13")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_calendario_con_partido_otra_fecha(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-07")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-calendario">' in contenido
		assert "Calendario del " in contenido
		assert '<strong class="ano-mes-filtrado">Julio 2019</strong>' in contenido
		assert "<strong>Junio 2019</strong>" in contenido
		assert '<div class="dias-semana">' in contenido
		assert '<div class="calendario">' in contenido
		assert '<div class="fila">' in contenido
		assert '<div class="dia" onclick="window.location.href' not in contenido
		assert "/partido/20190622" not in contenido
		assert '<p class="numero-dia-partido">' not in contenido
		assert '<div class="dia-proximo">' not in contenido
		assert '<p class="numero-dia-partido-proximo">' not in contenido
		assert '<div class="dia-sin-partido">' in contenido

@pytest.mark.parametrize(["ano_mes"],
	[("2019-08",),("2024-04",),("1998-01",),("1999-06",),("2004-11",)]
)
def test_pagina_partidos_calendario_con_partido_otra_fecha_varios(cliente, conexion_entorno, password_hash, ano_mes):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos/calendario/{ano_mes}")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-calendario">' in contenido
		assert "Calendario del " in contenido
		assert '<div class="dias-semana">' in contenido
		assert '<div class="calendario">' in contenido
		assert '<div class="fila">' in contenido
		assert '<div class="dia" onclick="window.location.href' not in contenido
		assert "/partido/20190622" not in contenido
		assert '<p class="numero-dia-partido">' not in contenido
		assert '<div class="dia-proximo">' not in contenido
		assert '<p class="numero-dia-partido-proximo">' not in contenido
		assert '<div class="dia-sin-partido">' in contenido

def test_pagina_partidos_calendario_con_partido(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-06")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-calendario">' in contenido
		assert "Calendario del " in contenido
		assert '<strong class="ano-mes-filtrado">Junio 2019</strong>' in contenido
		assert "<strong>Junio 2019</strong>" in contenido
		assert '<div class="dias-semana">' in contenido
		assert '<div class="calendario">' in contenido
		assert '<div class="fila">' in contenido
		assert '<div class="dia" onclick="window.location.href' in contenido
		assert "/partido/20190622" in contenido
		assert '<p class="numero-dia-partido">' in contenido
		assert '<div class="dia-proximo">' not in contenido
		assert '<p class="numero-dia-partido-proximo">' not in contenido
		assert '<div class="dia-sin-partido">' in contenido

@pytest.mark.parametrize(["dias"],
	[
		(["01", "13", "22"],),
		(["01", "13", "22", "23"],),
		(["01", "13", "22", "23", "02"],)
	]
)
def test_pagina_partidos_calendario_con_partidos(cliente, conexion, password_hash, dias):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	for dia in dias:

		conexion.c.execute(f"""INSERT INTO partidos
							VALUES ('201906{dia}', 'atletico-madrid', 'atletico-madrid', '2019-06-{dia}', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-06")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-calendario">' in contenido
		assert "Calendario del " in contenido
		assert '<strong class="ano-mes-filtrado">Junio 2019</strong>' in contenido
		assert "<strong>Junio 2019</strong>" in contenido
		assert '<div class="dias-semana">' in contenido
		assert '<div class="calendario">' in contenido
		assert '<div class="fila">' in contenido
		assert '<div class="dia" onclick="window.location.href' in contenido

		for dia in dias:

			assert f"/partido/201906{dia}" in contenido

		assert '<p class="numero-dia-partido">' in contenido
		assert '<div class="dia-proximo">' not in contenido
		assert '<p class="numero-dia-partido-proximo">' not in contenido
		assert '<div class="dia-sin-partido">' in contenido

def test_pagina_partidos_calendario_no_ano_mes_anterior_no_ano_mes_siguiente(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-06")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<button class="button-partidos-calendario-anterior"' not in contenido
		assert '<button class="button-partidos-calendario-siguiente"' not in contenido
		assert "/partidos/calendario/2019-05" not in contenido
		assert "/partidos/calendario/2019-07" not in contenido

def test_pagina_partidos_calendario_si_ano_mes_anterior_no_ano_mes_siguiente(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES ('20190522', 'atletico-madrid', 'atletico-madrid', '2019-05-22', '22:00', 'Liga', '1-0', 'Victoria')""")


	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-06")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<button class="button-partidos-calendario-anterior"' in contenido
		assert '<button class="button-partidos-calendario-siguiente"' not in contenido
		assert "/partidos/calendario/2019-05" in contenido
		assert "/partidos/calendario/2019-07" not in contenido

def test_pagina_partidos_calendario_no_ano_mes_anterior_si_ano_mes_siguiente(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES ('20190722', 'atletico-madrid', 'atletico-madrid', '2019-07-22', '22:00', 'Liga', '1-0', 'Victoria')""")


	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-06")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<button class="button-partidos-calendario-anterior"' not in contenido
		assert '<button class="button-partidos-calendario-siguiente"' in contenido
		assert "/partidos/calendario/2019-05" not in contenido
		assert "/partidos/calendario/2019-07" in contenido

def test_pagina_partidos_calendario_si_ano_mes_anterior_si_ano_mes_siguiente(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES ('20190522', 'atletico-madrid', 'atletico-madrid', '2019-05-22', '22:00', 'Liga', '1-0', 'Victoria'),
										('20190722', 'atletico-madrid', 'atletico-madrid', '2019-07-22', '22:00', 'Liga', '1-0', 'Victoria')""")


	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-06")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<button class="button-partidos-calendario-anterior"' in contenido
		assert '<button class="button-partidos-calendario-siguiente"' in contenido
		assert "/partidos/calendario/2019-05" in contenido
		assert "/partidos/calendario/2019-07" in contenido

def test_pagina_partidos_calendario_con_proximo_partido(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2020-06")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-calendario">' in contenido
		assert "Calendario del " in contenido
		assert '<strong class="ano-mes-filtrado">Junio 2020</strong>' in contenido
		assert "<strong>Junio 2019</strong>" in contenido
		assert '<div class="dias-semana">' in contenido
		assert '<div class="calendario">' in contenido
		assert '<div class="fila">' in contenido
		assert '<div class="dia" onclick="window.location.href' not in contenido
		assert "/partido/20190622" not in contenido
		assert '<p class="numero-dia-partido">' not in contenido
		assert '<div class="dia-proximo">' in contenido
		assert '<p class="numero-dia-partido-proximo">' in contenido
		assert '<div class="dia-sin-partido">' in contenido

def test_pagina_partidos_calendario_con_partido_y_proximo_partido(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO proximos_partidos
						VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-06")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-calendario">' in contenido
		assert "Calendario del " in contenido
		assert '<strong class="ano-mes-filtrado">Junio 2019</strong>' in contenido
		assert "<strong>Junio 2019</strong>" in contenido
		assert '<div class="dias-semana">' in contenido
		assert '<div class="calendario">' in contenido
		assert '<div class="fila">' in contenido
		assert '<div class="dia" onclick="window.location.href' in contenido
		assert "/partido/20190622" in contenido
		assert '<p class="numero-dia-partido">' in contenido
		assert '<div class="dia-proximo">' in contenido
		assert '<p class="numero-dia-partido-proximo">' in contenido
		assert '<div class="dia-sin-partido">' in contenido