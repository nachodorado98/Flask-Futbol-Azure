def test_tabla_partido_entrenador_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_entrenador")

	assert not conexion.c.fetchall()

def test_insertar_partido_entrenador(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarEntrenador("cholo")

	conexion.insertarPartidoEntrenador(("1", "cholo", "4-4-2", True))

	conexion.c.execute("SELECT * FROM partido_entrenador")

	assert len(conexion.c.fetchall())==1

def test_existe_partido_entrenador_no_existe(conexion):

	assert not conexion.existe_partido_entrenador("1", "cholo")

def test_existe_partido_entrenador_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.insertarEntrenador("cholo")

	conexion.insertarPartidoEntrenador(("1", "cholo", "4-4-2", True))

	assert conexion.existe_partido_entrenador("1", "cholo")