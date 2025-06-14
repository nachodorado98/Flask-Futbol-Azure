import pytest
import os
import time

from src.utilidades.utils import vaciarCarpeta

def test_pagina_registro(cliente):

	respuesta=cliente.get("/registro")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Crear Una Cuenta</h1>" in contenido

	ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

	vaciarCarpeta(ruta_carpeta_imagenes)

@pytest.mark.parametrize(["usuario", "correo", "nombre", "apellido", "contrasena", "fecha_nacimiento", "ciudad", "equipo"],
	[
		(None, "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atleti"),
		("golden98", None, "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", None, "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", None, "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", None, "1998-02-16", "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", None, "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", None),
		("carlos_456", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atleti"),
		("golden98", "nacho@.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", "nacho1", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado2", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "12345678", "1998-02-16", "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2098-02-16", "Madrid", "atleti"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atleti?co")
	]
)
def test_pagina_singin_datos_incorrectos(cliente, usuario, correo, nombre, apellido, contrasena, fecha_nacimiento, ciudad, equipo):

	respuesta=cliente.post("/singin", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"fecha-nacimiento":fecha_nacimiento, "ciudad":ciudad, "equipo":equipo})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

	ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

	assert not os.path.exists(ruta_carpeta_imagenes+f"/{usuario}")

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("naCho98",),("nacho",),("amanditaa",),("amanda99",)]
)
def test_pagina_singin_usuario_existente(cliente, conexion_entorno, usuario):

	conexion_entorno.insertarUsuario(usuario, "nacho@gmail.es", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", 103, "atletico-madrid")

	respuesta=cliente.post("/singin", data={"usuario":usuario, "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":"Madrid", "equipo":"atletico-madrid"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

	ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

	ruta_carpeta_imagenes_usuario=os.path.join(ruta_carpeta_imagenes, usuario)

	assert not os.path.exists(ruta_carpeta_imagenes_usuario)

@pytest.mark.parametrize(["equipo"],
	[("atm",),("atleti",),("equipo",),("atleticomadrid",),("atletico madrid",),("atleti-madrid",)]
)
def test_pagina_singin_equipo_no_existente(cliente, conexion_entorno, equipo):

	respuesta=cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":"Madrid", "equipo":equipo})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

	ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

	ruta_carpeta_imagenes_usuario=os.path.join(ruta_carpeta_imagenes, "nacho98")

	assert not os.path.exists(ruta_carpeta_imagenes_usuario)

@pytest.mark.parametrize(["ciudad"],
	[("madrid",),("MADRID",),("Barna",),("Bcn",),("Tokio",),("tokyo",)]
)
def test_pagina_singin_ciudad_no_existente(cliente, conexion_entorno, ciudad):

	respuesta=cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":ciudad, "equipo":"atletico-madrid"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

	ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

	ruta_carpeta_imagenes_usuario=os.path.join(ruta_carpeta_imagenes, "nacho98")

	assert not os.path.exists(ruta_carpeta_imagenes_usuario)

@pytest.mark.parametrize(["usuario", "correo", "nombre", "apellido", "contrasena", "fecha_nacimiento", "ciudad", "equipo"],
	[
		("nacho98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1999-07-16", "Madrid", "atletico-madrid"),
		("golnachoen98", "nacho@golden.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Madrid", "atletico-madrid"),
		("golden98", "nacho@gmail.es", "nachogol", "dorado", "Ab!Golden19&9", "1998-02-01", "Madrid", "atletico-madrid"),
		("golde98", "nacho@gmail.es", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-05-16", "Madrid", "atletico-madrid"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "16&goldenNacho&98", "1998-02-16", "Madrid", "atletico-madrid"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2005-02-16", "Madrid", "atletico-madrid"),
		("golden9", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1990-02-16", "Madrid", "atletico-madrid")
	]
)
def test_pagina_singin_correcto(cliente, conexion_entorno, usuario, correo, nombre, apellido, contrasena, fecha_nacimiento, ciudad, equipo):

	respuesta=cliente.post("/singin", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"fecha-nacimiento":fecha_nacimiento, "ciudad":ciudad, "equipo":equipo})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert f"<p>Gracias por registrarte en nuestra plataforma, {nombre.title()}.</p>" in contenido
	assert "<p>Se han registrado tus datos junto con tu equipo favorito" in contenido
	assert f'<img src="/static/imagenes/favoritos/{equipo}.png'in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia!</p>" in contenido

	conexion_entorno.c.execute("SELECT * FROM usuarios")

	usuarios=conexion_entorno.c.fetchall()

	assert len(usuarios)==1

	ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

	ruta_carpeta_imagenes_usuario=os.path.join(ruta_carpeta_imagenes, usuario)

	assert os.path.exists(ruta_carpeta_imagenes_usuario)

	vaciarCarpeta(ruta_carpeta_imagenes)

@pytest.mark.parametrize(["usuarios_agregar"],
	[
		(["nacho98", "naCho98", "nacho", "amanditaa","amanda99"],),
		(["nacho98", "nacho", "amanditaa","amanda99"],),
		(["nacho98", "amanditaa","amanda99"],),
		(["nacho98", "naCho98", "nacho", "amanda99"],),
		(["nacho98", "amanda99"],)
	]
)
def test_pagina_singins_correctos(cliente, conexion_entorno, usuarios_agregar):

	for usuario in usuarios_agregar:

		cliente.post("/singin", data={"usuario":usuario, "correo":"nacho@gmail.com", "nombre":"nacho",
										"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
										"fecha-nacimiento":"1998-02-16", "ciudad": "Madrid", "equipo":"atletico-madrid"})

	conexion_entorno.c.execute("SELECT * FROM usuarios")

	usuarios=conexion_entorno.c.fetchall()

	assert len(usuarios)==len(usuarios_agregar)

	ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

	for usuario in usuarios_agregar:

		ruta_carpeta_imagenes_usuario=os.path.join(ruta_carpeta_imagenes, usuario)

		assert os.path.exists(ruta_carpeta_imagenes_usuario)

	vaciarCarpeta(ruta_carpeta_imagenes)

	time.sleep(5)

def test_pagina_singins_correcto_carpeta_datalake(cliente, conexion_entorno, datalake, entorno):

	time.sleep(20)

	cliente.post("/singin", data={"usuario":"nachodorado", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16", "ciudad": "Madrid", "equipo":"atletico-madrid"})

	conexion_entorno.c.execute("SELECT * FROM usuarios")

	assert len(conexion_entorno.c.fetchall())==1

	time.sleep(25)

	assert datalake.existe_carpeta(entorno, "usuarios/nachodorado")
	assert datalake.existe_carpeta(entorno, "usuarios/nachodorado/imagenes")
	assert datalake.existe_carpeta(entorno, "usuarios/nachodorado/perfil")

	datalake.cerrarConexion()

	ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes")

	vaciarCarpeta(ruta_carpeta_imagenes)

def test_pagina_obtener_ciudades_pais_sin_pais(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/ciudades_pais")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==400
		assert "error" in contenido

def test_pagina_obtener_ciudades_pais_pais_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/ciudades_pais?pais=no_existo")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==404
		assert "error" in contenido

def test_pagina_obtener_ciudades_pais(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/ciudades_pais?pais=España")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==404
		assert "error" not in contenido