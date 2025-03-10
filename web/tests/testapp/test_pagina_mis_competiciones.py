import pytest

def test_pagina_mis_competiciones_sin_login(cliente):

	respuesta=cliente.get("/competiciones/mis_competiciones", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mis_competiciones_competiciones_no_existen(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM competiciones")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_competiciones_partidos_asistidos_no_existen(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_competiciones_competiciones_asistidas_no_existen(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM competiciones")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_competiciones(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-competiciones-asistidas"' in contenido
		assert '<p class="titulo-pagina-competiciones-asistidas">' in contenido
		assert '<div class="tarjetas-competiciones-asistidas">' in contenido
		assert '<div class="tarjeta-competicion-asistida"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-competiciones-asistidas">' in contenido
		assert "Competiciones Asistidas" in contenido
		assert '<p class="valor-circulo-competiciones-asistidas"><strong>1</strong></p>' in contenido

@pytest.mark.parametrize(["veces"],
	[(1,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_competiciones_varias_veces(cliente, conexion_entorno_usuario, veces):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partido_competicion VALUES('20190622{numero}', 'primera')""")

			conexion_entorno_usuario.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-competiciones-asistidas"' in contenido
		assert '<p class="titulo-pagina-competiciones-asistidas">' in contenido
		assert '<div class="tarjetas-competiciones-asistidas">' in contenido
		assert '<div class="tarjeta-competicion-asistida"' in contenido
		assert f"<h4>{veces} veces</h4>" in contenido
		assert '<p class="titulo-circulo-competiciones-asistidas">' in contenido
		assert "Competiciones Asistidas" in contenido
		assert '<p class="valor-circulo-competiciones-asistidas"><strong>1</strong></p>' in contenido

def test_pagina_mis_competiciones_competicion_asistida(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-competiciones-asistidas">' in contenido
		assert "Competiciones Asistidas" in contenido
		assert '<p class="valor-circulo-competiciones-asistidas"><strong>1</strong></p>' in contenido

@pytest.mark.parametrize(["veces"],
	[(1,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_competiciones_competicion_asistida_varias_veces(cliente, conexion_entorno_usuario, veces):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partido_competicion VALUES('20190622{numero}', 'primera')""")

			conexion_entorno_usuario.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/competiciones/mis_competiciones")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert f"<h4>{veces} veces</h4>" in contenido
		assert '<p class="titulo-circulo-competiciones-asistidas">' in contenido
		assert "Competiciones Asistidas" in contenido
		assert '<p class="valor-circulo-competiciones-asistidas"><strong>1</strong></p>' in contenido