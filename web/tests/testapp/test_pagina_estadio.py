import pytest
import os

def test_pagina_estadio_sin_login(cliente):

	respuesta=cliente.get("/estadio/estadio", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_estadio_estadio_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/estadio")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_estadio_estadio(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadio"' in contenido
		assert '<div class="equipo-estadio">' in contenido
		assert '<img class="escudo-equipo"' in contenido
		assert '<p class="nombre">' in contenido
		assert '<p class="direccion">' in contenido
		assert '<div class="info-estadio-detalle">' in contenido
		assert '<p class="fecha-fundacion">' in contenido
		assert '<p class="espectadores">' in contenido
		assert '<p class="dimensiones">' in contenido
		assert '<p class="titulo-circulo-numero-veces-asistido">' in contenido
		assert "Veces Asistido" in contenido
		assert '<p class="valor-circulo-numero-veces-asistido"><strong>0</strong></p>' in contenido
		assert "iframe" in contenido
		assert "/estadio/mapa/mapa_small_estadio_user_" in contenido
		assert '<img class="no-mapa"' not in contenido
		assert '<div class="circulo-ultimo-partido-estadio">' in contenido
		assert '<div class="tarjeta-ultimo-partido-estadio"' in contenido
		assert '<div class="info-ultimo-partido-estadio">' in contenido
		assert '<div class="circulo-ultimo-partido-asistido-estadio">' not in contenido
		assert '<div class="tarjeta-ultimo-partido-asistido-estadio"' not in contenido
		assert '<div class="info-ultimo-partido-asistido-estadio">' not in contenido

def test_pagina_estadio_estadio_sin_equipo(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""DELETE FROM equipo_estadio""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadio"' in contenido
		assert '<p class="equipo-estadio">' not in contenido

def test_pagina_estadio_estadio_sin_direccion(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE estadios SET direccion=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadio"' in contenido
		assert '<p class="direccion">' not in contenido

def test_pagina_estadio_estadio_sin_fundacion(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE estadios SET fecha=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadio"' in contenido
		assert '<p class="fecha-fundacion">' not in contenido

def test_pagina_estadio_estadio_sin_espectadores(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE estadios SET capacidad=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadio"' in contenido
		assert '<p class="espectadores">' not in contenido

def test_pagina_estadio_estadio_sin_ancho(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE estadios SET ancho=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadio"' in contenido
		assert '<p class="dimensiones">' not in contenido

def test_pagina_estadio_estadio_sin_largo(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE estadios SET largo=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadio"' in contenido
		assert '<p class="dimensiones">' not in contenido

def test_pagina_estadio_estadio_no_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="estadio-asistido"' not in contenido
		assert '<p class="titulo-circulo-numero-veces-asistido">' in contenido
		assert "Veces Asistido" in contenido
		assert '<p class="valor-circulo-numero-veces-asistido"><strong>0</strong></p>' in contenido

def test_pagina_estadio_estadio_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="estadio-asistido"' in contenido
		assert '<p class="titulo-circulo-numero-veces-asistido">' in contenido
		assert "Veces Asistido" in contenido
		assert '<p class="valor-circulo-numero-veces-asistido"><strong>1</strong></p>' in contenido

@pytest.mark.parametrize(["veces"],
	[(10,),(2,),(16,),(7,),(22,)]
)
def test_pagina_estadio_estadio_asistido_varias_veces(cliente, conexion_entorno_usuario, veces):

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partidos
								VALUES ('20190622{numero}', 'atletico-madrid', 'rival', '2019-06-22', '22:00', 'Liga', '1-0', 'Local')""")

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero}', 'metropolitano')""")

			conexion_entorno_usuario.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"Comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="estadio-asistido"' in contenido
		assert '<p class="titulo-circulo-numero-veces-asistido">' in contenido
		assert "Veces Asistido" in contenido
		assert f'<p class="valor-circulo-numero-veces-asistido"><strong>{veces}</strong></p>' in contenido

def test_pagina_estadio_error_mapas(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE estadios SET Latitud=NULL, Longitud=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" not in contenido
		assert "/estadio/mapa/mapa_small_estadio_user_" not in contenido
		assert '<img class="no-mapa"' in contenido

def test_pagina_estadio_mapa_small(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert "/estadio/mapa/mapa_small_estadio_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_small_estadio_user_nacho98.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",),("golden",),("amanda",),("amanda99",),("nacho98",)]
)
def test_pagina_estadio_mapa_small_usuarios(cliente, conexion_entorno, password_hash, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)
		
		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert f"/estadio/mapa/mapa_small_estadio_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_small_estadio_user_{usuario}.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

def test_pagina_estadio_mapa_small_otro_usuario(cliente, conexion_entorno_usuario, password_hash):

	conexion_entorno_usuario.insertarUsuario("otro", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)
		
		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadio/metropolitano")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_small_estadio_user_otro.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

	with cliente as cliente_abierto:

		conexion_entorno_usuario.c.execute("""INSERT INTO estadios (Estadio_Id, Nombre, Capacidad, Latitud, Longitud, Codigo_Estadio, Codigo_Pais) VALUES('estadio', 'Nombre Estadio', 100000, 1.0, -1.0, 22619, 'pais')""")
		
		conexion_entorno_usuario.c.execute("""INSERT INTO partidos VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")
		
		conexion_entorno_usuario.c.execute("""INSERT INTO partido_estadio VALUES('20190623', 'estadio')""")
		
		conexion_entorno_usuario.confirmar()

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)
		
		data={"partido_anadir":"20190623", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadio/estadio")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_small_estadio_user_nacho98.html")

		assert os.path.exists(ruta_mapa2)

		with open(ruta_mapa2, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[1.0, -1.0]" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

def test_pagina_mapa_estadio_sin_login(cliente):

	respuesta=cliente.get("/estadio/mapa/nombre_mapa", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mapa_estadio_mapa_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		with pytest.raises(FileNotFoundError):

			cliente_abierto.get("/estadio/mapa/nombre_mapa.html")

def test_pagina_mapa_estadio_mapa_small_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadio/metropolitano")

		respuesta=cliente_abierto.get("/estadio/mapa/mapa_small_estadio_user_nacho98.html")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "[40.436, -3.599]" in contenido
		assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

def test_pagina_estadio_estadio_sin_ultimo_partido(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM partidos")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="circulo-ultimo-partido-estadio">' not in contenido
		assert '<div class="tarjeta-ultimo-partido-estadio"' not in contenido
		assert '<div class="info-ultimo-partido-estadio">' not in contenido

def test_pagina_estadio_estadio_con_ultimo_partido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="circulo-ultimo-partido-estadio">' in contenido
		assert '<div class="tarjeta-ultimo-partido-estadio"' in contenido
		assert '<div class="info-ultimo-partido-estadio">' in contenido

def test_pagina_estadio_estadio_con_ultimo_partido_varios(cliente, conexion_entorno_usuario):

	for numero in range(8):

		conexion_entorno_usuario.c.execute(f"""INSERT INTO partidos
									VALUES('{numero}', 'atletico-madrid', 'atletico-madrid', '201{numero}-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno_usuario.c.execute(f"""INSERT INTO partido_estadio
									VALUES('{numero}', 'metropolitano')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="circulo-ultimo-partido-estadio">' in contenido
		assert '<div class="tarjeta-ultimo-partido-estadio"' in contenido
		assert '<div class="info-ultimo-partido-estadio">' in contenido
		assert '<p><strong>22/06/2019</strong></p>' in contenido

def test_pagina_estadio_estadio_sin_ultimo_partido_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="circulo-ultimo-partido-asistido-estadio">' not in contenido
		assert '<div class="tarjeta-ultimo-partido-asistido-estadio"' not in contenido
		assert '<div class="info-ultimo-partido-asistido-estadio">' not in contenido

def test_pagina_estadio_estadio_con_ultimo_partido_asistido(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.insertarPartidoAsistido("20190622", "nacho98", "comentario")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="circulo-ultimo-partido-asistido-estadio">' in contenido
		assert '<div class="tarjeta-ultimo-partido-asistido-estadio"' in contenido
		assert '<div class="info-ultimo-partido-asistido-estadio">' in contenido

def test_pagina_estadio_estadio_con_ultimo_partido_asistido_varios(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.insertarPartidoAsistido("20190622", "nacho98", "comentario")

	for numero in range(8):

		conexion_entorno_usuario.c.execute(f"""INSERT INTO partidos
									VALUES('{numero}', 'atletico-madrid', 'atletico-madrid', '202{numero}-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno_usuario.c.execute(f"""INSERT INTO partido_estadio
									VALUES('{numero}', 'metropolitano')""")

		conexion_entorno_usuario.insertarPartidoAsistido(numero, "nacho98", "comentario")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio/metropolitano")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="circulo-ultimo-partido-asistido-estadio">' in contenido
		assert '<div class="tarjeta-ultimo-partido-asistido-estadio"' in contenido
		assert '<div class="info-ultimo-partido-asistido-estadio">' in contenido
		assert '<p><strong>22/06/2027</strong></p>' in contenido