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
		assert "abrirVentana('ventana-emergente-trayectos')" in contenido
		assert '<p><strong>Distancia Recorrida</strong></p>' in contenido
		assert '<h4>0 kms</h4>' in contenido
		assert '<div id="ventana-emergente-partidos" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-partidos-asistidos">' in contenido
		assert '<div id="ventana-emergente-estadios" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-estadios-asistidos">' in contenido
		assert '<div id="ventana-emergente-estadios-nuevos" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-estadios-asistidos">' in contenido
		assert '<div id="ventana-emergente-equipos" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-equipos-vistos">' in contenido
		assert '<div id="ventana-emergente-paises" class="ventana-emergente">' in contenido
		assert '<div id="ventana-emergente-trayectos" class="ventana-emergente">' in contenido
		assert '<div class="tarjeta-trayecto-realizado"' not in contenido
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

@pytest.mark.parametrize(["ciudad_ida", "transporte_ida", "ciudad_vuelta", "transporte_vuelta"],
	[
		("A Coruña", "Avion", "A Coruña", "Autobus"),
		("Madrid", "Pie", "Barcelona", "Tren"),
		("Leganés", "Cercanias", "Elche", "Coche"),
		("Valencia", "Autobus", "Madrid", "Pie"),
		("Madrid", "Metro", "Sevilla", "Tren")
	]
)
def test_pagina_wrapped_trayecto_simple(cliente, conexion_entorno_usuario, ciudad_ida, transporte_ida, ciudad_vuelta, transporte_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "ciudad-ida":ciudad_ida, "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-21", "transporte-ida":transporte_ida, "ciudad-vuelta":ciudad_vuelta, "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":transporte_vuelta, "teletrabajo":True}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "abrirVentana('ventana-emergente-trayectos')" in contenido
		assert '<p><strong>Distancia Recorrida</strong></p>' in contenido
		assert '<h4>0 kms</h4>' not in contenido
		assert '<div class="tarjeta-trayecto-realizado"' in contenido
		assert '<div class="contenedor-datos-trayecto-realizado">' in contenido
		assert '<p class="distancia-trayecto-realizado"><strong>Distancia Total:' in contenido
		assert '<p class="distancia-trayecto-realizado"><strong>Distancia Ida:' in contenido
		assert '<p class="distancia-trayecto-realizado"><strong>Distancia Vuelta:' in contenido
		assert '<p class="escala-trayecto-realizado"><strong>Escalas: 0</strong></p>' in contenido
		assert f'<p class="texto-origen-destino"><strong>{ciudad_ida}</strong></p>' in contenido
		assert f'<img src="/static/imagenes/iconos/{transporte_ida.lower()}.png" alt="Transporte Icon" class="icono-transporte">' in contenido
		assert '<p class="texto-origen-destino"><strong>Metropolitano</strong></p>' in contenido
		assert f'<img src="/static/imagenes/iconos/{transporte_vuelta.lower()}.png" alt="Transporte Icon" class="icono-transporte">' in contenido
		assert f'<p class="texto-origen-destino"><strong>{ciudad_vuelta}</strong></p>' in contenido

