def test_tabla_jugadores_vacia(conexion):

	conexion.c.execute("SELECT * FROM jugadores")

	assert not conexion.c.fetchall()

def test_insertar_jugador(conexion):

	conexion.insertarJugador("jugador")

	conexion.c.execute("SELECT * FROM jugadores")

	assert len(conexion.c.fetchall())==1

def test_existe_jugador_no_existe(conexion):

	assert not conexion.existe_jugador("jugador")

def test_existe_jugador_existe(conexion):

	conexion.insertarJugador("jugador")

	assert conexion.existe_jugador("jugador")