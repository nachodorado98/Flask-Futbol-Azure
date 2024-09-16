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

def test_obtener_partidos_no_asistidos_usuario_partido_equipos_no_existen(conexion_entorno):

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

def test_ultima_fecha_partidos_asistidos_no_existen_partidos(conexion):

	assert not conexion.ultima_fecha_partido_asistido("nacho")

def test_ultima_fecha_partidos_asistidos_no_existen_partidos_asistidos(conexion_entorno):

	assert not conexion_entorno.ultima_fecha_partido_asistido("nacho")

def test_ultima_fecha_partidos_asistidos_partido_asistido_sin_fecha(conexion_entorno):

	conexion_entorno.c.execute("UPDATE partidos SET fecha=NULL")

	conexion_entorno.confirmar()

	assert not conexion_entorno.ultima_fecha_partido_asistido("nacho")

def test_ultima_fecha_partidos_asistidos(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho")

	fecha=conexion_entorno.ultima_fecha_partido_asistido("nacho")

	assert fecha=="2019-06-22"

@pytest.mark.parametrize(["fechas", "fecha_mas_reciente"],
	[
		(["2019-06-23", "2010-11-22", "2024-06-22", "2020-01-01", "2019-04-13"], "2024-06-22"),
		(["2019-06-23", "2010-11-22", "2017-06-22", "2020-01-01", "2019-04-13"], "2020-01-01"),
		(["2025-06-23", "2010-11-22", "2024-06-22", "2020-01-01", "2019-04-13"], "2025-06-23"),
		(["2019-06-23", "2110-11-22", "2024-06-22", "2020-01-01", "2019-04-13"], "2110-11-22"),
		(["2019-06-23", "2010-11-22", "2024-06-22", "2020-01-01", "2029-04-13"], "2029-04-13")
	]
)
def test_ultima_fecha_partidos_asistidos_varios(conexion_entorno, fechas, fecha_mas_reciente):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero, fecha in enumerate(fechas):

		conexion_entorno.c.execute(f"""INSERT INTO partidos
										VALUES('20190622{numero}', 'atletico-madrid', 'atletico-madrid', '{fecha}', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.confirmar()

		conexion_entorno.insertarPartidoAsistido(f"20190622{numero}", "nacho")

	fecha=conexion_entorno.ultima_fecha_partido_asistido("nacho")

	assert fecha==fecha_mas_reciente

def test_obtener_partidos_no_asistidos_usuario_recientes_no_existen_partidos(conexion):

	assert not conexion.obtenerPartidosNoAsistidosUsuarioRecientes("nacho", "atletico-madrid")

def test_obtener_partidos_no_asistidos_usuario_recientes_partido_equipos_no_existen(conexion_entorno):

	assert not conexion_entorno.obtenerPartidosNoAsistidosUsuarioRecientes("nacho", "atleti")

def test_obtener_partidos_no_asistidos_usuario_recientes(conexion_entorno):

	partidos=conexion_entorno.obtenerPartidosNoAsistidosUsuarioRecientes("nacho", "atletico-madrid")

	assert len(partidos)==1

def test_obtener_partidos_no_asistidos_usuario_recientes_varios(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria'),
										('2019063543', 'atletico-madrid', 'atletico-madrid', '2020-12-23', '22:00', 'Liga', '1-0', 'Victoria'),
										('46547568', 'atletico-madrid', 'atletico-madrid', '2010-07-03', '22:00', 'Liga', '1-0', 'Victoria'),
										('46358h2h', 'atletico-madrid', 'atletico-madrid', '2020-07-03', '22:00', 'Liga', '1-0', 'Victoria'),
										('dsgfd686', 'atletico-madrid', 'atletico-madrid', '2000-10-12', '22:00', 'Liga', '1-0', 'Victoria'),
										('456673kh', 'atletico-madrid', 'atletico-madrid', '2025-07-09', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosNoAsistidosUsuarioRecientes("nacho", "atletico-madrid")

	assert len(partidos)==7

def test_obtener_partidos_no_asistidos_usuario_recientes_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerPartidosNoAsistidosUsuarioRecientes("nacho", "atletico-madrid")

@pytest.mark.parametrize(["partido_id", "numero_partidos"],
	[("20190623", 3), ("456673kh", 0), ("20190622", 4),("46547568", 5), ("dsgfd686", 6)]
)
def test_obtener_partidos_no_asistidos_usuario_recientes_partido_asistido_fecha_reciente(conexion_entorno, partido_id, numero_partidos):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria'),
										('2019063543', 'atletico-madrid', 'atletico-madrid', '2020-12-23', '22:00', 'Liga', '1-0', 'Victoria'),
										('46547568', 'atletico-madrid', 'atletico-madrid', '2010-07-03', '22:00', 'Liga', '1-0', 'Victoria'),
										('46358h2h', 'atletico-madrid', 'atletico-madrid', '2020-07-03', '22:00', 'Liga', '1-0', 'Victoria'),
										('dsgfd686', 'atletico-madrid', 'atletico-madrid', '2000-10-12', '22:00', 'Liga', '1-0', 'Victoria'),
										('456673kh', 'atletico-madrid', 'atletico-madrid', '2025-07-09', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido(partido_id, "nacho")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosNoAsistidosUsuarioRecientes("nacho", "atletico-madrid")

	assert len(partidos)==numero_partidos

def test_obtener_partidos_no_asistidos_usuario_recientes_partido_asistido_otro_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarUsuario("otro", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "otro")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosNoAsistidosUsuario("nacho", "atletico-madrid")

	assert len(partidos)==1

def test_obtener_partidos_no_asistidos_usuario_recientes_partido_asistido_fecha_reciente_otro_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarUsuario("otro", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria'),
										('2019063543', 'atletico-madrid', 'atletico-madrid', '2020-12-23', '22:00', 'Liga', '1-0', 'Victoria'),
										('46547568', 'atletico-madrid', 'atletico-madrid', '2010-07-03', '22:00', 'Liga', '1-0', 'Victoria'),
										('46358h2h', 'atletico-madrid', 'atletico-madrid', '2020-07-03', '22:00', 'Liga', '1-0', 'Victoria'),
										('dsgfd686', 'atletico-madrid', 'atletico-madrid', '2000-10-12', '22:00', 'Liga', '1-0', 'Victoria'),
										('456673kh', 'atletico-madrid', 'atletico-madrid', '2025-07-09', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido("46358h2h", "otro")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosNoAsistidosUsuarioRecientes("nacho", "atletico-madrid")

	assert len(partidos)==7

def test_obtener_partidos_asistidos_usuario_no_existe_usuario(conexion):

	assert not conexion.obtenerPartidosAsistidosUsuario("nacho")

def test_obtener_partidos_asistidos_usuario_no_existen(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

def test_obtener_partidos_asistidos_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho")

	conexion_entorno.confirmar()

	assert conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")