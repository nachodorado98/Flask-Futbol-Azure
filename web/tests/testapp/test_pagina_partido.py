import pytest

def test_pagina_partido_sin_login(cliente):

	respuesta=cliente.get("/partido/1", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_partido_partido_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/1")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_equipo_no_pertenece(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('equipo-no-partido')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "equipo-no-partido")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_con_estadio(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-detalle"' in contenido
		assert '<p class="competicion"' in contenido
		assert '<div class="info-partido-detalle">' in contenido
		assert '<div class="info-partido-estadio"' in contenido

def test_pagina_partido_sin_estadio(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM estadios")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-detalle"' in contenido
		assert '<p class="competicion"' in contenido
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
def test_pagina_partido_temporada(cliente, conexion, password_hash, partido_id, temporada):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES(%s, 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""",
						(partido_id,))

	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/{partido_id}")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert f'/partidos?temporada={temporada}' in contenido

def test_pagina_partido_no_partido_anterior_no_partido_siguiente(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior"' not in contenido
		assert '<button class="button-partido-siguiente"' not in contenido

def test_pagina_partido_no_partido_anterior_si_partido_siguiente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior"' not in contenido
		assert '<button class="button-partido-siguiente"' in contenido

def test_pagina_partido_si_partido_anterior_no_partido_siguiente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior"' in contenido
		assert '<button class="button-partido-siguiente"' not in contenido

def test_pagina_partido_si_partido_anterior_si_partido_siguiente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria'),
									('202454564', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior"' in contenido
		assert '<button class="button-partido-siguiente"' in contenido

def test_pagina_partido_con_competicion(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<strong class="strong-competicion" onclick="window.location.href=' in contenido
		assert '<strong class="strong-competicion">' not in contenido

def test_pagina_partido_sin_competicion(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM partido_competicion""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<strong class="strong-competicion" onclick="window.location.href=' not in contenido
		assert '<strong class="strong-competicion">' in contenido

def test_pagina_partido_sin_goleadores(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM partido_goleador""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-partido-goleadores">' not in contenido
		assert '<div class="columna-local">' not in contenido
		assert '<div class="fila-goleador-local"' not in contenido
		assert '<div class="columna-visitante">' not in contenido
		assert '<div class="fila-goleador-visitante"' not in contenido

def test_pagina_partido_con_goleadores(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-partido-goleadores">' in contenido
		assert '<div class="columna-local">' in contenido
		assert '<div class="fila-goleador-local"' in contenido
		assert '<div class="columna-visitante">' in contenido
		assert '<div class="fila-goleador-visitante"' in contenido

def test_pagina_partido_con_goleadores_local(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM partido_goleador WHERE Local=False""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-partido-goleadores">' in contenido
		assert '<div class="columna-local">' in contenido
		assert '<div class="fila-goleador-local"' in contenido
		assert '<div class="columna-visitante">' in contenido
		assert '<div class="fila-goleador-visitante"' not in contenido

def test_pagina_partido_con_goleadores_visitante(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM partido_goleador WHERE Local=True""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-partido-goleadores">' in contenido
		assert '<div class="columna-local">' in contenido
		assert '<div class="fila-goleador-local"' not in contenido
		assert '<div class="columna-visitante">' in contenido
		assert '<div class="fila-goleador-visitante"' in contenido

def test_pagina_partido_con_historial_entre_equipos(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM partidos""")

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival'),('otro')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
								VALUES('20190621', 'atletico-madrid', 'otro', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria Local'),
										('20190622', 'rival', 'atletico-madrid', '2019-07-22', '20:00', 'Liga', '1-0', 'Empate'),
										('20190623', 'atletico-madrid', 'rival', '2024-06-22', '20:00', 'Liga', '1-0', 'Victoria Local'),
										('20190624', 'rival', 'otro', '2020-12-02', '20:00', 'Liga', '1-0', 'Victoria Local'),
										('20190625', 'rival', 'atletico-madrid', '2019-04-13', '20:00', 'Liga', '1-0', 'Victoria Visitante')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-historial-entre-equipos">' in contenido
		assert '<div class="historial-container">' in contenido
		assert '<div class="columna-historial">' in contenido
		assert '<div class="fila-titulo-historial">' in contenido
		assert 'Victorias' in contenido
		assert 'Empates' in contenido
		assert '<div class="fila-datos-historial">' in contenido
		assert '<h4>2</h4>' in contenido
		assert '<h4>1</h4>' in contenido
		assert '<h4>0</h4>' in contenido

def test_pagina_partido_con_partidos_entre_equipos(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM partidos""")

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival'),('otro')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
								VALUES('20190621', 'atletico-madrid', 'otro', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria Local'),
										('20190622', 'rival', 'atletico-madrid', '2019-07-22', '20:00', 'Liga', '1-0', 'Empate'),
										('20190623', 'atletico-madrid', 'rival', '2024-06-22', '20:00', 'Liga', '1-0', 'Victoria Local'),
										('20190624', 'rival', 'otro', '2020-12-02', '20:00', 'Liga', '1-0', 'Victoria Local'),
										('20190625', 'rival', 'atletico-madrid', '2019-04-13', '20:00', 'Liga', '1-0', 'Victoria Visitante')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<p class="titulo-partidos-entre-equipos">' in contenido
		assert '<div class="tarjetas-partidos-entre-equipos">' in contenido

def test_pagina_partido_partido_no_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="icono-partido-asistido"' in contenido
		assert '/partido_asistido.png' not in contenido
		assert '/anadir_partido_asistido.png' in contenido
		assert 'alt="Partido No Asistido Icon"' in contenido
		assert 'alt="Partido Asistido Icon"' not in contenido

def test_pagina_partido_partido_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":"comentario"})

		respuesta=cliente_abierto.get("/partido/20190622")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="icono-partido-asistido"' in contenido
		assert '/partido_asistido.png' in contenido
		assert '/anadir_partido_asistido.png' not in contenido
		assert 'alt="Partido No Asistido Icon"' not in contenido
		assert 'alt="Partido Asistido Icon"' in contenido