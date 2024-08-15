def test_tabla_partido_competicion_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_competicion")

	assert not conexion.c.fetchall()

def test_insertar_partido_competicion(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarCompeticion("competicion")

	conexion.insertarPartidoCompeticion(("1", "competicion"))

	conexion.c.execute("SELECT * FROM partido_competicion")

	assert len(conexion.c.fetchall())==1

def test_existe_partido_competicion_no_existe(conexion):

	assert not conexion.existe_partido_competicion("1", "competicion")

def test_existe_partido_competicion_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarCompeticion("competicion")

	conexion.insertarPartidoCompeticion(("1", "competicion"))

	assert conexion.existe_partido_competicion("1", "competicion")