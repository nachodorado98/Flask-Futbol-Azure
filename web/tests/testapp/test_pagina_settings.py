def test_pagina_settings_sin_login(cliente):

	respuesta=cliente.get("/settings", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_settings(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente.get("/settings", follow_redirects=True)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="tarjeta-configuracion">' in contenido
		assert '<p class="titulo-pagina-configuracion">' in contenido
		assert '<div class="contenedor-configuracion">' in contenido
		assert '<div id="ventana-emergente" class="ventana-emergente">' in contenido