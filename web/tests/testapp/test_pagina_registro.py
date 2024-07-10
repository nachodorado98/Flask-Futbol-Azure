import pytest

def test_pagina_registro(cliente):

	respuesta=cliente.get("/registro")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Crear Una Cuenta</h1>" in contenido

@pytest.mark.parametrize(["usuario", "correo", "nombre", "apellido", "contrasena", "fecha_nacimiento", "equipo"],
	[
		(None, "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", None, "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho@gmail.es", None, "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", None, "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", None, "1998-02-16", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", None, "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", None),
		("carlos_456", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho@.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho@gmail.es", "nacho1", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado2", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "12345678", "1998-02-16", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2098-02-16", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti?co")
	]
)
def test_pagina_singin_datos_incorrectos(cliente, usuario, correo, nombre, apellido, contrasena, fecha_nacimiento, equipo):

	respuesta=cliente.post("/singin", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"fecha-nacimiento":fecha_nacimiento,
											"equipo":equipo})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("naCho98",),("nacho",),("amanditaa",),("amanda99",)]
)
def test_pagina_singin_usuario_existente(cliente, conexion_entorno, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.es", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atletico-madrid")

	conexion_entorno.confirmar()

	respuesta=cliente.post("/singin", data={"usuario":usuario, "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16",
											"equipo":"atletico-madrid"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario", "correo", "nombre", "apellido", "contrasena", "fecha_nacimiento", "equipo"],
	[
		("nacho98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1999-07-16", "atletico-madrid"),
		("golnachoen98", "nacho@golden.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atletico-madrid"),
		("golden98", "nacho@gmail.es", "nachogol", "dorado", "Ab!Golden19&9", "1998-02-01", "atletico-madrid"),
		("golde98", "nacho@gmail.es", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-05-16", "atletico-madrid"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "16&goldenNacho&98", "1998-02-16", "atletico-madrid"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2005-02-16", "atletico-madrid"),
		("golden9", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1990-02-16", "atletico-madrid")
	]
)
def test_pagina_singin_correcto(cliente, conexion_entorno, usuario, correo, nombre, apellido, contrasena, fecha_nacimiento, equipo):

	respuesta=cliente.post("/singin", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"fecha-nacimiento":fecha_nacimiento,
											"equipo":equipo})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert f"<p>Gracias por registrarte en nuestra plataforma, {nombre.title()}.</p>" in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia!</p>" in contenido

	conexion_entorno.c.execute("SELECT * FROM usuarios")

	usuarios=conexion_entorno.c.fetchall()

	assert len(usuarios)==1

@pytest.mark.parametrize(["usuarios_agregar"],
	[
		(["nacho98", "naCho98", "nacho", "amanditaa","amanda99"],),
		(["nacho98", "nacho", "amanditaa","amanda99"],),
		(["nacho98", "amanditaa","amanda99"],),
		(["nacho98", "naCho98", "nacho", "amanda99"],),
		(["nacho98", "amanda99"],)
	]
)
def test_pagina_singin_correctos(cliente, conexion_entorno, usuarios_agregar):

	for usuario in usuarios_agregar:

		cliente.post("/singin", data={"usuario":usuario, "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16",
										"equipo":"atletico-madrid"})

	conexion_entorno.c.execute("SELECT * FROM usuarios")

	usuarios=conexion_entorno.c.fetchall()

	assert len(usuarios)==len(usuarios_agregar)