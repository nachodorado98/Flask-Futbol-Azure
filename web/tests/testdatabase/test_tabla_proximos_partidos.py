def test_tabla_proximos_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()

def test_obtener_proximos_partidos_equipo_no_existe_equipo(conexion):

	assert not conexion.obtenerProximosPartidosEquipo("atletico-madrid", 5)

def test_obtener_proximos_partidos_equipo_no_existe_partido(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerProximosPartidosEquipo("atletico-madrid", 5)

def test_obtener_proximos_partidos_equipo(conexion_entorno):

	proximos_partidos=conexion_entorno.obtenerProximosPartidosEquipo("atletico-madrid", 5)

	assert len(proximos_partidos)==1