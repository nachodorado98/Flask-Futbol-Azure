import pytest

def test_tabla_trayecto_partido_asistido_vacia(conexion):

	conexion.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20190622", "nacho")]
)
def test_insertar_trayecto_partido_asistido(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido(partido_id, usuario, "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id", partido_id, usuario, "I", 103, "Transporte", 103)

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	trayectos_partido_asistido=conexion_entorno.c.fetchall()

	assert len(trayectos_partido_asistido)==1

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20190622", "nacho")]
)
def test_insertar_trayecto_partido_asistido_ida_vuelta(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido(partido_id, usuario, "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_ida", partido_id, usuario, "I", 103, "Transporte", 103)

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_vuelta", partido_id, usuario, "V", 103, "Transporte", 103)

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	trayectos_partido_asistido=conexion_entorno.c.fetchall()

	assert len(trayectos_partido_asistido)==2

def test_eliminar_trayectos_partido_asistido_no_existen_partidos(conexion):

	conexion.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion.c.fetchall()

	conexion.eliminarTrayectosPartidoAsistido("20190622", "nacho")

	conexion.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion.c.fetchall()

def test_eliminar_trayectos_partido_asistido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

	conexion_entorno.eliminarTrayectosPartidoAsistido("20190622", "otro")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

def test_eliminar_trayectos_partido_asistido_no_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

	conexion_entorno.eliminarTrayectosPartidoAsistido("20190622", "nacho")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

def test_eliminar_trayectos_partido_asistido_no_existen_trayectos(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

	conexion_entorno.eliminarTrayectosPartidoAsistido("20190622", "nacho")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

def test_eliminar_trayectos_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_ida", "20190622", "nacho", "I", 103, "Transporte", 103)

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert conexion_entorno.c.fetchall()

	conexion_entorno.eliminarTrayectosPartidoAsistido("20190622", "nacho")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()