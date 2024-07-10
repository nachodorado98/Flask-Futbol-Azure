import pytest

def test_tabla_usuarios_vacia(conexion):

	conexion.c.execute("SELECT * FROM usuarios")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["usuario", "contrasena", "nombre", "apellido", "fecha_nacimiento", "equipo"],
	[
		("nacho98", "1234", "nacho", "dorado", "1998-02-16", "atleti"),
		("nacho948", "12vvnvvb34", "naegcho", "dordado", "1999-08-06", "atm"),
		("nacho", "12vvn&fvvb34", "nachitoo", "dordado", "1998-02-16", "atleti")
	]
)
def test_insertar_usuario(conexion, usuario, contrasena, nombre, apellido, fecha_nacimiento, equipo):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES(%s)""", (equipo,))

	conexion.confirmar()

	conexion.insertarUsuario(usuario, contrasena, nombre, apellido, fecha_nacimiento, equipo)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_usuarios(conexion, numero_usuarios):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES(%s)""", ("atleti",))

	conexion.confirmar()

	for numero in range(numero_usuarios):

		conexion.insertarUsuario(f"nacho{numero}", "1234", "nacho", "dorado", "1998-02-16", "atleti")

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==numero_usuarios

def test_existe_usuario_no_existen(conexion):

	assert not conexion.existe_usuario("nacho98")

def test_existe_usuario_existen_no_existente(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES(%s)""", ("atleti",))

	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", "1998-02-16", "atleti")

	assert not conexion.existe_usuario("nacho99")

def test_existe_usuario_existen_existente(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES(%s)""", ("atleti",))

	conexion.confirmar()

	conexion.insertarUsuario("nacho98", "1234", "nacho", "dorado", "1998-02-16", "atleti")

	assert conexion.existe_usuario("nacho98")