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

def test_pagina_partidos_calendario_con_partido(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partidos/calendario/2019-06")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-calendario">' in contenido
		assert "Calendario del " in contenido
		assert '<strong class="ano-mes-filtrado">2019-06</strong>' in contenido
		assert '<div class="dias-semana">' in contenido
		assert '<div class="calendario">' in contenido
		assert '<div class="fila">' in contenido
		assert '<div class="dia">' in contenido
		assert '2019-06-01' in contenido
		assert '2019-06-22' in contenido
		assert '2019-06-30' in contenido

@pytest.mark.parametrize(["ano_mes"],
	[("2019-06",),("2024-04",),("1998-01",),("1999-06",),("2004-11",)]
)
def test_pagina_partidos_calendario_con_partido_varios(cliente, conexion, password_hash, ano_mes):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.c.execute(f"""INSERT INTO partidos
						VALUES ('20190622', 'atletico-madrid', 'atletico-madrid', '{ano_mes}-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/partidos/calendario/{ano_mes}")
	
		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-calendario">' in contenido
		assert "Calendario del " in contenido
		assert f'<strong class="ano-mes-filtrado">{ano_mes}</strong>' in contenido
		assert '<div class="dias-semana">' in contenido
		assert '<div class="calendario">' in contenido
		assert '<div class="fila">' in contenido
		assert '<div class="dia">' in contenido
		assert f'{ano_mes}-01' in contenido
		assert f'{ano_mes}-22' in contenido
		assert f'{ano_mes}-30' in contenido