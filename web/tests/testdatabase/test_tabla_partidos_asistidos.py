import pytest

def test_tabla_partidos_asistidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM partidos_asistidos")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20190622", "nacho")]
)
def test_insertar_partido_usuario(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido(partido_id, usuario, "comentario")

	conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

	partidos_asistidos=conexion_entorno.c.fetchall()

	assert len(partidos_asistidos)==1

def test_existe_partido_asistido_no_existen(conexion):

	assert not conexion.existe_partido_asistido("20190622", "nacho")

def test_existe_partido_asistido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.existe_partido_asistido("20190622", "otro")

def test_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

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

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.obtenerPartidosNoAsistidosUsuario("nacho", "atletico-madrid")

def test_obtener_partidos_no_asistidos_usuario_partido_asistido_otro_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarUsuario("otro", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "otro", "comentario")

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

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

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

		conexion_entorno.insertarPartidoAsistido(f"20190622{numero}", "nacho", "comentario")

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

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

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

	conexion_entorno.insertarPartidoAsistido(partido_id, "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosNoAsistidosUsuarioRecientes("nacho", "atletico-madrid")

	assert len(partidos)==numero_partidos

def test_obtener_partidos_no_asistidos_usuario_recientes_partido_asistido_otro_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarUsuario("otro", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "otro", "comentario")

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

	conexion_entorno.insertarPartidoAsistido("46358h2h", "otro", "comentario")

	partidos=conexion_entorno.obtenerPartidosNoAsistidosUsuarioRecientes("nacho", "atletico-madrid")

	assert len(partidos)==7

def test_obtener_partidos_asistidos_usuario_no_existe_usuario(conexion):

	assert not conexion.obtenerPartidosAsistidosUsuario("nacho")

def test_obtener_partidos_asistidos_usuario_no_existen(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

def test_obtener_partidos_asistidos_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

def test_obtener_partidos_asistidos_usuario_ganado(conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('1', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria Visitante')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("1", "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	assert partidos[0][-1]==0
	assert partidos[0][-2]==0
	assert partidos[0][-3]==1

@pytest.mark.parametrize(["resultados", "ganados"],
	[
		(["Victoria Visitante", "Victoria Penaltis Visitante", "Victoria Visitante", "Victoria Local"], 1),
		(["Visitante", "Victoria Penaltis Local", "Victoria Visitante", "Local"], 2),
		(["Victoria Local", "Victoria Penaltis Local", "Local", "Local Victoria"], 4),
		(["Victoria", "Victoria Visitante Panaltis", "Victoria Visitante", "Empate"], 0)
	]
)
def test_obtener_partidos_asistidos_usuario_ganados_local(conexion_entorno, resultados, ganados):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', %s)""",
									(numero+1, resultado))

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.insertarPartidoAsistido(numero+1, "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	partidos_ganados=list(filter(lambda partido: partido[-3]==1, partidos))

	partidos_no_ganados=list(filter(lambda partido: partido[-3]==0, partidos))

	assert len(partidos_ganados)==ganados
	assert len(partidos)==len(partidos_ganados)+len(partidos_no_ganados)

@pytest.mark.parametrize(["resultados", "ganados"],
	[
		(["Victoria Visitante", "Victoria Penaltis Visitante", "Victoria Visitante", "Victoria Local"], 3),
		(["Visitante", "Victoria Penaltis Local", "Victoria Visitante", "Victoria Local"], 2),
		(["Victoria Visitante", "Victoria Penaltis Visitante", "Victoria Visitante", "Visitante Victoria"], 4),
		(["Victoria", "Victoria Local Panaltis", "Victoria Local", "Empate"], 0)
	]
)
def test_obtener_partidos_asistidos_usuario_ganados_visitante(conexion_entorno, resultados, ganados):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', %s)""",
									(numero+1, resultado))

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.insertarPartidoAsistido(numero+1, "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	partidos_ganados=list(filter(lambda partido: partido[-3]==1, partidos))

	partidos_no_ganados=list(filter(lambda partido: partido[-3]==0, partidos))

	assert len(partidos_ganados)==ganados
	assert len(partidos)==len(partidos_ganados)+len(partidos_no_ganados)

def test_obtener_partidos_asistidos_usuario_perdido(conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('1', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria Local')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("1", "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	assert partidos[0][-1]==0
	assert partidos[0][-2]==1
	assert partidos[0][-3]==0

@pytest.mark.parametrize(["resultados", "perdidos"],
	[
		(["Victoria Visitante", "Victoria Penaltis Visitante", "Victoria Visitante", "Victoria Local"], 3),
		(["Visitante", "Victoria Penaltis Local", "Victoria Visitante", "Local"], 2),
		(["Victoria Local", "Victoria Penaltis Local", "Local", "Local Victoria"], 0),
		(["Victoria", "Victoria Visitante Panaltis", "Victoria Visitante", "Empate"], 2)
	]
)
def test_obtener_partidos_asistidos_usuario_perdidos_local(conexion_entorno, resultados, perdidos):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', %s)""",
									(numero+1, resultado))

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.insertarPartidoAsistido(numero+1, "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	partidos_perdidos=list(filter(lambda partido: partido[-2]==1, partidos))

	partidos_no_perdidos=list(filter(lambda partido: partido[-2]==0, partidos))

	assert len(partidos_perdidos)==perdidos
	assert len(partidos)==len(partidos_perdidos)+len(partidos_no_perdidos)

@pytest.mark.parametrize(["resultados", "perdidos"],
	[
		(["Victoria Visitante", "Victoria Penaltis Visitante", "Victoria Visitante", "Victoria Local"], 1),
		(["Visitante", "Victoria Penaltis Local", "Victoria Visitante", "Victoria Local"], 2),
		(["Victoria Visitante", "Victoria Penaltis Visitante", "Victoria Visitante", "Visitante Victoria"], 0),
		(["Victoria", "Victoria Local Panaltis", "Victoria Local", "Empate"], 2)
	]
)
def test_obtener_partidos_asistidos_usuario_perdidos_visitante(conexion_entorno, resultados, perdidos):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', %s)""",
									(numero+1, resultado))

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.insertarPartidoAsistido(numero+1, "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	partidos_perdidos=list(filter(lambda partido: partido[-2]==1, partidos))

	partidos_no_perdidos=list(filter(lambda partido: partido[-2]==0, partidos))

	assert len(partidos_perdidos)==perdidos
	assert len(partidos)==len(partidos_perdidos)+len(partidos_no_perdidos)

def test_obtener_partidos_asistidos_usuario_empatado(conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('1', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Empate')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("1", "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	assert partidos[0][-1]==1
	assert partidos[0][-2]==0
	assert partidos[0][-3]==0

@pytest.mark.parametrize(["resultados", "empatados"],
	[
		(["Victoria Visitante", "Empate", "Victoria Visitante", "Empate A Dos"], 2),
		(["Visitante", "Victoria Penaltis Local", "Victoria Visitante", "Empate"], 1),
		(["Victoria Local", "Victoria Penaltis Local", "Local", "Local Victoria"], 0),
		(["Victoria Empate", "Victoria Empate Panaltis", "Victoria Visitante", "Empate"], 3)
	]
)
def test_obtener_partidos_asistidos_usuario_empatados_local(conexion_entorno, resultados, empatados):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', %s)""",
									(numero+1, resultado))

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.insertarPartidoAsistido(numero+1, "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	partidos_empatados=list(filter(lambda partido: partido[-1]==1, partidos))

	partidos_no_empatados=list(filter(lambda partido: partido[-1]==0, partidos))

	assert len(partidos_empatados)==empatados
	assert len(partidos)==len(partidos_empatados)+len(partidos_no_empatados)

@pytest.mark.parametrize(["resultados", "empatados"],
	[
		(["Victoria Visitante", "Empate", "Victoria Visitante", "Empate A Dos"], 2),
		(["Visitante", "Victoria Penaltis Local", "Victoria Visitante", "Empate"], 1),
		(["Victoria Local", "Victoria Penaltis Local", "Local", "Local Victoria"], 0),
		(["Victoria Empate", "Victoria Empate Panaltis", "Victoria Visitante", "Empate"], 3)
	]
)
def test_obtener_partidos_asistidos_usuario_empatados_visitante(conexion_entorno, resultados, empatados):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', %s)""",
									(numero+1, resultado))

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.insertarPartidoAsistido(numero+1, "nacho", "comentario")

	partidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	partidos_empatados=list(filter(lambda partido: partido[-1]==1, partidos))

	partidos_no_empatados=list(filter(lambda partido: partido[-1]==0, partidos))

	assert len(partidos_empatados)==empatados
	assert len(partidos)==len(partidos_empatados)+len(partidos_no_empatados)

def test_obtener_estadio_partido_asistido_fecha_no_existe_usuario(conexion):

	assert not conexion.obtenerEstadiosPartidosAsistidosUsuarioFecha("nacho", 5)

def test_obtener_estadio_partido_asistido_fecha_no_existen_partidos(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioFecha("nacho", 5)

def test_obtener_estadio_partido_asistido_fecha(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido(f"20190622", "nacho", "comentario")

	estadios=conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioFecha("nacho", 5)

	assert len(estadios)==1

def test_obtener_estadio_partido_asistido_fecha_otro_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarUsuario("otro", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido(f"20190622", "otro", "comentario")

	assert not conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioFecha("nacho", 5)

def test_obtener_estadio_partido_asistido_fecha_varios(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero in range(1,21):

		conexion_entorno.c.execute(f"""INSERT INTO equipos (Equipo_Id) VALUES('equipo{numero}')""")

		conexion_entorno.c.execute(f"""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio{numero}', 10000)""")

		conexion_entorno.c.execute(f"""INSERT INTO equipo_estadio VALUES('equipo{numero}', 'estadio{numero}')""")

		conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190623{numero}', 'equipo{numero}', 'atletico-madrid', '20{numero}-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.c.execute(f"""INSERT INTO partido_estadio VALUES('20190623{numero}', 'estadio{numero}')""")

		conexion_entorno.insertarPartidoAsistido(f"20190623{numero}", "nacho", "comentario")

	conexion_entorno.confirmar()

	partidos_asistidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	estadios=conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioFecha("nacho", 5)

	assert len(partidos_asistidos)==20
	assert len(estadios)==5
	assert estadios[0][-1]>estadios[-1][-1]

def test_obtener_estadio_partido_asistido_fecha_mismo_varias_veces(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero in range(1,21):

		conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190623{numero}', 'atletico-madrid', 'atletico-madrid', '20{numero}-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.c.execute(f"""INSERT INTO partido_estadio VALUES('20190623{numero}', 'metropolitano')""")

		conexion_entorno.insertarPartidoAsistido(f"20190623{numero}", "nacho", "comentario")

	conexion_entorno.confirmar()

	partidos_asistidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	estadios=conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioFecha("nacho", 5)

	assert len(partidos_asistidos)==20
	assert len(estadios)==1

def test_obtener_estadio_partido_asistido_cantidad_no_existe_usuario(conexion):

	assert not conexion.obtenerEstadiosPartidosAsistidosUsuarioCantidad("nacho", 5)

def test_obtener_estadio_partido_asistido_cantidad_no_existen_partidos(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioCantidad("nacho", 5)

def test_obtener_estadio_partido_asistido_cantidad(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido(f"20190622", "nacho", "comentario")

	estadios=conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioCantidad("nacho", 5)

	assert len(estadios)==1
	assert estadios[0][-1]==1

def test_obtener_estadio_partido_asistido_cantidad_otro_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarUsuario("otro", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido(f"20190622", "otro", "comentario")

	assert not conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioCantidad("nacho", 5)

def test_obtener_estadio_partido_asistido_cantidad_varios(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero in range(1,21):

		conexion_entorno.c.execute(f"""INSERT INTO equipos (Equipo_Id) VALUES('equipo{numero}')""")

		conexion_entorno.c.execute(f"""INSERT INTO estadios (Estadio_Id, Capacidad) VALUES('estadio{numero}', 10000)""")

		conexion_entorno.c.execute(f"""INSERT INTO equipo_estadio VALUES('equipo{numero}', 'estadio{numero}')""")

		conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190623{numero}', 'equipo{numero}', 'atletico-madrid', '20{numero}-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.c.execute(f"""INSERT INTO partido_estadio VALUES('20190623{numero}', 'estadio{numero}')""")

		conexion_entorno.insertarPartidoAsistido(f"20190623{numero}", "nacho", "comentario")

	conexion_entorno.confirmar()

	partidos_asistidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	estadios=conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioCantidad("nacho", 5)

	assert len(partidos_asistidos)==20
	assert len(estadios)==5
	assert estadios[0][-1]==1

def test_obtener_estadio_partido_asistido_cantidad_mismo_varias_veces(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	for numero in range(1,21):

		conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('20190623{numero}', 'atletico-madrid', 'atletico-madrid', '20{numero}-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.c.execute(f"""INSERT INTO partido_estadio VALUES('20190623{numero}', 'metropolitano')""")

		conexion_entorno.insertarPartidoAsistido(f"20190623{numero}", "nacho", "comentario")

	conexion_entorno.confirmar()

	partidos_asistidos=conexion_entorno.obtenerPartidosAsistidosUsuario("nacho")

	estadios=conexion_entorno.obtenerEstadiosPartidosAsistidosUsuarioCantidad("nacho", 5)

	assert len(partidos_asistidos)==20
	assert len(estadios)==1
	assert estadios[0][-1]==20

def test_obtener_partido_asistido_usuario_no_existe_usuario(conexion):

	assert not conexion.obtenerPartidoAsistidoUsuario("nacho", "20190622")

def test_obtener_partido_asistido_usuario_no_existe_partido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuario("nacho", "20190623")

def test_obtener_partido_asistido_usuario_partido_no_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuario("nacho", "20190622")

def test_obtener_partido_asistido_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	partido_asistido=conexion_entorno.obtenerPartidoAsistidoUsuario("nacho", "20190622")

	assert partido_asistido[0]=="20190622-nacho"
	assert partido_asistido[1]=="20190622"

def test_obtener_partido_asistido_usuario_siguiente_no_existe_usuario(conexion):

	assert not conexion.obtenerPartidoAsistidoUsuarioSiguiente("nacho", "20190622")

def test_obtener_partido_asistido_usuario_siguiente_no_existe_partido(conexion_entorno):

	conexion_entorno.c.execute("""DELETE FROM partidos""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuarioSiguiente("nacho", "20190622")

def test_obtener_partido_asistido_usuario_siguiente_no_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuarioSiguiente("nacho", "20190622")

def test_obtener_partido_asistido_usuario_siguiente_existe_uno_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuarioSiguiente("nacho", "20190622")

def test_obtener_partido_asistido_usuario_siguiente_existe_anterior(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190621', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido("20190621", "nacho", "comentario")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuarioSiguiente("nacho", "20190622")

def test_obtener_partido_asistido_usuario_siguiente(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido("20190623", "nacho", "comentario")

	partido_id=conexion_entorno.obtenerPartidoAsistidoUsuarioSiguiente("nacho", "20190622")

	assert partido_id=="20190623"

@pytest.mark.parametrize(["data", "partido_id_siguiente"],
	[
		([("667658", "2019-02-19"),("664657658", "2019-06-19"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "20197658"),
		([("667658", "2019-06-23"),("664657658", "2019-06-19"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "667658"),
		([("667658", "2019-02-19"),("664657658", "2019-06-25"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "664657658"),
		([("667658", "2019-02-19"),("664657658", "2019-06-19"),("20197658", "2019-07-19"),("661357658", "2019-07-18")], "661357658")
	]
)
def test_obtener_partido_asistido_usuario_siguiente_varios(conexion_entorno, data, partido_id_siguiente):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	for partido_id, fecha in data:

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'atletico-madrid', 'atletico-madrid', %s, '22:00', 'Liga', '1-0', 'Victoria')""",
									(partido_id, fecha))

		conexion_entorno.confirmar()

		conexion_entorno.insertarPartidoAsistido(partido_id, "nacho", "comentario")

	partido_id=conexion_entorno.obtenerPartidoAsistidoUsuarioSiguiente("nacho", "20190622")

	assert partido_id==partido_id_siguiente

def test_obtener_partido_asistido_usuario_anterior_no_existe_usuario(conexion):

	assert not conexion.obtenerPartidoAsistidoUsuarioAnterior("nacho", "20190622")

def test_obtener_partido_asistido_usuario_anterior_no_existe_partido(conexion_entorno):

	conexion_entorno.c.execute("""DELETE FROM partidos""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuarioAnterior("nacho", "20190622")

def test_obtener_partido_asistido_usuario_anterior_no_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuarioAnterior("nacho", "20190622")

def test_obtener_partido_asistido_usuario_anterior_existe_uno_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuarioAnterior("nacho", "20190622")

def test_obtener_partido_asistido_usuario_anterior_existe_siguiente(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido("20190623", "nacho", "comentario")

	assert not conexion_entorno.obtenerPartidoAsistidoUsuarioAnterior("nacho", "20190622")

def test_obtener_partido_asistido_usuario_anterior(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190621', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarPartidoAsistido("20190621", "nacho", "comentario")

	partido_id=conexion_entorno.obtenerPartidoAsistidoUsuarioAnterior("nacho", "20190622")

	assert partido_id=="20190621"

@pytest.mark.parametrize(["data", "partido_id_anterior"],
	[
		([("667658", "2019-02-19"),("664657658", "2019-05-19"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "664657658"),
		([("667658", "2019-06-19"),("664657658", "2019-05-19"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "667658"),
		([("667658", "2019-02-19"),("664657658", "2019-05-19"),("20197658", "2019-05-20"),("661357658", "2019-12-19")], "20197658"),
		([("667658", "2019-02-19"),("664657658", "2019-05-19"),("20197658", "2019-07-19"),("661357658", "2019-06-13")], "661357658")
	]
)
def test_obtener_partido_asistido_usuario_anterior_varios(conexion_entorno, data, partido_id_anterior):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	for partido_id, fecha in data:

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'atletico-madrid', 'atletico-madrid', %s, '22:00', 'Liga', '1-0', 'Victoria')""",
									(partido_id, fecha))

		conexion_entorno.confirmar()

		conexion_entorno.insertarPartidoAsistido(partido_id, "nacho", "comentario")

	partido_id=conexion_entorno.obtenerPartidoAsistidoUsuarioAnterior("nacho", "20190622")

	assert partido_id==partido_id_anterior

def test_actualizar_comentario_partido_asistido_no_existe_partido(conexion):

	assert not conexion.existe_partido("20190622")

	conexion.actualizarComentarioPartidoAsistido("20190622", "nacho", "nuevo comentario")

	assert not conexion.existe_partido("20190622")

def test_actualizar_comentario_partido_asistido_no_existe_usuario(conexion_entorno):

	assert not conexion_entorno.existe_usuario("nacho")

	conexion_entorno.actualizarComentarioPartidoAsistido("20190622", "nacho", "nuevo comentario")

	assert not conexion_entorno.existe_usuario("nacho")

def test_actualizar_comentario_partido_asistido_no_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	assert not conexion_entorno.existe_partido_asistido("20190622", "nacho")

	conexion_entorno.actualizarComentarioPartidoAsistido("20190622", "nacho", "nuevo comentario")

	assert not conexion_entorno.existe_partido_asistido("20190622", "nacho")

def test_actualizar_comentario_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert conexion_entorno.existe_partido_asistido("20190622", "nacho")

	conexion_entorno.c.execute("SELECT Comentario FROM partidos_asistidos")

	comentario=conexion_entorno.c.fetchone()["comentario"]

	assert comentario=="comentario"

	conexion_entorno.actualizarComentarioPartidoAsistido("20190622", "nacho", "nuevo comentario")

	assert conexion_entorno.existe_partido_asistido("20190622", "nacho")

	conexion_entorno.c.execute("SELECT Comentario FROM partidos_asistidos")

	nuevo_comentario=conexion_entorno.c.fetchone()["comentario"]

	assert nuevo_comentario=="nuevo comentario"