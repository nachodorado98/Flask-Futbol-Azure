def test_tabla_equipo_estadio_vacia(conexion):

	conexion.c.execute("SELECT * FROM equipo_estadio")

	assert not conexion.c.fetchall()

def test_equipo_estadio_no_existe(conexion):

	assert not conexion.estadio_equipo("atletico-madrid")

def test_equipo_estadio(conexion_entorno):

	assert conexion_entorno.estadio_equipo("atletico-madrid")