def test_tabla_equipos_vacia(conexion):

	conexion.c.execute("SELECT * FROM equipos")

	assert not conexion.c.fetchall()

def test_insertar_equipo(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.c.execute("SELECT * FROM equipos")

	assert len(conexion.c.fetchall())==1

def test_existe_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atleti-madrid")

def test_existe_equipo_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	assert conexion.existe_equipo("atleti-madrid")