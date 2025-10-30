import pytest

def test_tabla_porra_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM porra_partidos")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20200622", "nacho")]
)
def test_insertar_porra_partido_usuario(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido(usuario, partido_id, 1, 0)

	conexion_entorno.c.execute("SELECT * FROM porra_partidos")

	porra_partidos=conexion_entorno.c.fetchall()

	assert len(porra_partidos)==1

def test_existe_porra_partido_no_existen(conexion):

	assert not conexion.existe_porra_partido("20200622", "nacho")

def test_existe_porra_partido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.existe_porra_partido("20200622", "otro")

def test_existe_porra_partido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho", "20200622", 1, 0)

	assert conexion_entorno.existe_porra_partido("20200622", "nacho")

def test_obtener_porra_partido_no_existen(conexion):

	assert not conexion.obtenerPorraPartido("20200622", "nacho")

def test_obtener_porra_partido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerPorraPartido("20200622", "otro")

def test_obtener_porra_partido_no_existe_porra(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerPorraPartido("20200622", "nacho")

def test_obtener_porra_partido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho", "20200622", 1, 0)

	porra_partido=conexion_entorno.obtenerPorraPartido("20200622", "nacho")

	assert porra_partido==(1, 0)