def test_tabla_equipo_titulo_vacia(conexion):

	conexion.c.execute("SELECT * FROM equipo_titulo")

	assert not conexion.c.fetchall()

def test_obtener_titulos_equipo_no_existen(conexion):

	assert not conexion.obtenerTitulosEquipo("atletico-madrid")

def test_obtener_titulos_equipo(conexion_entorno):

	assert conexion_entorno.obtenerTitulosEquipo("atletico-madrid")