@pytest.mark.parametrize(["ciudad_ida", "transporte_ida", "ciudad_vuelta", "transporte_vuelta", "transportes_ida", "paises_ida", "ciudades_ida", "transportes_vuelta", "paises_vuelta", "ciudades_vuelta"],
	[
		("Barcelona", "Cercanias", "Barcelona", "Avion", ["Avion", "Cercanias"], ["España", "España"], ["Getafe", "Leganés"], ["Metro", "Avion"], ["España", "Francia"], ["Getafe", "Paris"]),
		("Valencia", "Metro", "Zaragoza", "Tren", ["Avion", "Tren"], ["España", "España"], ["Sevilla", "Leganés"], ["Coche", "Avion"], ["España", "Francia"], ["Getafe", "Paris"]),
		("Sevilla", "Tren", "Oviedo", "Autobus", ["Autobus", "Coche"], ["España", "España"], ["Granada", "Elche"], ["Coche", "Tren"], ["España", "España"], ["Gijon", "Valladolid"]),
		("Malaga", "Metro", "Barcelona", "Autobus", ["Autobus", "Coche", "Tren"], ["España", "España", "España"], ["Murcia", "Alicante", "Alcorcon"], ["Metro"], ["España"], ["Getafe"]),
		("Barcelona", "Cercanias", "Barcelona", "Autobus", ["Avion"], ["España"], ["Getafe"], ["Avion", "Avion", "Avion"], ["Reino Unido", "Alemania", "España"], ["Londres", "Berlin", "Palma"]),
		("Malaga", "Metro", "Barcelona", "Avion", ["Autobus", "Coche", "Tren", "Cercanias"], ["España", "España", "España", "España"], ["Murcia", "Alicante", "Alcorcon", "Getafe"], ["Avion", "Tren", "Avion", "Tren"], ["Alemania", "Alemania", "Francia", "Bélgica"], ["Munich", "Berlin", "Paris", "Bruselas"]),
		("Barcelona", "Avion", "Barcelona", "Tren", ["Avion", "Avion"], ["Reino Unido", "Francia"], ["Glasgow", "Marsella"], ["Avion", "Avion", "Avion", "Avion"], ["Reino Unido", "Alemania", "Francia", "España"], ["Londres", "Berlin", "Paris", "Alicante"]),
		("Barcelona", "Avion", "Valencia", "Tren", ["Avion", "Tren"], ["Italia", "Italia"], ["Milan", "Verona"], ["Coche"], ["España"], ["Alicante"])
	]
)
def test_pagina_wrapped_trayecto_complejo(cliente, conexion_entorno_usuario, ciudad_ida, transporte_ida, ciudad_vuelta, transporte_vuelta, transportes_ida, 
																	paises_ida, ciudades_ida, transportes_vuelta, paises_vuelta, ciudades_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario","ciudad-ida":ciudad_ida, "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":transporte_ida, "ciudad-vuelta":ciudad_vuelta, "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":transporte_vuelta, "teletrabajo":True, "transporte-parada-ida[]":transportes_ida, "pais-parada-ida[]":paises_ida, 
			"ciudad-parada-ida[]":ciudades_ida, "transporte-parada-vuelta[]":transportes_vuelta, "pais-parada-vuelta[]":paises_vuelta, "ciudad-parada-vuelta[]":ciudades_vuelta}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/wrapped/2019")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "abrirVentana('ventana-emergente-trayectos')" in contenido
		assert '<p><strong>Distancia Recorrida</strong></p>' in contenido
		assert '<h4>0 kms</h4>' not in contenido
		assert '<div class="tarjeta-trayecto-realizado"' in contenido
		assert '<div class="contenedor-datos-trayecto-realizado">' in contenido
		assert '<p class="distancia-trayecto-realizado"><strong>Distancia Total:' in contenido
		assert '<p class="distancia-trayecto-realizado"><strong>Distancia Ida:' in contenido
		assert '<p class="distancia-trayecto-realizado"><strong>Distancia Vuelta:' in contenido

		ciudades_ida_combinadas=[ciudad_ida]+ciudades_ida
		transporte_ida_combinadas=transportes_ida+[transporte_ida]

		assert f'<p class="escala-trayecto-realizado"><strong>Escalas: {len(ciudades_ida)}</strong></p>' in contenido

		for ciudad, transporte in zip(ciudades_ida_combinadas, transporte_ida_combinadas):

			assert f'<p class="texto-origen-destino"><strong>{ciudad}</strong></p>' in contenido
			assert f'<img src="/static/imagenes/iconos/{transporte.lower()}.png" alt="Transporte Icon" class="icono-transporte">' in contenido

		assert '<p class="texto-origen-destino"><strong>Metropolitano</strong></p>' in contenido

		ciudades_vuelta_combinadas=ciudades_vuelta+[ciudad_vuelta]
		transporte_vuelta_combinadas=transportes_vuelta+[transporte_vuelta]

		assert f'<p class="escala-trayecto-realizado"><strong>Escalas: {len(ciudades_vuelta)}</strong></p>' in contenido

		assert '<p class="texto-origen-destino"><strong>Metropolitano</strong></p>' in contenido

		for ciudad, transporte in zip(ciudades_vuelta_combinadas, transporte_vuelta_combinadas):

			assert f'<p class="texto-origen-destino"><strong>{ciudad}</strong></p>' in contenido
			assert f'<img src="/static/imagenes/iconos/{transporte.lower()}.png" alt="Transporte Icon" class="icono-transporte">' in contenido

		assert '<p class="texto-origen-destino"><strong>Metropolitano</strong></p>' in contenido