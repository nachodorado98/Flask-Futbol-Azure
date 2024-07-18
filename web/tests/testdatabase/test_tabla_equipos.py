def test_tabla_equipos_vacia(conexion):

	conexion.c.execute("SELECT * FROM equipos")

	assert not conexion.c.fetchall()

def test_existe_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atletico-madrid")

def test_existe_equipo_existente(conexion_entorno):

	assert conexion_entorno.existe_equipo("atletico-madrid")