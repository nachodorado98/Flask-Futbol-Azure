def test_tabla_jugadores_vacia(conexion):

	conexion.c.execute("SELECT * FROM jugadores")

	assert not conexion.c.fetchall()

def test_existe_jugador_no_existe(conexion):

	assert not conexion.existe_jugador("julian-alvarez")

def test_existe_jugador_existe(conexion_entorno):

	assert conexion_entorno.existe_jugador("julian-alvarez")

def test_obtener_jugador_no_existe(conexion):

	assert not conexion.obtenerDatosJugador("julian-alvarez")

def test_obtener_jugador(conexion_entorno):

	assert conexion_entorno.obtenerDatosJugador("julian-alvarez")