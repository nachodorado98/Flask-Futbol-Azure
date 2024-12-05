def test_tabla_proximos_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()

def test_insertar_proximo_partido(conexion):

	conexion.insertarEquipo("atleti-madrid")

	proximo_partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert len(conexion.c.fetchall())==1

def test_existe_proximo_partido_no_existe(conexion):

	assert not conexion.existe_proximo_partido("1")

def test_existe_proximo_partido_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	proximo_partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	assert conexion.existe_proximo_partido("1")

def test_vaciar_tabla_proximos_partidos_no_hay(conexion):

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()

	conexion.vaciar_proximos_partidos()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()

def test_vaciar_tabla_proximos_partidos(conexion):

	conexion.insertarEquipo("atleti-madrid")

	proximo_partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert conexion.c.fetchall()

	conexion.vaciar_proximos_partidos()

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()