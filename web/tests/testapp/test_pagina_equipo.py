def test_pagina_equipo_sin_login(cliente):

	respuesta=cliente.get("/equipo/equipo", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_equipo_equipo_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/equipo")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_equipo_equipo(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-equipo"' in contenido
		assert '<p class="nombre-largo">' in contenido
		assert '<div class="info-equipo">' in contenido
		assert '<p class="fundacion">' in contenido
		assert '<p class="competicion"' in contenido
		assert '<p class="ubicacion">' in contenido
		assert '<img class="pais-equipo"' in contenido
		assert '<p class="temporadas">' in contenido
		assert '<div class="info-equipo-imagenes">' in contenido
		assert '<div class="info-entrenador"' in contenido
		assert '<div class="info-equipo">' in contenido
		assert '<div class="info-estadio"' in contenido
		assert '<div class="info-jugador"' in contenido
		assert '<div class="info-ultimo-partido"' in contenido
		assert '<div class="tarjeta-jugadores-equipo">' in contenido
		assert '<p class="titulo-equipo-jugadores">' in contenido
		assert '<div class="tarjetas-jugadores-equipo">' in contenido

def test_pagina_equipo_equipo_sin_fundacion(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE equipos SET fundacion=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo">' in contenido
		assert '<p class="fundacion">' not in contenido

def test_pagina_equipo_equipo_sin_competicion(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE equipos SET competicion=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo">' in contenido
		assert '<p class="competicion">' not in contenido

def test_pagina_equipo_equipo_sin_ciudad(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE equipos SET ciudad=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo">' in contenido
		assert '<p class="ubicacion">' not in contenido

def test_pagina_equipo_equipo_sin_pais(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE equipos SET pais=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo">' in contenido
		assert '<p class="ubicacion">' not in contenido

def test_pagina_equipo_equipo_sin_temporadas(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE equipos SET temporadas=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo">' in contenido
		assert '<p class="temporadas">' not in contenido

def test_pagina_equipo_equipo_sin_entrenador(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE equipos SET entrenador=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo-imagenes">' in contenido
		assert '<div class="info-entrenador">' not in contenido

def test_pagina_equipo_equipo_sin_presidente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE equipos SET presidente=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo-imagenes">' in contenido
		assert '<div class="info-presidente">' not in contenido

def test_pagina_equipo_equipo_sin_estadio(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM estadios")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo-imagenes">' in contenido
		assert '<div class="info-estadio">' not in contenido

def test_pagina_equipo_equipo_sin_jugador(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM jugadores")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo-imagenes">' in contenido
		assert '<div class="info-jugador">' not in contenido

def test_pagina_equipo_equipo_sin_partido(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM partidos")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="info-equipo-imagenes">' in contenido
		assert '<div class="info-ultimo-partido"' not in contenido

def test_pagina_equipo_equipo_favorito(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="favorito"' in contenido

def test_pagina_equipo_equipo_no_favorito(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id)  VALUES('rival')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/rival")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="favorito"' not in contenido

def test_pagina_equipo_equipo_con_competiciones_existentes(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<p class="competicion" onclick="window.location.href=' in contenido
		assert '<p class="competicion">' not in contenido

def test_pagina_equipo_equipo_sin_competiciones_existentes(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM competiciones""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<p class="competicion" onclick="window.location.href=' not in contenido
		assert '<p class="competicion">' in contenido

def test_pagina_equipo_equipo_sin_jugadores(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM jugadores""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/equipo/atletico-madrid")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-jugadores-equipo">' in contenido
		assert '<p class="titulo-equipo-jugadores">' in contenido
		assert '<div class="tarjetas-jugadores-equipo">' not in contenido