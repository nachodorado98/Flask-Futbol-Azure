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

def test_obtener_trayecto_partido_asistido_no_existen_partidos(conexion):

	assert not conexion.obtenerTrayectoPartidoAsistido("20190622", "nacho", "I")

def test_obtener_trayecto_partido_asistido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "otro", "I")

def test_obtener_trayecto_partido_asistido_no_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "I")

def test_obtener_trayecto_partido_asistido_no_existen_trayectos(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "I")

def test_obtener_trayecto_partido_asistido_no_existe_tipo_trayecto(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_ida", "20190622", "nacho", "I", 103, "Transporte", 103)

	assert not conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "N")

def test_obtener_trayecto_partido_asistido_ida(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_ida", "20190622", "nacho", "I", 103, "Transporte", 103)

	trayecto=conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "I")

	assert trayecto[0]=="I"
	assert trayecto[1]=="Transporte"
	assert trayecto[2]=="Madrid"
	assert trayecto[3]!=trayecto[6]
	assert trayecto[4]!=trayecto[7]
	assert trayecto[5]=="Metropolitano"
	assert trayecto[8]=="transporte"
	assert trayecto[9]=="23"

def test_obtener_trayecto_partido_asistido_vuelta(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_vuelta", "20190622", "nacho", "V", 103, "Transporte Nacho", 103)

	trayecto=conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "V")

	assert trayecto[0]=="V"
	assert trayecto[1]=="Transporte Nacho"
	assert trayecto[2]=="Metropolitano"
	assert trayecto[3]!=trayecto[6]
	assert trayecto[4]!=trayecto[7]
	assert trayecto[5]=="Madrid"
	assert trayecto[8]=="23"
	assert trayecto[9]=="transporte_nacho"