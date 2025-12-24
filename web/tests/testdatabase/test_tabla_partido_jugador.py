def test_tabla_partido_jugador_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_jugador")

	assert not conexion.c.fetchall()

def test_obtener_partido_jugadores_no_existen(conexion):

	assert not conexion.obtenerJugadoresEquipoPartido("20190622", True)

def test_obtener_partido_jugadores_no_titular(conexion_entorno):

	conexion_entorno.c.execute("UPDATE partido_jugador SET Titular=False")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerJugadoresEquipoPartido("20190622", True)

def test_obtener_partido_jugadores_local(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO jugadores
							VALUES('nacho', 'Julian', 'atletico-madrid', 'ar', '1324', 100, 100.0, 9, 'DC')""")

	conexion_entorno.c.execute("""INSERT INTO partido_jugador
				VALUES('20190622', 'nacho', 9, 10.0, True, False, 1)""")

	conexion_entorno.confirmar()

	jugadores=conexion_entorno.obtenerJugadoresEquipoPartido("20190622", True)

	assert len(jugadores)==1
	assert "julian-alvarez" in jugadores[0]
	assert "nacho" not in jugadores[0]

def test_obtener_partido_jugadores_visitante(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO jugadores
							VALUES('nacho', 'Julian', 'atletico-madrid', 'ar', '1324', 100, 100.0, 9, 'DC')""")

	conexion_entorno.c.execute("""INSERT INTO partido_jugador
				VALUES('20190622', 'nacho', 9, 10.0, True, False, 1)""")

	conexion_entorno.confirmar()

	jugadores=conexion_entorno.obtenerJugadoresEquipoPartido("20190622", False)

	assert len(jugadores)==1
	assert "julian-alvarez" not in jugadores[0]
	assert "nacho" in jugadores[0]