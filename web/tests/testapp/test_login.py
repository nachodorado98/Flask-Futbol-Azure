import pytest
from flask_login import current_user

def test_pagina_inicio_sin_login(cliente):

	respuesta=cliente.get("/partidos", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho",),("nacho98",),("usuario_correcto",), ("amanda",)]
)
def test_pagina_inicio_con_login_usuario_no_existe(cliente, conexion, usuario):

	respuesta=cliente.post("/login", data={"usuario": "nacho", "contrasena": "Ab!CdEfGhIJK3LMN"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["contrasena"],
	[("213214hhj&&ff",),("354354vff",),("2223321",), ("fdfgh&&55fjfkAfh",)]
)
def test_pagina_inicio_con_login_usuario_existe_contrasena_error(cliente, conexion_entorno, contrasena):

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": contrasena})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_inicio_con_login(cliente, conexion_entorno):

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Partidos del" in contenido

def test_pagina_logout(cliente, conexion_entorno):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
												"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
												"fecha-nacimiento":"1998-02-16",
												"equipo":"atletico-madrid"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"})

		assert current_user.is_authenticated

		respuesta=cliente_abierto.get("/logout", follow_redirects=True)

		contenido=respuesta.data.decode()

		assert not current_user.is_authenticated

		assert respuesta.status_code==200
		assert "<h1>Iniciar Sesión</h1>" in contenido