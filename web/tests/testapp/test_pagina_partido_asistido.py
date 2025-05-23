import pytest
import os

from src.utilidades.utils import vaciarCarpeta
from src.config import CONTENEDOR

def test_pagina_partido_asistido_sin_login(cliente):

	respuesta=cliente.get("/partido/1/asistido", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_partido_asistido_partido_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/1/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_asistido_equipo_no_pertenece(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('equipo-no-partido')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_asistido_partido_no_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==302
		assert respuesta.location=="/partidos"
		assert "Redirecting..." in contenido

def test_pagina_partido_asistido_con_comentario(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="info-partido-asistido-detalle">' in contenido
		assert '<div class="contenedor-comentario">' in contenido
		assert '<div class="comentario">' in contenido
		assert '<h2 class="no-comentario">' not in contenido
		assert '<div class="seccion-comentar-partido-asistido"' not in contenido
		assert "/no_favorito_asistido.png" in contenido
		assert "/favorito_asistido.png" not in contenido
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' not in contenido
		assert '<div class="seccion-on-tour-partido-asistido">' not in contenido
		assert '<div class="tarjeta-mapa-trayecto-ida-vuelta-total"' not in contenido
		assert '<div id="ventana-emergente-mapa" class="ventana-emergente-mapa">' not in contenido
		assert '<img class="no-mapa"' not in contenido

def test_pagina_partido_asistido_sin_comentario(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":""}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="info-partido-asistido-detalle">' in contenido
		assert '<div class="contenedor-comentario">' in contenido
		assert '<div class="comentario">' not in contenido
		assert '<h2 class="no-comentario">' in contenido
		assert '<div class="seccion-comentar-partido-asistido"' in contenido
		assert "/no_favorito_asistido.png" in contenido
		assert "/favorito_asistido.png" not in contenido
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' not in contenido
		assert '<div class="seccion-on-tour-partido-asistido">' not in contenido
		assert '<div class="tarjeta-mapa-trayecto-ida-vuelta-total"' not in contenido
		assert '<div id="ventana-emergente-mapa" class="ventana-emergente-mapa">' not in contenido
		assert '<img class="no-mapa"' not in contenido

def test_pagina_partido_asistido_sin_imagen(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="info-partido-asistido-detalle">' in contenido
		assert '<div class="contenedor-imagen">' in contenido
		assert '<div class="imagen">' not in contenido
		assert '<div class="contenedor-subir-imagen">' in contenido
		assert '<div class="botones-anadir-imagen-partido-asistido">' in contenido

def test_pagina_partido_asistido_con_imagen(cliente, conexion_entorno, datalake):

	datalake.crearCarpeta(CONTENEDOR, "usuarios/nacho98/imagenes")

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad": "Madrid", "equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/insertar_partido_asistido", data=data, buffered=True, content_type="multipart/form-data")

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="info-partido-asistido-detalle">' in contenido
		assert '<div class="contenedor-imagen">' in contenido
		assert '<div class="imagen">' in contenido
		assert '<div class="contenedor-subir-imagen">' not in contenido
		assert '<div class="botones-anadir-imagen-partido-asistido">' not in contenido
		assert "/nacho98_20190622.jpeg" in contenido

		datalake.eliminarCarpeta(CONTENEDOR, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		vaciarCarpeta(ruta_carpeta_imagenes)

def test_pagina_partido_asistido_sin_on_tour(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="contenedor-desplegable-on-tour">' not in contenido
		assert '<div class="seccion-on-tour-partido-asistido">' not in contenido

@pytest.mark.parametrize(["fecha_ida", "fecha_vuelta", "fecha_ida_on_tour", "fecha_vuelta_on_tour", "ciudad_ida", "transporte_ida", "ciudad_vuelta", "transporte_vuelta", "teletrabajo", "si_no"],
	[
		("2019-06-21", "2019-06-23", "21-06-2019", "23-06-2019", "A Coruna", "Avion", "A Coruna", "Autobus", True, "Si"),
		("2019-06-22", "2019-06-22", "22-06-2019", "22-06-2019", "Madrid", "Pie", "Barcelona", "Tren", False, "No"),
		("2019-04-13", "2019-06-23", "13-04-2019", "23-06-2019", "Leganés", "Cercanias", "Elche", "Coche", False, "No"),
		("2019-06-21", "2019-07-22", "21-06-2019", "22-07-2019", "Valencia", "Autobus", "Madrid", "Pie", True, "Si"),
		("2009-06-21", "2029-06-23", "21-06-2009", "23-06-2029", "Madrid", "Metro", "Sevilla", "Tren", True, "Si")
	]
)
def test_pagina_partido_asistido_con_on_tour_trayecto_simple(cliente, conexion_entorno_usuario, fecha_ida, fecha_vuelta, fecha_ida_on_tour, fecha_vuelta_on_tour, 
																ciudad_ida, transporte_ida, ciudad_vuelta, transporte_vuelta, teletrabajo, si_no):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "ciudad-ida":ciudad_ida, "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":fecha_ida, "transporte-ida":transporte_ida, "ciudad-vuelta":ciudad_vuelta, "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":fecha_vuelta, "transporte-vuelta":transporte_vuelta, "teletrabajo":teletrabajo}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="tarjeta-partido-asistido-detalle"' in contenido
		assert '<div class="contenedor-desplegable-on-tour">' in contenido
		assert '<div class="seccion-on-tour-partido-asistido"' in contenido
		assert '<div class="contenedor-datos-ida">' in contenido
		assert '<div class="contenedor-datos-vuelta">' in contenido
		assert '<p class="titulo-datos-ida-on-tour">' in contenido
		assert '<p class="titulo-datos-vuelta-on-tour">' in contenido
		assert '<div class="contenedor-fecha-on-tour">' in contenido
		assert f'<p class="fecha-on-tour-ida"><strong>Fecha: {fecha_ida_on_tour}</strong></p>' in contenido
		assert f'<p class="fecha-on-tour-vuelta"><strong>Fecha: {fecha_vuelta_on_tour}</strong></p>' in contenido
		assert '<div class="contenedor-origen-destino">' in contenido
		assert f'<p class="texto-origen-destino-ida"><strong>{ciudad_ida}</strong></p>' in contenido
		assert f'<img src="/static/imagenes/iconos/{transporte_ida.lower()}.png" alt="Transporte Icon Ida" class="icono-transporte-ida">' in contenido
		assert '<p class="texto-origen-destino-ida"><strong>Metropolitano</strong></p>' in contenido
		assert '<p class="texto-origen-destino-vuelta"><strong>Metropolitano</strong></p>' in contenido
		assert f'<img src="/static/imagenes/iconos/{transporte_vuelta.lower()}.png" alt="Transporte Icon Vuelta" class="icono-transporte-vuelta">' in contenido
		assert f'<p class="texto-origen-destino-vuelta"><strong>{ciudad_vuelta}</strong></p>' in contenido
		assert '<p class="teletrabajo-on-tour">' in contenido
		assert f"Teletrabajo {si_no}" in contenido

@pytest.mark.parametrize(["ciudad_ida", "transporte_ida", "ciudad_vuelta", "transporte_vuelta", "transportes_ida", "paises_ida", "ciudades_ida", "transportes_vuelta", "paises_vuelta", "ciudades_vuelta"],
	[
		("Barcelona", "Cercanias", "Barcelona", "Avion", ["Avion", "Cercanias"], ["España", "España"], ["Getafe", "Leganés"], ["Metro", "Avion"], ["España", "Francia"], ["Getafe", "Paris"]),
		("Valencia", "Metro", "Zaragoza", "Tren", ["Avion", "Tren"], ["España", "España"], ["Sevilla", "Leganés"], ["Coche", "Avion"], ["España", "Francia"], ["Getafe", "Paris"]),
		("Sevilla", "Tren", "Oviedo", "Autobus", ["Autobus", "Coche"], ["España", "España"], ["Granada", "Elche"], ["Coche", "Tren"], ["España", "España"], ["Gijon", "Valladolid"]),
		("Malaga", "Metro", "Barcelona", "Autobus", ["Autobus", "Coche", "Tren"], ["España", "España", "España"], ["Murcia", "Alicante", "Alcorcon"], ["Metro"], ["España"], ["Getafe"]),
		("Barcelona", "Cercanias", "Barcelona", "Autobus", ["Avion"], ["España"], ["Getafe"], ["Avion", "Avion", "Avion"], ["Reino Unido", "Alemania", "España"], ["London", "Berlin", "Palma"]),
		("Malaga", "Metro", "Barcelona", "Avion", ["Autobus", "Coche", "Tren", "Cercanias"], ["España", "España", "España", "España"], ["Murcia", "Alicante", "Alcorcon", "Getafe"], ["Avion", "Tren", "Avion", "Tren"], ["Alemania", "Alemania", "Francia", "Bélgica"], ["Munich", "Berlin", "Paris", "Brussels"]),
		("Barcelona", "Avion", "Barcelona", "Tren", ["Avion", "Avion"], ["Reino Unido", "Francia"], ["Glasgow", "Marseille"], ["Avion", "Avion", "Avion", "Avion"], ["Reino Unido", "Alemania", "Francia", "España"], ["London", "Berlin", "Paris", "Alicante"]),
		("Barcelona", "Avion", "Valencia", "Tren", ["Avion", "Tren"], ["Italia", "Italia"], ["Milan", "Verona"], ["Coche"], ["España"], ["Alicante"])
	]
)
def test_pagina_partido_asistido_con_on_tour_trayectos_complejos(cliente, conexion_entorno_usuario, ciudad_ida, transporte_ida, ciudad_vuelta, transporte_vuelta, transportes_ida, 
																	paises_ida, ciudades_ida, transportes_vuelta, paises_vuelta, ciudades_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario","ciudad-ida":ciudad_ida, "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":transporte_ida, "ciudad-vuelta":ciudad_vuelta, "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":transporte_vuelta, "teletrabajo":True, "transporte-parada-ida[]":transportes_ida, "pais-parada-ida[]":paises_ida, 
			"ciudad-parada-ida[]":ciudades_ida, "transporte-parada-vuelta[]":transportes_vuelta, "pais-parada-vuelta[]":paises_vuelta, "ciudad-parada-vuelta[]":ciudades_vuelta}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<div class="seccion-on-tour-partido-asistido"' in contenido
		assert '<div class="contenedor-datos-ida">' in contenido
		assert '<div class="contenedor-datos-vuelta">' in contenido
		assert '<div class="contenedor-fecha-on-tour">' in contenido
		assert '<div class="contenedor-origen-destino">' in contenido

		ciudades_ida_combinadas=[ciudad_ida]+ciudades_ida
		transporte_ida_combinadas=transportes_ida+[transporte_ida]

		for ciudad, transporte in zip(ciudades_ida_combinadas, transporte_ida_combinadas):

			assert f'<p class="texto-origen-destino-ida"><strong>{ciudad}</strong></p>' in contenido
			assert f'<img src="/static/imagenes/iconos/{transporte.lower()}.png" alt="Transporte Icon Ida" class="icono-transporte-ida">' in contenido

		assert '<p class="texto-origen-destino-ida"><strong>Metropolitano</strong></p>' in contenido

		ciudades_vuelta_combinadas=ciudades_vuelta+[ciudad_vuelta]
		transporte_vuelta_combinadas=transportes_vuelta+[transporte_vuelta]

		assert '<p class="texto-origen-destino-vuelta"><strong>Metropolitano</strong></p>' in contenido

		for ciudad, transporte in zip(ciudades_vuelta_combinadas, transporte_vuelta_combinadas):

			assert f'<p class="texto-origen-destino-vuelta"><strong>{ciudad}</strong></p>' in contenido
			assert f'<img src="/static/imagenes/iconos/{transporte.lower()}.png" alt="Transporte Icon Vuelta" class="icono-transporte-vuelta">' in contenido

		assert '<p class="texto-origen-destino-ida"><strong>Metropolitano</strong></p>' in contenido

def test_pagina_partido_asistido_no_partido_anterior_no_partido_siguiente(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":""})

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior-asistido"' not in contenido
		assert '<button class="button-partido-siguiente-asistido"' not in contenido

def test_pagina_partido_asistido_no_partido_anterior_si_partido_siguiente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":""})

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20245964", "comentario":""})

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior-asistido"' not in contenido
		assert '<button class="button-partido-siguiente-asistido"' in contenido

def test_pagina_partido_asistido_si_partido_anterior_no_partido_siguiente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
								VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":""})

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20245964", "comentario":""})

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior-asistido"' in contenido
		assert '<button class="button-partido-siguiente-asistido"' not in contenido

def test_pagina_partido_asistido_si_partido_anterior_si_partido_siguiente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
									VALUES('20245964', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria'),
										('202454564', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":""})

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20245964", "comentario":""})

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"202454564", "comentario":""})

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<button class="button-partido-anterior-asistido"' in contenido
		assert '<button class="button-partido-siguiente-asistido"' in contenido

def test_pagina_partido_asistido_partido_asistido_favorito(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "partido-favorito":"on"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert "/no_favorito_asistido.png" not in contenido
		assert "/favorito_asistido.png" in contenido
		assert '<h3 class="titulo-partido-asistido-favorito">¡El mejor partido asistido!</h3>' in contenido

def test_pagina_partido_asistido_ventana_emergente_papelera_disponible(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"Comentario", "partido-favorito":"on"}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()

		respuesta.status_code==200
		assert '<img class="papelera-partido-asistido"' in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido
		assert "/partido/20190622/asistido/eliminar" in contenido

def test_pagina_partido_asistido_mapas_trayectos(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"A Coruna", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Avion", "ciudad-vuelta":"A Coruna", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()
 
		respuesta.status_code==200
		assert '<div class="tarjeta-mapa-trayecto-ida-vuelta-total"' in contenido
		assert "iframe" in contenido
		assert "/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_ida_vuelta_user_" in contenido
		assert '<div id="ventana-emergente-mapa" class="ventana-emergente-mapa">' in contenido
		assert '<div class="contenido-ventana-emergente-mapa">' in contenido
		assert '<div class="botones-mapa-detalle-ida-vuelta">' in contenido
		assert '<div class="contenedor-mapa-ida-vuelta-detalle">' in contenido
		assert "iframe" in contenido
		assert "/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_ida_user_" in contenido
		assert "/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_vuelta_user_" in contenido
		assert '<img class="no-mapa"' not in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "trayectos")
 
		ruta_mapa_ida_vuelta=os.path.join(ruta_carpeta_mapas, "mapa_trayecto_ida_vuelta_user_nacho98.html")
 
		assert os.path.exists(ruta_mapa_ida_vuelta)
 
		with open(ruta_mapa_ida_vuelta, "r") as mapa:
 
			contenido=mapa.read()
 
			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[43.3667, -8.3833]" in contenido
			assert "/static/imagenes/iconos/inicio.png" in contenido
			assert "A Coruna" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido
			assert "Metropolitano" in contenido
			assert "var poly_line_" in contenido
			assert "L.polyline" in contenido
			assert "[[43.3667, -8.3833], [40.436, -3.599]]" in contenido
			assert "solid red" not in contenido
			assert "solid blue" not in contenido
			assert "solid orange" in contenido
			assert '"color": "red"' not in contenido
			assert '"color": "blue"' not in contenido
			assert '"color": "orange"' in contenido
			assert "background-color: #ffcccc" not in contenido
			assert "background-color: #95ebf7" not in contenido
			assert "background-color: #ffdd73" in contenido
 
		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "trayectos")
 
		ruta_mapa_ida=os.path.join(ruta_carpeta_mapas, "mapa_trayecto_ida_user_nacho98.html")
 
		assert os.path.exists(ruta_mapa_ida)
 
		with open(ruta_mapa_ida, "r") as mapa:
 
			contenido=mapa.read()
 
			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[43.3667, -8.3833]" in contenido
			assert "/static/imagenes/iconos/inicio.png" in contenido
			assert "A Coruna" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido
			assert "Metropolitano" in contenido
			assert "var poly_line_" in contenido
			assert "L.polyline" in contenido
			assert "[[43.3667, -8.3833], [40.436, -3.599]]" in contenido
			assert "solid red" in contenido
			assert "solid blue" not in contenido
			assert "solid orange" not in contenido
			assert '"color": "red"' in contenido
			assert '"color": "blue"' not in contenido
			assert '"color": "orange"' not in contenido
			assert "background-color: #ffcccc" in contenido
			assert "background-color: #95ebf7" not in contenido
			assert "background-color: #ffdd73" not in contenido

		ruta_mapa_vuelta=os.path.join(ruta_carpeta_mapas, "mapa_trayecto_vuelta_user_nacho98.html")
 
		assert os.path.exists(ruta_mapa_vuelta)
 
		with open(ruta_mapa_vuelta, "r") as mapa:
 
			contenido=mapa.read()
 
			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[43.3667, -8.3833]" in contenido
			assert "/static/imagenes/iconos/inicio.png" in contenido
			assert "A Coruna" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido
			assert "Metropolitano" in contenido
			assert "var poly_line_" in contenido
			assert "L.polyline" in contenido
			assert "[[40.436, -3.599], [43.3667, -8.3833]]" in contenido
			assert "solid red" not in contenido
			assert "solid blue" in contenido
			assert "solid orange" not in contenido
			assert '"color": "red"' not in contenido
			assert '"color": "blue"' in contenido
			assert '"color": "orange"' not in contenido
			assert "background-color: #ffcccc" not in contenido
			assert "background-color: #95ebf7" in contenido
			assert "background-color: #ffdd73" not in contenido

def test_pagina_partido_asistido_mapas_trayectos_ida_vuelta_diferente(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"A Coruna", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Avion", "ciudad-vuelta":"Barcelona", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()
 
		respuesta.status_code==200
		assert '<div class="tarjeta-mapa-trayecto-ida-vuelta-total"' in contenido
		assert "iframe" in contenido
		assert "/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_ida_vuelta_user_" in contenido
		assert '<div id="ventana-emergente-mapa" class="ventana-emergente-mapa">' in contenido
		assert '<div class="contenido-ventana-emergente-mapa">' in contenido
		assert '<div class="botones-mapa-detalle-ida-vuelta">' in contenido
		assert '<div class="contenedor-mapa-ida-vuelta-detalle">' in contenido
		assert "iframe" in contenido
		assert "/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_ida_user_" in contenido
		assert "/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_vuelta_user_" in contenido
		assert '<img class="no-mapa"' not in contenido

		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "trayectos")
 
		ruta_mapa_ida_vuelta=os.path.join(ruta_carpeta_mapas, "mapa_trayecto_ida_vuelta_user_nacho98.html")
 
		assert os.path.exists(ruta_mapa_ida_vuelta)
 
		with open(ruta_mapa_ida_vuelta, "r") as mapa:
 
			contenido=mapa.read()

			assert '<div class="folium-map" id="map_' in contenido
			assert "var map_" in contenido
			assert "L.map" in contenido
			assert "var marker_" in contenido
			assert "L.marker" in contenido
			assert "[43.3667, -8.3833]" in contenido
			assert "/static/imagenes/iconos/inicio.png" in contenido
			assert "A Coruna" in contenido
			assert "[40.436, -3.599]" in contenido
			assert "/static/imagenes/iconos/estadio_mapa.png" in contenido
			assert "Metropolitano" in contenido
			assert "var poly_line_" in contenido
			assert "L.polyline" in contenido
			assert "[[43.3667, -8.3833], [40.436, -3.599]]" in contenido
			assert "[41.3825, 2.1769]" in contenido
			assert "Barcelona" in contenido
			assert "[[40.436, -3.599], [41.3825, 2.1769]]" in contenido
			assert "solid red" in contenido
			assert "solid blue" in contenido
			assert "solid orange" not in contenido
			assert '"color": "red"' in contenido
			assert '"color": "blue"' in contenido
			assert '"color": "orange"' not in contenido
			assert "background-color: #ffcccc" in contenido
			assert "background-color: #95ebf7" in contenido
			assert "background-color: #ffdd73" not in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho99",),("golden",),("amanda",),("amanda99",),("nacho98",)]
)
def test_pagina_partido_asistido_mapas_trayectos_usuarios(cliente, conexion_entorno, password_hash, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": usuario, "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"A Coruna", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Avion", "ciudad-vuelta":"A Coruna", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		respuesta=cliente_abierto.get("/partido/20190622/asistido")

		contenido=respuesta.data.decode()
 
		respuesta.status_code==200
		assert '<div class="tarjeta-mapa-trayecto-ida-vuelta-total"' in contenido
		assert "iframe" in contenido
		assert "/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_ida_vuelta_user_" in contenido
		assert '<div id="ventana-emergente-mapa" class="ventana-emergente-mapa">' in contenido
		assert '<div class="contenido-ventana-emergente-mapa">' in contenido
		assert '<div class="botones-mapa-detalle-ida-vuelta">' in contenido
		assert '<div class="contenedor-mapa-ida-vuelta-detalle">' in contenido
		assert "iframe" in contenido
		assert "/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_ida_user_" in contenido
		assert "/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_vuelta_user_" in contenido
		assert '<img class="no-mapa"' not in contenido
 
		ruta_carpeta_mapas=os.path.join(os.path.abspath(".."), "src", "templates", "mapas", "trayectos")

		ruta_mapa_ida_vuelta=os.path.join(ruta_carpeta_mapas, f"mapa_trayecto_ida_vuelta_user_{usuario}.html")
 
		assert os.path.exists(ruta_mapa_ida_vuelta)
 
		ruta_mapa_ida=os.path.join(ruta_carpeta_mapas, f"mapa_trayecto_ida_user_{usuario}.html")
 
		assert os.path.exists(ruta_mapa_ida)
 
		ruta_mapa_vuelta=os.path.join(ruta_carpeta_mapas, f"mapa_trayecto_vuelta_user_{usuario}.html")
 
		assert os.path.exists(ruta_mapa_vuelta)

def test_pagina_mapa_partido_asistido_sin_login(cliente):

	respuesta=cliente.get("/partido/20190622/asistido/trayecto/mapa/nombre_mapa", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_mapa_partido_asistido_mapa_trayecto_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		with pytest.raises(FileNotFoundError):

			cliente_abierto.get("/partido/20190622/asistido/trayecto/mapa/nombre_mapa.html")

def test_pagina_mapa_partido_asistido_mapa_trayecto_ida_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"A Coruna", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Avion", "ciudad-vuelta":"A Coruna", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/partido/20190622/asistido")

		respuesta=cliente_abierto.get("/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_ida_user_nacho98.html")

		contenido=respuesta.data.decode()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "[43.3667, -8.3833]" in contenido
		assert "/static/imagenes/iconos/inicio.png" in contenido
		assert "A Coruna" in contenido
		assert "[40.436, -3.599]" in contenido
		assert "Metropolitano" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert "[[43.3667, -8.3833], [40.436, -3.599]]" in contenido
		assert "solid red" in contenido
		assert "solid blue" not in contenido
		assert "solid orange" not in contenido
		assert '"color": "red"' in contenido
		assert '"color": "blue"' not in contenido
		assert '"color": "orange"' not in contenido
		assert "background-color: #ffcccc" in contenido
		assert "background-color: #95ebf7" not in contenido
		assert "background-color: #ffdd73" not in contenido

def test_pagina_mapa_partido_asistido_mapa_trayecto_vuelta_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"A Coruna", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Avion", "ciudad-vuelta":"A Coruna", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/partido/20190622/asistido")

		respuesta=cliente_abierto.get("/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_vuelta_user_nacho98.html")

		contenido=respuesta.data.decode()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "[43.3667, -8.3833]" in contenido
		assert "/static/imagenes/iconos/inicio.png" in contenido
		assert "A Coruna" in contenido
		assert "[40.436, -3.599]" in contenido
		assert "Metropolitano" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert "[[40.436, -3.599], [43.3667, -8.3833]]" in contenido
		assert "solid red" not in contenido
		assert "solid blue" in contenido
		assert "solid orange" not in contenido
		assert '"color": "red"' not in contenido
		assert '"color": "blue"' in contenido
		assert '"color": "orange"' not in contenido
		assert "background-color: #ffcccc" not in contenido
		assert "background-color: #95ebf7" in contenido
		assert "background-color: #ffdd73" not in contenido

def test_pagina_mapa_partido_asistido_mapa_trayecto_ida_vuelta_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"A Coruna", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Avion", "ciudad-vuelta":"A Coruna", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		cliente_abierto.post("/insertar_partido_asistido", data=data)

		cliente_abierto.get("/partido/20190622/asistido")

		respuesta=cliente_abierto.get("/partido/20190622/asistido/trayecto/mapa/mapa_trayecto_ida_vuelta_user_nacho98.html")

		contenido=respuesta.data.decode()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "[43.3667, -8.3833]" in contenido
		assert "/static/imagenes/iconos/inicio.png" in contenido
		assert "A Coruna" in contenido
		assert "[40.436, -3.599]" in contenido
		assert "Metropolitano" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert "[[43.3667, -8.3833], [40.436, -3.599]]" in contenido
		assert "solid red" not in contenido
		assert "solid blue" not in contenido
		assert "solid orange" in contenido
		assert '"color": "red"' not in contenido
		assert '"color": "blue"' not in contenido
		assert '"color": "orange"' in contenido
		assert "background-color: #ffcccc" not in contenido
		assert "background-color: #95ebf7" not in contenido
		assert "background-color: #ffdd73" in contenido