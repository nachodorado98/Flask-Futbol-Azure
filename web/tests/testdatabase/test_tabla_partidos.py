def test_tabla_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM partidos")

	assert not conexion.c.fetchall()

def test_obtener_partidos_equipo_no_existe_equipo(conexion):

	assert not conexion.obtenerPartidosEquipo("atletico-madrid")

def test_obtener_partidos_equipo_no_existe_partido(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerPartidosEquipo("atletico-madrid")

def test_obtener_partidos_equipo(conexion_entorno):

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	assert len(partidos)==1

def test_obtener_partidos_equipo_local(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos VALUES('2', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	assert len(partidos)==2

def test_obtener_partidos_equipo_visitante(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos VALUES('2', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	assert len(partidos)==2

def test_obtener_partidos_equipo_varios_partidos(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero in range(2,10):

		conexion_entorno.c.execute(f"""INSERT INTO partidos VALUES('{numero}', 'rival', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	assert len(partidos)==1

def test_obtener_partidos_equipo_equipo_diferente(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos VALUES('2', 'rival', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerPartidosEquipo("atleti-madrid")