import pytest

def test_pagina_partidos_asistidos_competicion_sin_login(cliente):

	respuesta=cliente.get("/competiciones/mis_competiciones/partidos_competicion/primera", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_partidos_asistidos_competicion_sin_partidos(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM partidos")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_asistidos_competicion_sin_partidos_asistidos(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_asistidos_competicion_sin_competiciones(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM competiciones")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partidos_asistidos_competicion_con_partido_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos en " in contenido
		assert '<div class="contenedor-titulo-partidos-asistidos-competicion">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-partidos-asistidos-competicion">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-competicion-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos-competicion"' in contenido
		assert '<div class="info-partido-asistidos-competicion">' in contenido
		assert '<p class="valor-circulo-partidos-asistidos-competicion"><strong>1</strong></p>' in contenido
		assert '<p class="titulo-circulo-competicion">Primera</p>'

@pytest.mark.parametrize(["cantidad_partidos", "cantidad_partidos_asistidos"],
	[(1,1),(2,1),(10,6),(7,3),(22,15)]
)
def test_pagina_partidos_asistidos_competicion_con_partidos_asistidos(cliente, conexion, password_hash, cantidad_partidos, cantidad_partidos_asistidos):
	
	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO competiciones (Competicion_Id, Nombre, Codigo_Pais) VALUES('primera', 'Primera', 'es')""")

	for numero in range(cantidad_partidos):

		conexion.c.execute("""INSERT INTO partidos
							VALUES (%s, 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""",
							(f"2019{numero+1}",))

		conexion.c.execute("""INSERT INTO partido_competicion VALUES(%s, 'primera')""", (f"2019{numero+1}",))

	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero_asistidos in range(cantidad_partidos_asistidos):

			data={"partido_anadir":f"2019{numero_asistidos+1}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "Partidos Asistidos en " in contenido
		assert '<div class="contenedor-titulo-partidos-asistidos-competicion">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-partidos-asistidos-competicion">' in contenido
		assert '<div class="tarjetas-partidos-asistidos-competicion-wrapper">' in contenido
		assert '<div class="tarjeta-partido-asistidos-competicion"' in contenido
		assert '<div class="info-partido-asistidos-competicion">' in contenido
		assert f'<p class="valor-circulo-partidos-asistidos-competicion"><strong>{cantidad_partidos_asistidos}</strong></p>' in contenido
		assert '<p class="titulo-circulo-competicion">Primera</p>'

def test_pagina_partidos_asistidos_competicion_partido_asistido_estadisticas(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones/partidos_competicion/primera")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="circulo-estadisticas-partidos-asistidos-competicion">' in contenido
		assert '<canvas id="grafico_tarta">' in contenido
		assert "var datos_grafica_tarta=" in contenido