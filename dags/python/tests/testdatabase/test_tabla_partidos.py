def test_tabla_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM partidos")

	assert not conexion.c.fetchall()

def test_insertar_partido(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=[1, "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==1

def test_existe_partido_no_existe(conexion):

	assert not conexion.existe_partido(1)

def test_existe_partido_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=[1, "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	assert conexion.existe_partido(1)