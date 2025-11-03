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

def test_obtener_porras_partido_no_existen(conexion):

	assert not conexion.obtenerPorrasPartido("20200622")

def test_obtener_porras_partido_no_existen_porras(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerPorrasPartido("20200622")

def test_obtener_porras_partido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho", "20200622", 1, 0)

	porras_partido=conexion_entorno.obtenerPorrasPartido("20200622")

	assert len(porras_partido)==1

@pytest.mark.parametrize(["numero_porras"],
	[(2,),(5,),(13,),(22,)]
)
def test_obtener_porras_partido_varias(conexion_entorno, numero_porras):

	for numero in range(numero_porras):

		conexion_entorno.insertarUsuario(f"nacho_{numero}", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

		conexion_entorno.insertarPorraPartido(f"nacho_{numero}", "20200622", 1, 0)

	porras_partido=conexion_entorno.obtenerPorrasPartido("20200622")

	assert len(porras_partido)==numero_porras

def test_eliminar_porra_partido_no_existen(conexion):

	assert not conexion.obtenerPorrasPartido("20200622")

	conexion.eliminarPorraPartido("20200622", "nacho")

	assert not conexion.obtenerPorrasPartido("20200622")

def test_eliminar_porra_partido_asistido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerPorrasPartido("20200622")

	conexion_entorno.eliminarPorraPartido("20200622", "otro")

	assert not conexion_entorno.obtenerPorrasPartido("20200622")

def test_eliminar_porra_partido_no_existe_porra(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerPorrasPartido("20200622")

	conexion_entorno.eliminarPorraPartido("20200622", "nacho")

	assert not conexion_entorno.obtenerPorrasPartido("20200622")

def test_eliminar_porra_partido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho", "20200622", 1, 0)

	assert conexion_entorno.obtenerPorrasPartido("20200622")

	conexion_entorno.eliminarPorraPartido("20200622", "nacho")

	assert not conexion_entorno.obtenerPorrasPartido("20200622")

def test_obtener_clasificacion_porras_no_existen(conexion):

	assert not conexion.obtenerClasificacionPorras()

def test_obtener_clasificacion_porras_no_existen_porras(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerClasificacionPorras()

def test_obtener_clasificacion_porras_aun_no_jugado(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho", "20200622", 1, 0)

	assert not conexion_entorno.obtenerClasificacionPorras()

def test_obtener_clasificacion_porras_un_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho", "20190622", 1, 0)

	clasificacion=conexion_entorno.obtenerClasificacionPorras()

	assert clasificacion[0][0]=="nacho"
	assert clasificacion[0][3]==10

@pytest.mark.parametrize(["datos"],
	[
		([("nacho", 1, 0, 10)],),
		([("nacho", 1, 0, 10), ("amanda", 2, 0, 4)],),
		([("nacho", 1, 0, 10), ("amanda", 2, 0, 4), ("cuca", 0, 0, 0)],),
		([("nacho", 1, 0, 10), ("amanda", 2, 1, 4), ("baby", 0, 1, 0), ("cuca", 0, 0, 0)],),
		([("amanda", 2, 1, 4), ("nacho", 5, 0, 4), ("baby", 0, 1, 0), ("cuca", 0, 0, 0)],)
	]
)
def test_obtener_clasificacion_porras_varios_usuarios(conexion_entorno, datos):

	for nombre, local, visitante, puntos in datos:

		conexion_entorno.insertarUsuario(nombre, "micorreo@correo.es", "1234", nombre, "dorado", "1998-02-16", 103, "atletico-madrid")

		conexion_entorno.insertarPorraPartido(nombre, "20190622", local, visitante)

	clasificacion=conexion_entorno.obtenerClasificacionPorras()

	for d, c in zip(datos, clasificacion):

		assert d[0]==c[0]
		assert d[-1]==c[-1]