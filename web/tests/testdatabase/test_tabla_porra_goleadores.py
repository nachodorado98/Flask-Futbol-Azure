import pytest

def test_tabla_porra_goleadores_vacia(conexion):

	conexion.c.execute("SELECT * FROM porra_goleadores")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20200622", "nacho")]
)
def test_insertar_porra_goleadores_usuario(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido(f"{usuario}-{partido_id}", usuario, partido_id, 1, 0)

	conexion_entorno.insertarGoleadorPorra(f"{usuario}-{partido_id}", "julian-alvarez", 1, True)

	conexion_entorno.c.execute("SELECT * FROM porra_goleadores")

	porra_goleadores=conexion_entorno.c.fetchall()

	assert len(porra_goleadores)==1

def test_obtener_goleadores_porra_partido_no_existen(conexion):

	assert not conexion.obtenerGoleadoresPorraPartido("20200622", "nacho")

def test_obtener_goleadores_porra_partido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerGoleadoresPorraPartido("20200622", "otro")

def test_obtener_goleadores_porra_partido_no_existe_porra(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerGoleadoresPorraPartido("20200622", "nacho")

def test_obtener_goleadores_porra_partido_no_existen_goleadores(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho-20200622", "nacho", "20200622", 1, 0)

	assert not conexion_entorno.obtenerGoleadoresPorraPartido("20200622", "nacho")

def test_obtener_goleadores_porra_partido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho-20200622", "nacho", "20200622", 1, 0)

	conexion_entorno.insertarGoleadorPorra("nacho-20200622", "julian-alvarez", 1, True)

	porra_goleadores_partido=conexion_entorno.obtenerGoleadoresPorraPartido("20200622", "nacho")

	assert len(porra_goleadores_partido)==1