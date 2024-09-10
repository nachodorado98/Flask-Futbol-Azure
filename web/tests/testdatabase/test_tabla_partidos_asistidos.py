import pytest

def test_tabla_partidos_asistidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM partidos_asistidos")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20190622", "nacho")]
)
def test_insertar_partido_usuario(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido(partido_id, usuario)

	conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

	partidos_asistidos=conexion_entorno.c.fetchall()

	assert len(partidos_asistidos)==1

def test_existe_partido_asistido_no_existen(conexion):

	assert not conexion.existe_partido_asistido("20190622", "nacho")

def test_existe_partido_asistido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho")

	conexion_entorno.confirmar()

	assert not conexion_entorno.existe_partido_asistido("20190622", "otro")

def test_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho")

	conexion_entorno.confirmar()

	assert conexion_entorno.existe_partido_asistido("20190622", "nacho")

def test_obtener_partidos_no_asistidos_usuario_no_existen_partidos(conexion):

	assert not conexion.obtenerPartidosNoAsistidosUsuario("nacho", "atletico-madrid")

def test_obtener_partidos_no_asistidos_partido_equipos_no_existen(conexion_entorno):

	assert not conexion_entorno.obtenerPartidosNoAsistidosUsuario("nacho", "atleti")

def test_obtener_partidos_no_asistidos_usuario(conexion_entorno):

	partidos=conexion_entorno.obtenerPartidosNoAsistidosUsuario("nacho", "atletico-madrid")

	assert len(partidos)==1

def test_obtener_partidos_no_asistidos_usuario_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerPartidosNoAsistidosUsuario("nacho", "atletico-madrid")

def test_obtener_partidos_no_asistidos_usuario_partido_asistido_otro_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarUsuario("otro", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "otro")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosNoAsistidosUsuario("nacho", "atletico-madrid")

	assert len(partidos)==1