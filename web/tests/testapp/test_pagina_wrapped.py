import pytest

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
		assert '<div id="ventana-emergente-partidos" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-partidos-asistidos">' in contenido
		assert '<div id="ventana-emergente-estadios" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-estadios-asistidos">' in contenido
		assert '<div id="ventana-emergente-estadios-nuevos" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-estadios-asistidos">' in contenido
		assert '<div id="ventana-emergente-equipos" class="ventana-emergente">' in contenido
		assert '<div class="tarjetas-equipos-vistos">' in contenido
		assert '<div class="contenedor-lateral contenedor-lateral-izq">' in contenido
		assert '<div class="circulo-partido-mas-goles">' in contenido
		assert '<div class="tarjeta-partido-mas-goles"' in contenido
		assert '<div class="circulo-estadisticas-partidos-asistidos">' in contenido
		assert '<div class="tarjeta-dato-grafica">' in contenido