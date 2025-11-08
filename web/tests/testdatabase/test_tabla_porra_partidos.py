import pytest

def test_tabla_porra_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM porra_partidos")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20200622", "nacho")]
)
def test_insertar_porra_partido_usuario(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido(f"{usuario}-{partido_id}", usuario, partido_id, 1, 0)

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

	conexion_entorno.insertarPorraPartido("nacho-20200622", "nacho", "20200622", 1, 0)

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

	conexion_entorno.insertarPorraPartido("nacho-20200622", "nacho", "20200622", 1, 0)

	porra_partido=conexion_entorno.obtenerPorraPartido("20200622", "nacho")

	assert porra_partido==(1, 0)

def test_obtener_porras_partido_no_existen(conexion):

	assert not conexion.obtenerPorrasPartido("20200622")

def test_obtener_porras_partido_no_existen_porras(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerPorrasPartido("20200622")

def test_obtener_porras_partido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho-20200622", "nacho", "20200622", 1, 0)

	porras_partido=conexion_entorno.obtenerPorrasPartido("20200622")

	assert len(porras_partido)==1

@pytest.mark.parametrize(["numero_porras"],
	[(2,),(5,),(13,),(22,)]
)
def test_obtener_porras_partido_varias(conexion_entorno, numero_porras):

	for numero in range(numero_porras):

		conexion_entorno.insertarUsuario(f"nacho_{numero}", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

		conexion_entorno.insertarPorraPartido(f"nacho_{numero}-20200622", f"nacho_{numero}", "20200622", 1, 0)

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

	conexion_entorno.insertarPorraPartido("nacho-20200622", "nacho", "20200622", 1, 0)

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

	conexion_entorno.insertarPorraPartido("nacho-20200622", "nacho", "20200622", 1, 0)

	assert not conexion_entorno.obtenerClasificacionPorras()

def test_obtener_clasificacion_porras(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO partidos
						VALUES('20190413', 'atletico-madrid', 'atletico-madrid', '2019-04-13', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.c.execute("""INSERT INTO partido_goleador
						VALUES('20190413', 'julian-alvarez', 1, 0, True)""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho-20190413", "nacho", "20190413", 1, 0)

	conexion_entorno.insertarGoleadorPorra("nacho-20190413", "julian-alvarez", 1, True)

	clasificacion=conexion_entorno.obtenerClasificacionPorras()

	assert clasificacion[0][0]=="nacho"
	assert clasificacion[0][3]==10
	assert clasificacion[0][4]==2
	assert clasificacion[0][3]+clasificacion[0][4]==clasificacion[0][5]

@pytest.mark.parametrize(["goles_local", "goles_visitante", "goleadores", "puntos_resultado", "puntos_goleadores"],
	[
		(2, 0, [("julian-alvarez", 2, True)], 5, 4),
		(2, 0, [("julian-alvarez", 1, True), ("grizzi", 1, True)], 5, 2),
		(1, 0, [("julian-alvarez", 1, True)], 3, 2),
		(1, 0, [("grizzi", 1, True)], 3, 0),
		(3, 1, [("julian-alvarez", 2, True), ("koke", 1, True), ("lautaro", 1, False)], 10, 8),
		(3, 1, [("julian-alvarez", 2, True), ("koke", 1, True), ("thuram", 1, False)], 10, 6),
		(3, 1, [("julian-alvarez", 2, True), ("grizzi", 1, True), ("thuram", 1, False)], 10, 4),
		(1, 1, [("julian-alvarez", 1, True), ("lautaro", 1, False)], 0, 4),
		(1, 1, [("julian-alvarez", 1, True), ("thuram", 1, False)], 0, 2),
		(1, 1, [("grizzi", 1, True), ("thuram", 1, False)], 0, 0),
		(1, 1, [("grizzi", 1, True), ("lautaro", 1, False)], 0, 2),
		(2, 2, [("grizzi", 2, True), ("lautaro", 2, False)], 0, 2),
		(0, 0, [], 0, 0),
		(0, 1, [("lautaro", 1, False)], 0, 2),
		(0, 1, [("thuram", 1, False)], 0, 0),
		(0, 2, [("lautaro", 2, False)], 0, 2),
		(0, 2, [("lautaro", 1, False), ("thuram", 1, False)], 0, 2)
	]
)
def test_obtener_clasificacion_porras_victoria(conexion_entorno, goles_local, goles_visitante, goleadores, puntos_resultado, puntos_goleadores):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('inter')""")

	conexion_entorno.c.execute("""INSERT INTO jugadores (Jugador_Id, Equipo_Id)
									VALUES('lautaro', 'inter'), ('koke', 'atletico-madrid'),
									('grizzi', 'atletico-madrid'), ('thuram', 'inter')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190413', 'atletico-madrid', 'inter', '2019-04-13', '22:00', 'Liga', '3-1', 'Victoria')""")

	conexion_entorno.c.execute("""INSERT INTO partido_goleador
								VALUES ('20190413', 'julian-alvarez', 1, 0, True), ('20190413', 'julian-alvarez', 2, 0, True),
								('20190413', 'koke', 22, 0, True), ('20190413', 'lautaro', 13, 0, False)""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho-20190413", "nacho", "20190413", goles_local, goles_visitante)

	for goleador, numero_goles, local in goleadores:

		conexion_entorno.insertarGoleadorPorra("nacho-20190413", goleador, numero_goles, local)

	clasificacion=conexion_entorno.obtenerClasificacionPorras()

	assert clasificacion[0][0]=="nacho"
	assert clasificacion[0][3]==puntos_resultado
	assert clasificacion[0][4]==puntos_goleadores
	assert clasificacion[0][3]+clasificacion[0][4]==clasificacion[0][5]

@pytest.mark.parametrize(["goles_local", "goles_visitante", "goleadores", "puntos_resultado", "puntos_goleadores"],
	[
		(2, 0, [("julian-alvarez", 2, True)], 0, 2),
		(2, 0, [("julian-alvarez", 1, True), ("grizzi", 1, True)], 0, 2),
		(1, 0, [("julian-alvarez", 1, True)], 0, 2),
		(1, 0, [("grizzi", 1, True)], 0, 0),
		(3, 1, [("julian-alvarez", 2, True), ("koke", 1, True), ("lautaro", 1, False)], 0, 4),
		(3, 1, [("julian-alvarez", 2, True), ("koke", 1, True), ("thuram", 1, False)], 0, 2),
		(3, 1, [("julian-alvarez", 2, True), ("grizzi", 1, True), ("thuram", 1, False)], 0, 2),
		(1, 1, [("julian-alvarez", 1, True), ("lautaro", 1, False)], 10, 4),
		(1, 1, [("julian-alvarez", 1, True), ("thuram", 1, False)], 10, 2),
		(1, 1, [("grizzi", 1, True), ("thuram", 1, False)], 10, 0),
		(1, 1, [("grizzi", 1, True), ("lautaro", 1, False)], 10, 2),
		(2, 2, [("grizzi", 2, True), ("lautaro", 2, False)], 5, 2),
		(0, 0, [], 5, 0),
		(0, 1, [("lautaro", 1, False)], 0, 2),
		(0, 1, [("thuram", 1, False)], 0, 0),
		(0, 2, [("lautaro", 2, False)], 0, 2),
		(0, 2, [("lautaro", 1, False), ("thuram", 1, False)], 0, 2)
	]
)
def test_obtener_clasificacion_porras_empate(conexion_entorno, goles_local, goles_visitante, goleadores, puntos_resultado, puntos_goleadores):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('inter')""")

	conexion_entorno.c.execute("""INSERT INTO jugadores (Jugador_Id, Equipo_Id)
									VALUES('lautaro', 'inter'), ('koke', 'atletico-madrid'),
									('grizzi', 'atletico-madrid'), ('thuram', 'inter')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190413', 'atletico-madrid', 'inter', '2019-04-13', '22:00', 'Liga', '1-1', 'Empate')""")

	conexion_entorno.c.execute("""INSERT INTO partido_goleador
								VALUES ('20190413', 'julian-alvarez', 1, 0, True), ('20190413', 'lautaro', 13, 0, False)""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPorraPartido("nacho-20190413", "nacho", "20190413", goles_local, goles_visitante)

	for goleador, numero_goles, local in goleadores:

		conexion_entorno.insertarGoleadorPorra("nacho-20190413", goleador, numero_goles, local)

	clasificacion=conexion_entorno.obtenerClasificacionPorras()

	assert clasificacion[0][0]=="nacho"
	assert clasificacion[0][3]==puntos_resultado
	assert clasificacion[0][4]==puntos_goleadores
	assert clasificacion[0][3]+clasificacion[0][4]==clasificacion[0][5]

@pytest.mark.parametrize(["datos_usuarios", "orden"],
	[
		(
			[("nacho", 2, 0, [("julian-alvarez", 2, True)])],
			[("nacho", 9)]
		),
		(
			[("nacho", 2, 0, [("julian-alvarez", 2, True)]),
			("amanda", 1, 0, [("julian-alvarez", 1, True)])],
			[("nacho", 9), ("amanda", 5)]
		),
		(
			[("nacho", 1, 0, [("grizzi", 1, True)]),
			("amanda", 1, 0, [("julian-alvarez", 1, True)])],
			[("amanda", 5), ("nacho", 3)]
		),
		(
			[("nacho", 1, 1, [("grizzi", 1, True), ("lautaro", 1, False)]),
			("amanda", 1, 0, [("julian-alvarez", 1, True)]),
			("cuca", 3, 1, [("julian-alvarez", 2, True), ("grizzi", 1, True), ("thuram", 1, False)])],
			[("cuca", 14), ("amanda", 5), ("nacho", 2)]
		),
		(
			[("nacho", 1, 1, [("grizzi", 1, True), ("lautaro", 1, False)]),
			("amanda", 1, 0, [("julian-alvarez", 1, True)]),
			("cuca", 3, 1, [("julian-alvarez", 2, True), ("grizzi", 1, True), ("thuram", 1, False)]),
			("baby", 2, 1, [("julian-alvarez", 2, True), ("thuram", 1, False)])],
			[("cuca", 14), ("baby", 7), ("amanda", 5), ("nacho", 2)]
		),
		(
			[("nacho", 1, 1, [("grizzi", 1, True), ("lautaro", 1, False)]),
			("amanda", 1, 0, [("julian-alvarez", 1, True)]),
			("cuca", 3, 1, [("julian-alvarez", 2, True), ("grizzi", 1, True), ("thuram", 1, False)]),
			("baby", 2, 1, [("julian-alvarez", 2, True), ("thuram", 1, False)]),
			("user", 0, 2, [("thuram", 2, False)])],
			[("cuca", 14), ("baby", 7), ("amanda", 5), ("nacho", 2), ("user", 0)]
		)
	]
)
def test_obtener_clasificacion_porras_varios(conexion_entorno, datos_usuarios, orden):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('inter')""")

	conexion_entorno.c.execute("""INSERT INTO jugadores (Jugador_Id, Equipo_Id)
									VALUES('lautaro', 'inter'), ('koke', 'atletico-madrid'),
									('grizzi', 'atletico-madrid'), ('thuram', 'inter')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190413', 'atletico-madrid', 'inter', '2019-04-13', '22:00', 'Liga', '3-1', 'Empate')""")

	conexion_entorno.c.execute("""INSERT INTO partido_goleador
								VALUES ('20190413', 'julian-alvarez', 1, 0, True), ('20190413', 'julian-alvarez', 2, 0, True),
								('20190413', 'koke', 22, 0, True), ('20190413', 'lautaro', 13, 0, False)""")

	conexion_entorno.confirmar()

	for usuario, goles_local, goles_visitante, goleadores in datos_usuarios:

		conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", usuario, "dorado", "1998-02-16", 103, "atletico-madrid")

		conexion_entorno.insertarPorraPartido(f"{usuario}-20190413", usuario, "20190413", goles_local, goles_visitante)

		for goleador, numero_goles, local in goleadores:

			conexion_entorno.insertarGoleadorPorra(f"{usuario}-20190413", goleador, numero_goles, local)

	clasificacion=conexion_entorno.obtenerClasificacionPorras()

	for o, c in zip(orden, clasificacion):

		assert o[0]==c[0]
		assert o[1]==c[5]