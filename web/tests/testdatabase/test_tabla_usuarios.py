import pytest

def test_tabla_usuarios_vacia(conexion):

	conexion.c.execute("SELECT * FROM usuarios")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["usuario", "correo", "contrasena", "nombre", "apellido", "fecha_nacimiento", "codciudad", "equipo"],
	[
		("nacho98", "nacho@correo", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid"),
		("nacho948", "correo", "12vvnvvb34", "naegcho", "dordado", "1999-08-06", 1, "atletico-madrid"),
		("nacho", "micorreo@correo.es", "12vvn&fvvb34", "nachitoo", "dordado", "1998-02-16", 22, "atletico-madrid")
	]
)
def test_insertar_usuario(conexion_entorno, usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, codciudad, equipo):

	conexion_entorno.insertarUsuario(usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, codciudad, equipo)

	conexion_entorno.c.execute("SELECT * FROM usuarios")

	usuarios=conexion_entorno.c.fetchall()

	assert len(usuarios)==1

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_usuarios(conexion_entorno, numero_usuarios):

	for numero in range(numero_usuarios):

		conexion_entorno.insertarUsuario(f"nacho{numero}", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.c.execute("SELECT * FROM usuarios")

	usuarios=conexion_entorno.c.fetchall()

	assert len(usuarios)==numero_usuarios

def test_existe_usuario_no_existen(conexion):

	assert not conexion.existe_usuario("nacho98")

def test_existe_usuario_existen_no_existente(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.existe_usuario("nacho99")

def test_existe_usuario_existen_existente(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert conexion_entorno.existe_usuario("nacho98")

def test_obtener_contrasena_usuario_no_existe(conexion):

	assert conexion.obtenerContrasenaUsuario("nacho98") is None

def test_obtener_contrasena_usuario_existen(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert conexion_entorno.obtenerContrasenaUsuario("nacho98")=="1234"

def test_obtener_nombre_usuario_no_existe(conexion):

	assert conexion.obtenerNombre("nacho98") is None

def test_obtener_nombre_usuario_existen(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert conexion_entorno.obtenerNombre("nacho98")=="nacho"

def test_obtener_equipo_usuario_no_existe(conexion):

	assert conexion.obtenerEquipo("nacho98") is None

def test_obtener_equipo_usuario_existen(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert conexion_entorno.obtenerEquipo("nacho98")=="atletico-madrid"

def test_obtener_pais_ciudad_usuario_usuario_no_existe(conexion):

	assert not conexion.obtenerPaisCiudadUsuario("nacho98")

def test_obtener_pais_ciudad_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	pais, ciudad=conexion_entorno.obtenerPaisCiudadUsuario("nacho98")

	assert pais=="España"
	assert ciudad=="Madrid"

def test_eliminar_usuario_no_existe_usuario(conexion):

	assert not conexion.existe_usuario("nacho98")

	conexion.eliminarUsuario("nacho98")

	assert not conexion.existe_usuario("nacho98")

def test_eliminar_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert conexion_entorno.existe_usuario("nacho98")

	conexion_entorno.eliminarUsuario("nacho98")

	assert not conexion_entorno.existe_usuario("nacho98")

def test_obtener_imagen_perfil_usuario_no_existe_usuario(conexion):

	assert not conexion.obtenerImagenPerfilUsuario("nacho98")

def test_obtener_imagen_perfil_usuario_no_existe_imagen(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert conexion_entorno.obtenerImagenPerfilUsuario("nacho98")=='-1'

def test_obtener_imagen_perfil_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.c.execute("UPDATE usuarios SET Imagen_Perfil='imagen_perfil.png'")

	conexion_entorno.confirmar()

	assert conexion_entorno.obtenerImagenPerfilUsuario("nacho98")=='imagen_perfil.png'

def test_actualizar_imagen_perfil_usuario_no_existe_usuario(conexion_entorno):

	assert not conexion_entorno.existe_usuario("nacho")

	conexion_entorno.actualizarImagenPerfilUsuario("nacho", "imagen.png")

	assert not conexion_entorno.existe_usuario("nacho")

def test_actualizar_imagen_perfil_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.c.execute("SELECT Imagen_Perfil FROM usuarios")

	imagen=conexion_entorno.c.fetchone()["imagen_perfil"]

	assert imagen==None

	conexion_entorno.actualizarImagenPerfilUsuario("nacho", "imagen.png")

	conexion_entorno.c.execute("SELECT Imagen_Perfil FROM usuarios")

	imagen=conexion_entorno.c.fetchone()["imagen_perfil"]

	assert imagen=="imagen.png"