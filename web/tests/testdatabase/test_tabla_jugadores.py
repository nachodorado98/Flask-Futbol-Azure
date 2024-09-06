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

def test_obtener_jugadores_no_existen(conexion):

	assert not conexion.obtenerDatosJugadores()

def test_obtener_jugadores(conexion_entorno):

	assert conexion_entorno.obtenerDatosJugadores()

def test_obtener_jugador_equipo_no_existe(conexion):

	assert not conexion.obtenerDatosJugadorEquipoValoracion("atletico-madrid")

def test_obtener_jugador_equipo(conexion_entorno):

	assert conexion_entorno.obtenerDatosJugadorEquipoValoracion("atletico-madrid")

def test_obtener_jugador_equipo_varios(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO jugadores
						VALUES('nacho', 'Nacho', 'atletico-madrid', 'es', '1', 1000, 100.0, 9, 'DC'),
								('nacho-1', 'Nacho', 'atletico-madrid', 'es', '1', 10, 100.0, 9, 'DC'),
								('nacho-2', 'Nacho', 'atletico-madrid', 'es', '1', 10000, 100.0, 9, 'DC'),
								('nacho-3', 'Nacho', 'atletico-madrid', 'es', '1', 5000, 100.0, 9, 'DC'),
								('nacho-4', 'Nacho', 'atletico-madrid', 'es', '1', 1100, 100.0, 9, 'DC')""")

	conexion_entorno.confirmar()

	jugador=conexion_entorno.obtenerDatosJugadorEquipoValoracion("atletico-madrid")

	assert jugador[0]=="nacho-2"

def test_obtener_jugadores_top_no_existe(conexion):

	assert not conexion.obtenerDatosJugadoresTop(5)

def test_obtener_jugadores_top(conexion):

	conexion.c.execute("""INSERT INTO jugadores (Jugador_Id, Puntuacion, Equipo_Id)
									VALUES('jugador1', 100, 'equipo'),('jugador2', 100, 'equipo'),('jugador3', 22, 'equipo'),
											('jugador4', 101, 'equipo'),('jugador5', 5, 'equipo'), ('jugador6', 15, 'equipo'),
											('jugador7', 13, 'equipo'),('jugador8', 3, 'equipo'),('jugador9', 1011, 'equipo'),
											('jugador10', 1, 'equipo')""")

	conexion.confirmar()

	jugadores_top=conexion.obtenerDatosJugadoresTop(5)

	assert jugadores_top[0][0]=="jugador9"
	assert jugadores_top[-1][0]=="jugador3"

def test_obtener_jugadores_equipo_no_existe(conexion):

	assert not conexion.obtenerJugadoresEquipo("atletico-madrid")

def test_obtener_jugadores_equipo(conexion_entorno):

	assert conexion_entorno.obtenerJugadoresEquipo("atletico-madrid")