import pytest

def test_pagina_mis_estadios_division_sin_login(cliente):

	respuesta=cliente.get("/estadios/mis_estadios/division/primera", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mis_estadios_division_estadios_no_existen(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM estadios")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/division/primera")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_division_division_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/division/no-existo")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_division_partidos_asistidos_no_existen(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/division/primera")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-division"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-division">' in contenido
		assert "primera-division-ea.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-division">' in contenido
		assert '<div class="tarjeta-estadio-asistido-division" onclick="window.location.href=' not in contenido
		assert 'style="background-color: #d1d1d1;"' in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-division">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-division"><strong>0 / 1</strong></p>' in contenido

def test_pagina_mis_estadios_division_competicion_equipo_nula(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("UPDATE equipos SET Codigo_Competicion=NULL")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/division/primera")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_division(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/division/primera")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-division"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-division">' in contenido
		assert "primera-division-ea.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-division">' in contenido
		assert '<div class="tarjeta-estadio-asistido-division" onclick="window.location.href=' in contenido
		assert "/estadio/metropolitano" in contenido
		assert 'style="background-color: #d1d1d1;"' not in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-division">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-division"><strong>1 / 1</strong></p>' in contenido

@pytest.mark.parametrize(["estadios"],
	[(2,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_estadios_division_varios_estadios_division(cliente, conexion_entorno_usuario, estadios):

	for numero in range(1, estadios):

		conexion_entorno_usuario.c.execute(f"""INSERT INTO equipos (Equipo_Id, Competicion, Codigo_Competicion) VALUES('equipo{numero}', 'Primera', 'primera')""")

		conexion_entorno_usuario.c.execute(f"""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio{numero}', 100000)""")

		conexion_entorno_usuario.c.execute(f"""INSERT INTO equipo_estadio VALUES('equipo{numero}', 'estadio{numero}')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/division/primera")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-division"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-division">' in contenido
		assert "primera-division-ea.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-division">' in contenido
		assert '<div class="tarjeta-estadio-asistido-division" onclick="window.location.href=' in contenido
		assert "/estadio/metropolitano" in contenido
		assert 'style="background-color: #d1d1d1;"' in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-division">' in contenido
		assert "Estadios Visitados" in contenido
		assert f'<p class="valor-circulo-estadios-asistidos-division"><strong>1 / {estadios}</strong></p>' in contenido

		for numero in range(1, estadios):
			assert f"/estadio/estadio{numero}" not in contenido