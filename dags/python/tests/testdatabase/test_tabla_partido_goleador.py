def test_tabla_partido_goleador_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_goleador")

	assert not conexion.c.fetchall()

def test_insertar_partido_goleador(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarJugador("nacho")

	conexion.insertarPartidoGoleador(("1", "nacho", 1, 0, True))

	conexion.c.execute("SELECT * FROM partido_goleador")

	assert len(conexion.c.fetchall())==1

def test_existe_partido_goleador_no_existe(conexion):

	assert not conexion.existe_partido_goleador("1", "nacho", 1, 0)

def test_existe_partido_goleador_existe_partido(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarJugador("nachito")

	conexion.insertarPartidoGoleador(("1", "nachito", 2, 1, True))

	assert not conexion.existe_partido_goleador("1", "nacho", 1, 0)

def test_existe_partido_goleador_existe_jugador(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarJugador("nacho")

	conexion.insertarPartidoGoleador(("1", "nacho", 2, 1, True))

	assert not conexion.existe_partido_goleador("1", "nacho", 1, 0)

def test_existe_partido_goleador_existe_minuto(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarJugador("nacho")

	conexion.insertarPartidoGoleador(("1", "nacho", 1, 1, True))

	assert not conexion.existe_partido_goleador("1", "nacho", 1, 0)

def test_existe_partido_goleador_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarJugador("nacho")

	conexion.insertarPartidoGoleador(("1", "nacho", 1, 0, True))

	assert conexion.existe_partido_goleador("1", "nacho", 1, 0)