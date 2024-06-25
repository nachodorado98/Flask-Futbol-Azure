def test_pagina_inicio(cliente):

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido