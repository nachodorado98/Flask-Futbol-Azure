import pytest
import os

def test_pagina_wrapped_sin_login(cliente):

	respuesta=cliente.get("/wrapped/2019", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["annio"],
	[(0,),(2025,),("2021",),("annio",),("hola",),(2020,)]
)
def test_pagina_wrapped_no_hay_asistidos(cliente, conexion_entorno_usuario, annio):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get(f"/wrapped/{annio}")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_wrapped(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-wrapped">' in contenido
		assert '<p class="titulo-pagina-wrapped"><strong>Wrapped 2019</strong></p>' in contenido
		assert '<div class="tarjeta-dato"' in contenido
		assert "abrirVentana('ventana-emergente-partidos')" in contenido
		assert '<p><strong>Partidos</strong></p>' in contenido
		assert "abrirVentana('ventana-emergente-estadios')" in contenido
		assert '<p><strong>Estadios</strong></p>' in contenido
		assert "abrirVentana('ventana-emergente-estadios-nuevos')" in contenido
		assert '<p><strong>Estadios Nuevos</strong></p>' in contenido
		assert "abrirVentana('ventana-emergente-equipos')" in contenido
		assert '<p><strong>Equipo Mas Visto</strong></p>' in contenido
		assert "abrirVentana('ventana-emergente-paises')" in contenido
		assert '<p><strong>Paises</strong></p>' in contenido
		assert '<div id="ventana-emergente-partidos" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-partidos-asistidos">' in contenido
		assert '<div id="ventana-emergente-estadios" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-estadios-asistidos">' in contenido
		assert '<div id="ventana-emergente-estadios-nuevos" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-estadios-asistidos">' in contenido
		assert '<div id="ventana-emergente-equipos" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-equipos-vistos">' in contenido
		assert '<div id="ventana-emergente-paises" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-paises-asistidos">' in contenido
		assert '<div class="contenedor-lateral contenedor-lateral-izq">' in contenido
		assert '<div class="circulo-partido-mas-goles">' in contenido
		assert '<div class="tarjeta-partido-mas-goles"' in contenido
		assert '<div class="circulo-estadisticas-partidos-asistidos">' in contenido
		assert '<div class="tarjeta-dato-grafica">' in contenido
		assert '<div id="ventana-emergente-mes" class="ventana-emergente">' in contenido
		assert '<p class="titulo-ventana" id="titulo-ventana-mes"><strong>Partidos del mes</strong></p>' in contenido
		assert "iframe" in contenido
		assert "/wrapped/mapa/mapa_small_wrapped_2019_user_" in contenido
		assert '<img class="no-mapa"' not in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "/wrapped/mapa/mapa_detalle_wrapped_2019_user_" in contenido
		assert "/wrapped/mapa/mapa_detalle_paises_wrapped_2019_user_" in contenido

def test_pagina_wrapped_subida_ano_anterior(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="estado" src="/static/imagenes/iconos/subida.png" alt="Estado Icon">' in contenido
		assert '<img class="estado" src="/static/imagenes/iconos/bajada.png" alt="Estado Icon">' not in contenido
		assert '<img class="estado" src="/static/imagenes/iconos/igual.png" alt="Estado Icon">' not in contenido

def test_pagina_wrapped_igual_ano_anterior(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
										VALUES('20180622', 'rival', 'atletico-madrid', '2018-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO estadios (Estadio_Id) VALUES('estadio-rival')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO partido_estadio VALUES('20180622', 'estadio-rival')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for partido_id in ["20180622", "20190622"]:

			data={"partido_anadir":partido_id, "comentario":"Comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="estado" src="/static/imagenes/iconos/subida.png" alt="Estado Icon">' not in contenido
		assert '<img class="estado" src="/static/imagenes/iconos/bajada.png" alt="Estado Icon">' not in contenido
		assert '<img class="estado" src="/static/imagenes/iconos/igual.png" alt="Estado Icon">' in contenido

def test_pagina_wrapped_bajada_ano_anterior(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
										VALUES('20180622', 'rival', 'atletico-madrid', '2018-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
											('20180623', 'rival', 'atletico-madrid', '2018-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO estadios (Estadio_Id, Pais, Codigo_Pais)
										VALUES('estadio-rival', 'Pais1', 'p1'), ('estadio-rival-2', 'Pais2', 'p2')""")

	conexion_entorno_usuario.c.execute("""INSERT INTO partido_estadio
										VALUES('20180622', 'estadio-rival'), ('20180623', 'estadio-rival-2')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for partido_id in ["20180622", "20180623", "20190622"]:

			data={"partido_anadir":partido_id, "comentario":"Comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="estado" src="/static/imagenes/iconos/subida.png" alt="Estado Icon">' not in contenido
		assert '<img class="estado" src="/static/imagenes/iconos/bajada.png" alt="Estado Icon">' in contenido
		assert '<img class="estado" src="/static/imagenes/iconos/igual.png" alt="Estado Icon">' not in contenido

def test_pagina_wrapped_error_mapa(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE estadios SET Latitud=NULL, Longitud=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" not in contenido
		assert "/estadios/mis_estadios/mapa/mapa_small_wrapped_2019_user_nacho98.html" not in contenido
		assert '<img class="no-mapa"' in contenido

def test_pagina_wrapped_mapa_small(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert "/wrapped/mapa/mapa_small_wrapped_2019_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_small_wrapped_2019_user_nacho98.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var circle_" in contenido
			assert "L.circle" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "Metropolitano" not in contenido
			assert "23.png" not in contenido
			assert "es.png" not in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" not in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",),("golden",),("amanda",),("amanda99",),("nacho98",)]
)
def test_pagina_wrapped_mapa_small_usuarios(cliente, conexion_entorno, password_hash, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert f"/wrapped/mapa/mapa_small_wrapped_2019_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_small_wrapped_2019_user_{usuario}.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var circle_" in contenido
			assert "L.circle" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "Metropolitano" not in contenido
			assert "23.png" not in contenido
			assert "es.png" not in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" not in contenido

def test_pagina_wrapped_mapa_small_otro_usuario(cliente, conexion_entorno_usuario, password_hash):

	conexion_entorno_usuario.insertarUsuario("otro", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/wrapped/2019")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_small_wrapped_2019_user_otro.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var circle_" in contenido
			assert "L.circle" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "Metropolitano" not in contenido
			assert "23.png" not in contenido
			assert "es.png" not in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" not in contenido

	with cliente as cliente_abierto:

		conexion_entorno_usuario.c.execute("""INSERT INTO estadios (Estadio_Id, Nombre, Capacidad, Latitud, Longitud, Codigo_Estadio, Codigo_Pais) VALUES('estadio', 'Nombre Estadio', 100000, 1.0, -1.0, 22619, 'pais')""")

		conexion_entorno_usuario.c.execute("""INSERT INTO partidos VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno_usuario.c.execute("""INSERT INTO partido_estadio VALUES('20190623', 'estadio')""")

		conexion_entorno_usuario.confirmar()

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190623", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/wrapped/2019")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_small_wrapped_2019_user_nacho98.html")

		assert os.path.exists(ruta_mapa2)

		with open(ruta_mapa2, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var circle_" in contenido
			assert "L.circle" in contenido
			assert "[1.0, -1.0]" in contenido
			assert "Nombre Estadio" not in contenido
			assert "22619.png" not in contenido
			assert "pais.png" not in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" not in contenido

def test_pagina_wrapped_mapa_detalle(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert "/wrapped/mapa/mapa_detalle_wrapped_2019_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_wrapped_2019_user_nacho98.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "Metropolitano" in contenido
			assert "23.png" in contenido
			assert "es.png" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",),("golden",),("amanda",),("amanda99",),("nacho98",)]
)
def test_pagina_wrapped_mapa_detalle_usuarios(cliente, conexion_entorno, password_hash, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert f"/wrapped/mapa/mapa_detalle_wrapped_2019_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_detalle_wrapped_2019_user_{usuario}.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "Metropolitano" in contenido
			assert "23.png" in contenido
			assert "es.png" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

def test_pagina_wrapped_mapa_detalle_otro_usuario(cliente, conexion_entorno_usuario, password_hash):

	conexion_entorno_usuario.insertarUsuario("otro", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/wrapped/2019")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_wrapped_2019_user_otro.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "Metropolitano" in contenido
			assert "23.png" in contenido
			assert "es.png" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

	with cliente as cliente_abierto:

		conexion_entorno_usuario.c.execute("""INSERT INTO estadios (Estadio_Id, Nombre, Capacidad, Latitud, Longitud, Codigo_Estadio, Codigo_Pais) VALUES('estadio', 'Nombre Estadio', 100000, 1.0, -1.0, 22619, 'pais')""")

		conexion_entorno_usuario.c.execute("""INSERT INTO partidos VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno_usuario.c.execute("""INSERT INTO partido_estadio VALUES('20190623', 'estadio')""")

		conexion_entorno_usuario.confirmar()

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190623", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/wrapped/2019")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_detalle_wrapped_2019_user_nacho98.html")

		assert os.path.exists(ruta_mapa2)

		with open(ruta_mapa2, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[1.0, -1.0]" in contenido
			assert "Nombre Estadio" in contenido
			assert "22619.png" in contenido
			assert "pais.png" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

def test_pagina_wrapped_mapa_detalle_paises(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "iframe" in contenido
		assert "/wrapped/mapa/mapa_detalle_paises_wrapped_2019_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_paises_wrapped_2019_user_nacho98.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var geo_json_" in contenido
			assert "function geo_json_" in contenido
			assert '"bbox": [NaN, NaN, NaN, NaN]' not in contenido
			assert '"features": []' not in contenido
			assert '"type": "FeatureCollection"' in contenido
			assert '{"name": "Spain"}' in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",),("golden",),("amanda",),("amanda99",),("nacho98",)]
)
def test_pagina_wrapped_mapa_detalle_paises_usuarios(cliente, conexion_entorno, password_hash, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "iframe" in contenido
		assert f"/wrapped/mapa/mapa_detalle_paises_wrapped_2019_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_detalle_paises_wrapped_2019_user_{usuario}.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var geo_json_" in contenido
			assert "function geo_json_" in contenido
			assert '"bbox": [NaN, NaN, NaN, NaN]' not in contenido
			assert '"features": []' not in contenido
			assert '"type": "FeatureCollection"' in contenido
			assert '{"name": "Spain"}' in contenido

def test_pagina_wrapped_mapa_detalle_paises_otro_usuario(cliente, conexion_entorno_usuario, password_hash):

	conexion_entorno_usuario.insertarUsuario("otro", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/wrapped/2019")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_paises_wrapped_2019_user_otro.html")

		assert os.path.exists(ruta_mapa)

		with open(ruta_mapa, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var geo_json_" in contenido
			assert "function geo_json_" in contenido
			assert '"bbox": [NaN, NaN, NaN, NaN]' not in contenido
			assert '"features": []' not in contenido
			assert '"type": "FeatureCollection"' in contenido
			assert '{"name": "Spain"}' in contenido

	with cliente as cliente_abierto:

		conexion_entorno_usuario.c.execute("""INSERT INTO estadios (Estadio_Id, Nombre, Capacidad, Latitud, Longitud, Codigo_Estadio, Codigo_Pais) VALUES('estadio', 'Nombre Estadio', 100000, 41.9028, 12.4964, 22619, 'pais')""")

		conexion_entorno_usuario.c.execute("""INSERT INTO partidos VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno_usuario.c.execute("""INSERT INTO partido_estadio VALUES('20190623', 'estadio')""")

		conexion_entorno_usuario.confirmar()

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190623", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/wrapped/2019")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_detalle_paises_wrapped_2019_user_nacho98.html")

		assert os.path.exists(ruta_mapa2)

		with open(ruta_mapa2, "r") as mapa:

			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var geo_json_" in contenido
			assert "function geo_json_" in contenido
			assert '"bbox": [NaN, NaN, NaN, NaN]' not in contenido
			assert '"features": []' not in contenido
			assert '"type": "FeatureCollection"' in contenido
			assert '{"name": "Italy"}' in contenido

def test_pagina_mapa_wrapped_sin_login(cliente):

	respuesta=cliente.get("/wrapped/mapa/nombre_mapa", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mapa_wrapped_mapa_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		with pytest.raises(FileNotFoundError):

			cliente_abierto.get("/wrapped/mapa/nombre_mapa.html")

def test_pagina_mapa_wrapped_mapa_small_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/wrapped/2019")

		respuesta=cliente_abierto.get("/wrapped/mapa/mapa_small_wrapped_2019_user_nacho98.html")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var circle_" in contenido
		assert "L.circle" in contenido
		assert "[40.436, -3.599]" in contenido
		assert "Metropolitano" not in contenido
		assert "23.png" not in contenido
		assert "es.png" not in contenido
		assert "/static/imagenes/iconos/estadio_mapa.png" not in contenido

def test_pagina_mapa_wrapped_mapa_detalle_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/wrapped/2019")

		respuesta=cliente_abierto.get("/wrapped/mapa/mapa_detalle_wrapped_2019_user_nacho98.html")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "[40.436, -3.599]" in contenido
		assert "Metropolitano" in contenido
		assert "23.png" in contenido
		assert "es.png" in contenido
		assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

def test_pagina_mapa_wrapped_mapa_detalle_paises_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/wrapped/2019")

		respuesta=cliente_abierto.get("/wrapped/mapa/mapa_detalle_paises_wrapped_2019_user_nacho98.html")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var geo_json_" in contenido
		assert "function geo_json_" in contenido
		assert '"bbox": [NaN, NaN, NaN, NaN]' not in contenido
		assert '"features": []' not in contenido
		assert '"type": "FeatureCollection"' in contenido
		assert '{"name": "Spain"}' in contenido