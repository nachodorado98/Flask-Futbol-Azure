import pytest

def test_tabla_partido_asistido_favorito_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_asistido_favorito")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20190622", "nacho")]
)
def test_insertar_partido_asistidos_favorito_usuario(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido(partido_id, usuario, "comentario")

	conexion_entorno.insertarPartidoAsistidoFavorito(partido_id, usuario)

	conexion_entorno.c.execute("SELECT * FROM partido_asistido_favorito")

	partidos_asistidos_favoritos=conexion_entorno.c.fetchall()

	assert len(partidos_asistidos_favoritos)==1

def test_existe_partido_asistido_favorito_no_existen(conexion):

	assert not conexion.existe_partido_asistido_favorito("20190622", "nacho")

def test_existe_partido_asistido_favorito_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.existe_partido_asistido_favorito("20190622", "otro")

def test_existe_partido_asistido_favorito_no_existe_partido_favorito(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.existe_partido_asistido_favorito("20190622", "nacho")

def test_existe_partido_asistido_favorito(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarPartidoAsistidoFavorito("20190622", "nacho")

	assert conexion_entorno.existe_partido_asistido_favorito("20190622", "nacho")

def test_obtener_partido_asistido_favorito_no_existen(conexion):

	assert not conexion.obtenerPartidoAsistidoFavorito("nacho")

def test_obtener_partido_asistido_favorito_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.obtenerPartidoAsistidoFavorito("otro")

def test_obtener_partido_asistido_favorito_no_existe_partido_favorito(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.obtenerPartidoAsistidoFavorito("nacho")

def test_obtener_partido_asistido_favorito(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarPartidoAsistidoFavorito("20190622", "nacho")

	partido_asistido_usuario=conexion_entorno.obtenerPartidoAsistidoFavorito("nacho")

	assert partido_asistido_usuario=="20190622"