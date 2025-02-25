import pytest

def test_pagina_partidos_asistidos_equipo_sin_login(cliente):

	respuesta=cliente.get("/equipos/mis_equipos/partidos_equipo/atletico-madrid", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_partidos_asistidos_equipo_sin_partidos(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM partidos")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipos/mis_equipos/partidos_equipo/atletico-madrid")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_asistidos_equipo_sin_partidos_asistidos(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipos/mis_equipos/partidos_equipo/atletico-madrid")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_asistidos_equipo_sin_equipos(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/equipos/mis_equipos/partidos_equipo/no_existo")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_asistidos_equipo_con_partido_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/equipos/mis_equipos/partidos_equipo/atletico-madrid")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos contra " in contenido
		assert '<div class="contenedor-titulo-partidos-asistidos-equipo">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-partidos-asistidos-equipo">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-equipo-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos-equipo"' in contenido
		assert '<div class="info-partido-asistidos-equipo">' in contenido
		assert '<p class="valor-circulo-partidos-asistidos-equipo"><strong>1</strong></p>' in contenido
		assert '<p class="titulo-circulo-equipo">Atletico</p>'

@pytest.mark.parametrize(["cantidad_partidos", "cantidad_partidos_asistidos"],
	[(1,1),(2,1),(10,6),(7,3),(22,15)]
)
def test_pagina_partidos_asistidos_equipo_con_partidos_asistidos(cliente, conexion, password_hash, cantidad_partidos, cantidad_partidos_asistidos):
	
	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	for numero in range(cantidad_partidos):

		conexion.c.execute("""INSERT INTO partidos
							VALUES (%s, 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""",
							(f"2019{numero+1}",))

	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero_asistidos in range(cantidad_partidos_asistidos):

			data={"partido_anadir":f"2019{numero_asistidos+1}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/equipos/mis_equipos/partidos_equipo/rival")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos contra " in contenido
		assert '<div class="contenedor-titulo-partidos-asistidos-equipo">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-equipo">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-equipo-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos-equipo"' in contenido
		assert '<div class="info-partido-asistidos-equipo">' in contenido
		assert f'<p class="valor-circulo-partidos-asistidos-equipo"><strong>{cantidad_partidos_asistidos}</strong></p>' in contenido
		assert '<p class="titulo-circulo-equipo">Atletico</p>'

def test_pagina_partidos_asistidos_equipo_partido_asistido_estadisticas(cliente, conexion, password_hash):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
							VALUES ('20190622', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")
	
	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/equipos/mis_equipos/partidos_equipo/rival")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="circulo-estadisticas-partidos-asistidos-equipo">' in contenido
		assert '<canvas id="grafico_tarta">' in contenido
		assert "var datos_grafica_tarta=" in contenido