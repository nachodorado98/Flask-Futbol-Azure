def test_tabla_partido_jugador_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_jugador")

	assert not conexion.c.fetchall()

def test_insertar_partido_jugador(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarJugador("nacho")

	conexion.insertarPartidoJugador(("1", "nacho", 13, 6.8, True, True, 1))

	conexion.c.execute("SELECT * FROM partido_jugador")

	assert len(conexion.c.fetchall())==1

def test_existe_partido_jugador_no_existe(conexion):

	assert not conexion.existe_partido_jugador("1", "nacho")

def test_existe_partido_jugador_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarJugador("nacho")

	conexion.insertarPartidoJugador(("1", "nacho", 13, 6.8, True, True, 1))

	assert conexion.existe_partido_jugador("1", "nacho")