import pytest
from itertools import zip_longest

def test_pagina_insertar_porra_partido_sin_login(cliente):

	data={"partido_id":"20200622", "goles_local":0, "goles_visitante":0}

	respuesta=cliente.post("/insertar_porra_partido", data=data, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_insertar_porra_partido_proximos_partidos_no_hay(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM proximos_partidos")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_id":"20200622", "goles_local":0, "goles_visitante":0}

		respuesta=cliente_abierto.post("/insertar_porra_partido", data=data)

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_insertar_porra_partido_proximos_partidos_equipo_distinto(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('betis')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO proximos_partidos
											VALUES('202006221', 'betis', 'betis', '2020-06-22', '22:00', 'Liga')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_id":"202006221", "goles_local":0, "goles_visitante":0}

		respuesta=cliente_abierto.post("/insertar_porra_partido", data=data)

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_insertar_porra_partido_proximos_partidos_porra_no_disponible(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO proximos_partidos
											VALUES ('20210622', 'atletico-madrid', 'atletico-madrid', '2021-06-22', '22:00', 'Liga'),
											('20190622', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga'),
											('20250622', 'atletico-madrid', 'atletico-madrid', '2025-06-22', '22:00', 'Liga')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_id":"20200622", "goles_local":0, "goles_visitante":0}

		respuesta=cliente_abierto.post("/insertar_porra_partido", data=data)

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

@pytest.mark.parametrize(["goles_local", "goles_visitante"],
	[(100, 1),(0, 10),(32, 2),(22, 5),(1, -9)]
)
def test_pagina_insertar_porra_partido_proximos_partidos_goles_no_validos(cliente, conexion_entorno_usuario, goles_local, goles_visitante):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_id":"20200622", "goles_local":goles_local, "goles_visitante":goles_visitante}

		respuesta=cliente_abierto.post("/insertar_porra_partido", data=data)

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

@pytest.mark.parametrize(["goles_local", "goles_visitante", "goleadores_local", "goleadores_visitante"],
	[
		(0, 0, ["goleador_local1"], ["goleador_visitante1"]),
		(2, 0, ["goleador_local1", "goleador_local2"], ["goleador_visitante1"]),
		(3, 1, ["goleador_local1", "goleador_local2", "goleador_local3"], []),
		(1, 2, ["goleador_local1"], ["goleador_visitante1"])
	]
)
def test_pagina_insertar_porra_partido_proximos_partidos_goleadores_no_validos(cliente, conexion_entorno_usuario, goles_local, goles_visitante, goleadores_local, goleadores_visitante):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_id":"20200622", "goles_local":goles_local, "goles_visitante":goles_visitante}

		goleadores=list(zip_longest(goleadores_local, goleadores_visitante, fillvalue=None))

		for indice, goleadores_local_visitante in enumerate(goleadores):

			local=goleadores_local_visitante[0]

			visitante=goleadores_local_visitante[1]

			if local:

				data[f"local_goleador_{indice+1}"]=local

			if visitante:

				data[f"visitante_goleador_{indice+1}"]=visitante

		respuesta=cliente_abierto.post("/insertar_porra_partido", data=data)

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

@pytest.mark.parametrize(["goles_local", "goles_visitante", "goleadores_local", "goleadores_visitante"],
	[
		(1, 1, ["julian-alvarez"], ["antoine-griezmann"]),
		(2, 0, ["goleador_local1", "antoine-griezmann"], []),
		(3, 1, ["goleador_local1", "goleador_local2", "goleador_local3"], ["julian-alvarez"]),
		(1, 2, ["antoine-griezmann"], ["goleador_visitante1", "julian-alvarez"])
	]
)
def test_pagina_insertar_porra_partido_proximos_partidos_goleadores_no_existen(cliente, conexion_entorno_usuario, goles_local, goles_visitante, goleadores_local, goleadores_visitante):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_id":"20200622", "goles_local":goles_local, "goles_visitante":goles_visitante}

		goleadores=list(zip_longest(goleadores_local, goleadores_visitante, fillvalue=None))

		for indice, goleadores_local_visitante in enumerate(goleadores):

			local=goleadores_local_visitante[0]

			visitante=goleadores_local_visitante[1]

			if local:

				data[f"local_goleador_{indice+1}"]=local

			if visitante:

				data[f"visitante_goleador_{indice+1}"]=visitante

		respuesta=cliente_abierto.post("/insertar_porra_partido", data=data)

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

@pytest.mark.parametrize(["goles_local", "goles_visitante", "goleadores_local", "goleadores_visitante", "numero_goleadores"],
	[
		(1, 1, ["julian-alvarez"], ["antoine-griezmann"], 2),
		(2, 0, ["koke", "antoine-griezmann"], [], 2),
		(3, 1, ["koke", "antoine-griezmann", "koke"], ["julian-alvarez"], 3),
		(1, 2, ["antoine-griezmann"], ["koke", "julian-alvarez"], 3)
	]
)
def test_pagina_insertar_porra_partido_proximos_partidos(cliente, conexion_entorno_usuario, goles_local, goles_visitante,
														goleadores_local, goleadores_visitante, numero_goleadores):

	conexion_entorno_usuario.c.execute("""INSERT INTO jugadores
										VALUES('antoine-griezmann', 'Grizzi', 'atletico-madrid', 'fr', '1324', 100, 100.0, 9, 'DC'),
										('koke', 'Koke', 'atletico-madrid', 'es', '1324', 100, 100.0, 9, 'DC')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_id":"20200622", "goles_local":goles_local, "goles_visitante":goles_visitante}

		goleadores=list(zip_longest(goleadores_local, goleadores_visitante, fillvalue=None))

		for indice, goleadores_local_visitante in enumerate(goleadores):

			local=goleadores_local_visitante[0]

			visitante=goleadores_local_visitante[1]

			if local:

				data[f"local_goleador_{indice+1}"]=local

			if visitante:

				data[f"visitante_goleador_{indice+1}"]=visitante

		respuesta=cliente_abierto.post("/insertar_porra_partido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partido/20200622/porra"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM porra_partidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM porra_goleadores")

		assert len(conexion_entorno_usuario.c.fetchall())==numero_goleadores

def test_pagina_insertar_porra_partido_proximos_partidos_existente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO jugadores
										VALUES('antoine-griezmann', 'Grizzi', 'atletico-madrid', 'fr', '1324', 100, 100.0, 9, 'DC'),
										('koke', 'Koke', 'atletico-madrid', 'es', '1324', 100, 100.0, 9, 'DC')""")

	conexion_entorno_usuario.confirmar()

	conexion_entorno_usuario.insertarPorraPartido("nacho98-20200622", "nacho98", "20200622", 1, 0)

	conexion_entorno_usuario.insertarGoleadorPorra("nacho98-20200622", "julian-alvarez", 1, True)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_id":"20200622", "goles_local":1, "goles_visitante":2}

		goleadores=list(zip_longest(["antoine-griezmann"], ["koke", "julian-alvarez"], fillvalue=None))

		for indice, goleadores_local_visitante in enumerate(goleadores):

			local=goleadores_local_visitante[0]

			visitante=goleadores_local_visitante[1]

			if local:

				data[f"local_goleador_{indice+1}"]=local

			if visitante:

				data[f"visitante_goleador_{indice+1}"]=visitante

		respuesta=cliente_abierto.post("/insertar_porra_partido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partido/20200622/porra"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM porra_partidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM porra_goleadores")

		assert len(conexion_entorno_usuario.c.fetchall())==1