import pytest

def test_pagina_actualizar_comentario_partido_asistido_sin_login(cliente):

	data={"nuevo-comentario":"comentario nuevo"}

	respuesta=cliente.post("/actualizar_comentario_partido_asistido/20190622", data=data, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_actualizar_comentario_partido_asistido_partido_no_existente(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"nuevo-comentario":"comentario nuevo"}

		respuesta=cliente.post("/actualizar_comentario_partido_asistido/no_existo", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

def test_pagina_actualizar_comentario_partido_asistido_partido_asistido_no_existente(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"nuevo-comentario":"comentario nuevo"}

		respuesta=cliente.post("/actualizar_comentario_partido_asistido/20190622", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno.c.fetchall()

@pytest.mark.parametrize(["caracteres"],
	[(300,),(256,),(1000,),(43575,)]
)
def test_pagina_actualizar_comentario_partido_asistido_comentario_demasiado_extenso(cliente, conexion_entorno, caracteres, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":""})

		data={"nuevo-comentario":"a"*caracteres}

		respuesta=cliente.post("/actualizar_comentario_partido_asistido/20190622", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

def test_pagina_actualizar_comentario_partido_asistido_sin_comentario(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":"comentario"})

		data={"nuevo-comentario":None}

		respuesta=cliente.post("/actualizar_comentario_partido_asistido/20190622", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partido/20190622/asistido"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		partidos=conexion_entorno.c.fetchall()

		assert len(partidos)==1
		assert partidos[0]["comentario"] is None

def test_pagina_actualizar_comentario_partido_asistido(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":"comentario"})

		data={"nuevo-comentario":"comentario nuevo"}

		respuesta=cliente.post("/actualizar_comentario_partido_asistido/20190622", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partido/20190622/asistido"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		partidos=conexion_entorno.c.fetchall()

		assert len(partidos)==1
		assert partidos[0]["comentario"]=="comentario nuevo"

def test_pagina_actualizar_comentario_partido_asistido_comentario_limite(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/insertar_partido_asistido", data={"partido_anadir":"20190622", "comentario":"comentario"})

		data={"nuevo-comentario":"a"*255}

		respuesta=cliente.post("/actualizar_comentario_partido_asistido/20190622", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partido/20190622/asistido"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		partidos=conexion_entorno.c.fetchall()

		assert len(partidos)==1
		assert partidos[0]["comentario"]=="a"*255