import pytest
import os

def test_pagina_mis_estadios_pais_sin_login(cliente):

	respuesta=cliente.get("/estadios/mis_estadios/es", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mis_estadios_pais_estadios_no_existen(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM estadios")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/pais")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_pais_partidos_asistidos_no_existen(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/pais")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_pais_estadios_asistidos_no_existen(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM estadios")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_pais_codigos_pais_estadio_equipo_nulos(cliente, conexion_entorno):

	conexion_entorno.c.execute("UPDATE estadios SET Codigo_Pais=NULL")

	conexion_entorno.c.execute("UPDATE equipos SET Codigo_Pais=NULL")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

@pytest.mark.parametrize(["pais"],
	[("se",),("ese",),("p",),("nl",),("pt",)]
)
def test_pagina_mis_estadios_pais_codigo_pais_no_existe(cliente, conexion_entorno, pais):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get(f"/estadios/mis_estadios/{pais}")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_mis_estadios_pais(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-pais"><strong>1</strong></p>' in contenido
		assert '<div class="desplegable-contenedor">' not in contenido
		assert "iframe" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_small_mis_estadios_pais_es_user_" in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_mis_estadios_pais_es_user_" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_paises_mis_estadios_pais_es_user_" in contenido

def test_pagina_mis_estadios_pais_codigo_pais_estadio_nulo(cliente, conexion_entorno):

	conexion_entorno.c.execute("UPDATE estadios SET Codigo_Pais=NULL")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-pais"><strong>1</strong></p>' in contenido
		assert '<div class="desplegable-contenedor">' not in contenido
		assert "iframe" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_small_mis_estadios_pais_es_user_" in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_mis_estadios_pais_es_user_" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_paises_mis_estadios_pais_es_user_" in contenido

def test_pagina_mis_estadios_pais_codigo_pais_equipo_nulo(cliente, conexion_entorno):

	conexion_entorno.c.execute("UPDATE equipos SET Codigo_Pais=NULL")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-pais"><strong>1</strong></p>' in contenido
		assert '<div class="desplegable-contenedor">' not in contenido
		assert "iframe" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_small_mis_estadios_pais_es_user_" in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_mis_estadios_pais_es_user_" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_paises_mis_estadios_pais_es_user_" in contenido

@pytest.mark.parametrize(["veces"],
	[(1,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_estadios_pais_varias_veces(cliente, conexion_entorno, veces):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

			conexion_entorno.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero}', 'metropolitano')""")

			conexion_entorno.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert f"<h4>{veces} veces</h4>" in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert '<p class="valor-circulo-estadios-asistidos-pais"><strong>1</strong></p>' in contenido
		assert '<div class="desplegable-contenedor">' not in contenido
		assert "iframe" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_small_mis_estadios_pais_es_user_" in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_mis_estadios_pais_es_user_" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_paises_mis_estadios_pais_es_user_" in contenido

@pytest.mark.parametrize(["veces"],
	[(2,),(5,),(7,),(13,),(22,),(6,)]
)
def test_pagina_mis_estadios_pais_varios(cliente, conexion_entorno, veces):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(veces):

			conexion_entorno.c.execute(f"""INSERT INTO estadios (Estadio_Id, Capacidad, Pais, Codigo_Pais, Latitud, Longitud) VALUES('estadio{numero}', 100000, 'España', 'es', 1.0, -1.0)""")

			conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

			conexion_entorno.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero}', 'estadio{numero}')""")

			conexion_entorno.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert '<div class="tarjetas-estadios-asistidos-pais">' in contenido
		assert '<div class="tarjeta-estadio-asistido-pais"' in contenido
		assert "<h4>1 veces</h4>" in contenido
		assert f"<h4>{veces} veces</h4>" not in contenido
		assert '<p class="titulo-circulo-estadios-asistidos-pais">' in contenido
		assert "Estadios Visitados" in contenido
		assert f'<p class="valor-circulo-estadios-asistidos-pais"><strong>{veces}</strong></p>' in contenido
		assert '<div class="desplegable-contenedor">' not in contenido
		assert "iframe" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_small_mis_estadios_pais_es_user_" in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert '<div class="botones-mapa-detalle">' in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_mis_estadios_pais_es_user_" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_paises_mis_estadios_pais_es_user_" in contenido

def test_pagina_mis_estadios_pais_sin_nombre_pais(cliente, conexion_entorno):

	conexion_entorno.c.execute("UPDATE estadios SET Pais=NULL")

	conexion_entorno.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert "<strong>Mis Estadios de None</strong>" in contenido
		assert '<span class="boton-estadios-mapa-text">Estadios de None</span>' in contenido
		assert '<span class="boton-paises-mapa-text">None</span>' in contenido

def test_pagina_mis_estadios_pais_con_nombre_pais(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-estadios-asistidos-pais"' in contenido
		assert '<p class="titulo-pagina-estadios-asistidos-pais">' in contenido
		assert "es.png" in contenido
		assert "<strong>Mis Estadios de España</strong>" in contenido
		assert '<span class="boton-estadios-mapa-text">Estadios de España</span>' in contenido
		assert '<span class="boton-paises-mapa-text">España</span>' in contenido

def test_pagina_mis_estadios_pais_sin_paises_no_seleccionados(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="desplegable-contenedor">' not in contenido
		assert '<button class="boton-desplegable"' not in contenido
		assert '<div id="menuDesplegable" class="menu-desplegable">' not in contenido

@pytest.mark.parametrize(["pais"],
	[("es0",),("es1",),("es2",),("es3",),("es4",)]
)
def test_pagina_mis_estadios_pais_con_paises_no_seleccionados(cliente, conexion_entorno, pais):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		for numero in range(5):

			conexion_entorno.c.execute(f"""INSERT INTO estadios (Estadio_Id, Capacidad, Pais, Codigo_Pais, Latitud, Longitud) VALUES('estadio{numero}', 100000, 'España', 'es{numero}', 1.0, -1.0)""")

			conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

			conexion_entorno.c.execute(f"""INSERT INTO partido_estadio VALUES('20190622{numero}', 'estadio{numero}')""")

			conexion_entorno.confirmar()

			data={"partido_anadir":f"20190622{numero}", "comentario":"comentario"}

			cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get(f"/estadios/mis_estadios/{pais}")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="desplegable-contenedor">' in contenido
		assert '<button class="boton-desplegable"' in contenido
		assert '<div id="menuDesplegable" class="menu-desplegable">' in contenido

def test_pagina_mis_estadios_pais_mapa_small(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_small_mis_estadios_pais_es_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_small_mis_estadios_pais_es_user_nacho98.html")

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
def test_pagina_mis_estadios_pais_mapa_small_usuarios(cliente, conexion_entorno, usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":usuario, "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert f"/estadios/mis_estadios_pais/mapa/mapa_small_mis_estadios_pais_es_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_small_mis_estadios_pais_es_user_{usuario}.html")

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

def test_pagina_mis_estadios_pais_mapa_small_otro_usuario(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"otro", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios/es")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_small_mis_estadios_pais_es_user_otro.html")

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

		conexion_entorno.c.execute("""INSERT INTO estadios (Estadio_Id, Nombre, Capacidad, Latitud, Longitud, Codigo_Estadio, Codigo_Pais) VALUES('estadio', 'Nombre Estadio', 100000, 1.0, -1.0, 22619, 'pais')""")

		conexion_entorno.c.execute("""INSERT INTO partidos VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.c.execute("""INSERT INTO partido_estadio VALUES('20190623', 'estadio')""")

		conexion_entorno.confirmar()

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190623", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios/pais")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_small_mis_estadios_pais_pais_user_nacho98.html")

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

def test_pagina_mis_estadios_pais_mapa_detalle(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_mis_estadios_pais_es_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_mis_estadios_pais_es_user_nacho98.html")

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
def test_pagina_mis_estadios_pais_mapa_detalle_usuarios(cliente, conexion_entorno, usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":usuario, "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert f"/estadios/mis_estadios_pais/mapa/mapa_detalle_mis_estadios_pais_es_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_detalle_mis_estadios_pais_es_user_{usuario}.html")

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

def test_pagina_mis_estadios_pais_mapa_detalle_otro_usuario(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"otro", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios/es")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_mis_estadios_pais_es_user_otro.html")

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

		conexion_entorno.c.execute("""INSERT INTO estadios (Estadio_Id, Nombre, Capacidad, Latitud, Longitud, Codigo_Estadio, Codigo_Pais) VALUES('estadio', 'Nombre Estadio', 100000, 1.0, -1.0, 22619, 'pais')""")

		conexion_entorno.c.execute("""INSERT INTO partidos VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.c.execute("""INSERT INTO partido_estadio VALUES('20190623', 'estadio')""")

		conexion_entorno.confirmar()

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190623", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios/pais")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_detalle_mis_estadios_pais_pais_user_nacho98.html")

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

def test_pagina_mis_estadios_pais_mapa_detalle_paises(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert "/estadios/mis_estadios_pais/mapa/mapa_detalle_paises_mis_estadios_pais_es_user_nacho98.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_paises_mis_estadios_pais_es_user_nacho98.html")

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
def test_pagina_mis_estadios_pais_mapa_detalle_paises_usuarios(cliente, conexion_entorno, usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":usuario, "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/estadios/mis_estadios/es")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "iframe" in contenido
		assert f"/estadios/mis_estadios_pais/mapa/mapa_detalle_paises_mis_estadios_pais_es_user_{usuario}.html" in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, f"mapa_detalle_paises_mis_estadios_pais_es_user_{usuario}.html")

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

def test_pagina_mis_estadios_pais_mapa_detalle_paises_otro_usuario(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"otro", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "otro", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios/es")

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas")

		ruta_mapa=os.path.join(ruta_carpeta_mapas, "mapa_detalle_paises_mis_estadios_pais_es_user_otro.html")

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

		conexion_entorno.c.execute("""INSERT INTO estadios (Estadio_Id, Nombre, Capacidad, Latitud, Longitud, Codigo_Estadio, Codigo_Pais) VALUES('estadio', 'Nombre Estadio', 100000, 41.9028, 12.4964, 22619, 'pais')""")

		conexion_entorno.c.execute("""INSERT INTO partidos VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.c.execute("""INSERT INTO partido_estadio VALUES('20190623', 'estadio')""")

		conexion_entorno.confirmar()

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190623", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios/pais")

		ruta_mapa2=os.path.join(ruta_carpeta_mapas, "mapa_detalle_paises_mis_estadios_pais_pais_user_nacho98.html")

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

def test_pagina_mapa_mis_estadios_pais_sin_login(cliente):

	respuesta=cliente.get("/estadios/mis_estadios_pais/mapa/nombre_mapa", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mapa_mis_estadios_pais_mapa_no_existe(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		with pytest.raises(FileNotFoundError):

			cliente_abierto.get("/estadios/mis_estadios_pais/mapa/nombre_mapa.html")

def test_pagina_mapa_mis_estadios_pais_mapa_small_existe(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios/es")

		respuesta=cliente_abierto.get("/estadios/mis_estadios_pais/mapa/mapa_small_mis_estadios_pais_es_user_nacho98.html")

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

def test_pagina_mapa_mis_estadios_pais_mapa_detalle_existe(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios/es")

		respuesta=cliente_abierto.get("/estadios/mis_estadios_pais/mapa/mapa_detalle_mis_estadios_pais_es_user_nacho98.html")

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

def test_pagina_mapa_mis_estadios_pais_mapa_detalle_paises_existe(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/estadios/mis_estadios/es")

		respuesta=cliente_abierto.get("/estadios/mis_estadios_pais/mapa/mapa_detalle_paises_mis_estadios_pais_es_user_nacho98.html")

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