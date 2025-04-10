import pytest
import os

def test_pagina_mis_estadios_sin_login(cliente):

	respuesta=cliente.get("/estadios/mis_estadios", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mis_estadios_estadios_no_existen(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM estadios")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_partidos_asistidos_no_existen(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_estadios_asistidos_no_existen(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM estadios")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos">' in contenido
		assert '<div class="tarjetas-estadios-asistidos">' in contenido
		assert '<div class="tarjeta-estadio-asistido"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert '<div class="tarjeta-mis-estadios-recientes">' in contenido
		assert '<div class="tarjetas-mis-estadios-recientes">' in contenido
		assert '<div class="tarjeta-paises-mis-estadios">' in contenido
		assert '<p class="titulo-paises-mis-estadios">' in contenido
		assert '<div class="tarjetas-paises-mis-estadios">' in contenido
		assert '<p class="titulo-circulo-estadios-asistidos">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos"><strong>1</strong></p>' in contenido
		assert "iframe" in contenido
		assert "/estadios/mis_estadios/mapa/mapa_small_mis_estadios_user_" in contenido
		assert '<img class="no-mapa"' not in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "/estadios/mis_estadios/mapa/mapa_detalle_mis_estadios_user_" in contenido
		assert "/estadios/mis_estadios/mapa/mapa_detalle_paises_mis_estadios_user_" in contenido
		assert '<div class="tarjeta-mis-estadios-competiciones">' in contenido
		assert '<p class="titulo-mis-estadios-competiciones">' in contenido
		assert '<div class="tarjetas-mis-estadios-competiciones">' in contenido

@pytest.mark.parametrize(["veces"],
	[(1,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_estadios_varias_veces(cliente, conexion_entorno_usuario, veces):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero}', 'metropolitano')""")

			conexion_entorno_usuario.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos">' in contenido
		assert '<div class="tarjetas-estadios-asistidos">' in contenido
		assert '<div class="tarjeta-estadio-asistido"' in contenido
		assert f"<h4>{veces} veces</h4>" in contenido
		assert '<div class="tarjeta-mis-estadios-recientes">' in contenido
		assert '<div class="tarjetas-mis-estadios-recientes">' in contenido
		assert '<div class="tarjeta-paises-mis-estadios">' in contenido
		assert '<p class="titulo-paises-mis-estadios">' in contenido
		assert '<div class="tarjetas-paises-mis-estadios">' in contenido
		assert "iframe" in contenido
		assert "/estadios/mis_estadios/mapa/mapa_small_mis_estadios_user_" in contenido
		assert '<img class="no-mapa"' not in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "/estadios/mis_estadios/mapa/mapa_detalle_mis_estadios_user_" in contenido
		assert "/estadios/mis_estadios/mapa/mapa_detalle_paises_mis_estadios_user_" in contenido
		assert '<div class="tarjeta-mis-estadios-competiciones">' in contenido
		assert '<p class="titulo-mis-estadios-competiciones">' in contenido
		assert '<div class="tarjetas-mis-estadios-competiciones">' in contenido

def test_pagina_mis_estadios_codigo_pais_nulo(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("UPDATE estadios SET Codigo_Pais=NULL")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-paises-mis-estadios">' in contenido
		assert '<p class="titulo-paises-mis-estadios">' in contenido
		assert '<div class="tarjetas-paises-mis-estadios">' not in contenido

def test_pagina_mis_estadios_estadio_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos"><strong>1</strong></p>' in contenido

@pytest.mark.parametrize(["veces"],
	[(1,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_estadios_estadio_asistido_varias_veces(cliente, conexion_entorno_usuario, veces):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

			conexion_entorno_usuario.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero}', 'metropolitano')""")

			conexion_entorno_usuario.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert f"<h4>{veces} veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos"><strong>1</strong></p>' in contenido

def test_pagina_mis_estadios_error_mapa(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""UPDATE estadios SET Latitud=NULL, Longitud=NULL""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" not in contenido
		assert "/estadios/mis_estadios/mapa/mapa_small_mis_estadios_user_nacho98.html" not in contenido
		assert '<img class="no-mapa"' in contenido

def test_pagina_mis_estadios_mapa_small(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert "/estadios/mis_estadios/mapa/mapa_small_mis_estadios_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_small_mis_estadios_user_nacho98.html")

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
def test_pagina_mis_estadios_mapa_small_usuarios(cliente, conexion_entorno, password_hash, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert f"/estadios/mis_estadios/mapa/mapa_small_mis_estadios_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_small_mis_estadios_user_{usuario}.html")

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

def test_pagina_mis_estadios_mapa_small_otro_usuario(cliente, conexion_entorno_usuario, password_hash):

	conexion_entorno_usuario.insertarUsuario("otro", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_small_mis_estadios_user_otro.html")

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

		cliente_abierto.get("/estadios/mis_estadios")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_small_mis_estadios_user_nacho98.html")

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

def test_pagina_mis_estadios_mapa_detalle(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert "/estadios/mis_estadios/mapa/mapa_detalle_mis_estadios_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_mis_estadios_user_nacho98.html")

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
def test_pagina_mis_estadios_mapa_detalle_usuarios(cliente, conexion_entorno, password_hash, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert f"/estadios/mis_estadios/mapa/mapa_detalle_mis_estadios_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_detalle_mis_estadios_user_{usuario}.html")

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

def test_pagina_mis_estadios_mapa_detalle_otro_usuario(cliente, conexion_entorno_usuario, password_hash):

	conexion_entorno_usuario.insertarUsuario("otro", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_mis_estadios_user_otro.html")

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

		cliente_abierto.get("/estadios/mis_estadios")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_detalle_mis_estadios_user_nacho98.html")

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

def test_pagina_mis_estadios_mapa_detalle_paises(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "iframe" in contenido
		assert "/estadios/mis_estadios/mapa/mapa_detalle_paises_mis_estadios_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_paises_mis_estadios_user_nacho98.html")

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
def test_pagina_mis_estadios_mapa_detalle_paises_usuarios(cliente, conexion_entorno, password_hash, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "iframe" in contenido
		assert f"/estadios/mis_estadios/mapa/mapa_detalle_paises_mis_estadios_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_detalle_paises_mis_estadios_user_{usuario}.html")

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

def test_pagina_mis_estadios_mapa_detalle_paises_otro_usuario(cliente, conexion_entorno_usuario, password_hash):

	conexion_entorno_usuario.insertarUsuario("otro", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "estadios")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_paises_mis_estadios_user_otro.html")

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

		cliente_abierto.get("/estadios/mis_estadios")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_detalle_paises_mis_estadios_user_nacho98.html")

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

def test_pagina_mapa_mis_estadios_sin_login(cliente):

	respuesta=cliente.get("/estadios/mis_estadios/mapa/nombre_mapa", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mapa_mis_estadios_mapa_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		with pytest.raises(FileNotFoundError):

			cliente_abierto.get("/estadios/mis_estadios/mapa/nombre_mapa.html")

def test_pagina_mapa_mis_estadios_mapa_small_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios")

		respuesta=cliente_abierto.get("/estadios/mis_estadios/mapa/mapa_small_mis_estadios_user_nacho98.html")

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

def test_pagina_mapa_mis_estadios_mapa_detalle_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios")

		respuesta=cliente_abierto.get("/estadios/mis_estadios/mapa/mapa_detalle_mis_estadios_user_nacho98.html")

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

def test_pagina_mapa_mis_estadios_mapa_detalle_paises_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios")

		respuesta=cliente_abierto.get("/estadios/mis_estadios/mapa/mapa_detalle_paises_mis_estadios_user_nacho98.html")

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

def test_pagina_mis_estadios_codigo_competicion_nulo(cliente, conexion_entorno_usuario):
 
	conexion_entorno_usuario.c.execute("UPDATE equipos SET Competicion=NULL")
 
	conexion_entorno_usuario.confirmar()
 
	with cliente as cliente_abierto:
 
		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)
 
		data={"partido_anadir":"20190622", "comentario":"comentario"}
 
		cliente_abierto.post("/insertar_partido_asistido", data=data)
 
		respuesta=cliente_abierto.get("/estadios/mis_estadios")
 
		contenido=respuesta.data.decode()
 
		respuesta.status_code==200
		assert '<div class="tarjeta-mis-estadios-competiciones">' in contenido
		assert '<p class="titulo-mis-estadios-competiciones">' in contenido
		assert '<div class="tarjetas-mis-estadios-competiciones">' not in contenido