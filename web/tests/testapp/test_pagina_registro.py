import pytest

def test_pagina_registro(cliente):

	respuesta=cliente.get("/registro")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Crear Una Cuenta</h1>" in contenido

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "fecha_nacimiento", "equipo"],
	[
		(None, "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", None, "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho", None, "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho", "dorado", None, "1998-02-16", "atleti"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", None, "atleti"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", None),
		("carlos_456", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho1", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho", "dorado2", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nacho", "dorado", "12345678", "1998-02-16", "atleti"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2098-02-16", "atleti"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti?co")
	]
)
def test_pagina_singin_datos_incorrectos(cliente, usuario, nombre, apellido, contrasena, fecha_nacimiento, equipo):

	respuesta=cliente.post("/singin", data={"usuario":usuario,"nombre":nombre, "apellido":apellido,
											"contrasena":contrasena, "fecha-nacimiento":fecha_nacimiento,
											"equipo":equipo})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("naCho98",),("nacho",),("amanditaa",),("amanda99",)]
)
def test_pagina_singin_usuario_existente(cliente, conexion, usuario):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES(%s)""", ("atleti",))

	conexion.insertarUsuario(usuario, "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti")

	conexion.confirmar()

	respuesta=cliente.post("/singin", data={"usuario":usuario,"nombre":"nacho", "apellido":"dorado",
											"contrasena":"Ab!CdEfGhIJK3LMN", "fecha-nacimiento":"1998-02-16",
											"equipo":"atleti"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "fecha_nacimiento", "equipo"],
	[
		("nacho98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("hola", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
		("golden98", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1900-02-16", "atleti"),
		("golden98", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti-madrid"),
		("golden", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti"),
	]
)
def test_pagina_singin_correcto(cliente, conexion, usuario, nombre, apellido, contrasena, fecha_nacimiento, equipo):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES(%s)""", (equipo,))

	conexion.confirmar()

	respuesta=cliente.post("/singin", data={"usuario":usuario,"nombre":nombre, "apellido":apellido,
											"contrasena":contrasena, "fecha-nacimiento":fecha_nacimiento,
											"equipo":equipo})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert f"<p>Gracias por registrarte en nuestra plataforma, {nombre.title()}.</p>" in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia!</p>" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

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
def test_pagina_singin_correctos(cliente, conexion, usuarios_agregar):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES(%s)""", ("atleti",))

	conexion.confirmar()

	for usuario in usuarios_agregar:

		cliente.post("/singin", data={"usuario":usuario, "nombre":"nacho", "apellido":"dorado",
										"contrasena":"Ab!CdEfGhIJK3LMN", "fecha-nacimiento":"1998-02-16",
										"equipo":"atleti"})

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==len(usuarios_agregar)