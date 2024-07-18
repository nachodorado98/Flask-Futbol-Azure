import pytest

def test_tabla_usuarios_vacia(conexion):

	conexion.c.execute("SELECT * FROM usuarios")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["usuario", "correo", "contrasena", "nombre", "apellido", "fecha_nacimiento", "equipo"],
	[
		("nacho98", "nacho@correo", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid"),
		("nacho948", "correo", "12vvnvvb34", "naegcho", "dordado", "1999-08-06", "atletico-madrid"),
		("nacho", "micorreo@correo.es", "12vvn&fvvb34", "nachitoo", "dordado", "1998-02-16", "atletico-madrid")
	]
)
def test_insertar_usuario(conexion_entorno, usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, equipo):

	conexion_entorno.insertarUsuario(usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, equipo)

	conexion_entorno.c.execute("SELECT * FROM usuarios")

	usuarios=conexion_entorno.c.fetchall()

	assert len(usuarios)==1

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_usuarios(conexion_entorno, numero_usuarios):

	for numero in range(numero_usuarios):

		conexion_entorno.insertarUsuario(f"nacho{numero}", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.c.execute("SELECT * FROM usuarios")

	usuarios=conexion_entorno.c.fetchall()

	assert len(usuarios)==numero_usuarios

def test_existe_usuario_no_existen(conexion):

	assert not conexion.existe_usuario("nacho98")

def test_existe_usuario_existen_no_existente(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.existe_usuario("nacho99")

def test_existe_usuario_existen_existente(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert conexion_entorno.existe_usuario("nacho98")

def test_obtener_contrasena_usuario_no_existe(conexion):

	assert conexion.obtenerContrasenaUsuario("nacho98") is None

def test_obtener_contrasena_usuario_existen(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert conexion_entorno.obtenerContrasenaUsuario("nacho98")=="1234"

def test_obtener_nombre_usuario_no_existe(conexion):

	assert conexion.obtenerNombre("nacho98") is None

def test_obtener_nombre_usuario_existen(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert conexion_entorno.obtenerNombre("nacho98")=="nacho"

def test_obtener_equipo_usuario_no_existe(conexion):

	assert conexion.obtenerEquipo("nacho98") is None

def test_obtener_equipo_usuario_existen(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert conexion_entorno.obtenerEquipo("nacho98")=="atletico-madrid"