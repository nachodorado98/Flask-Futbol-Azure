def test_tabla_partido_goleador_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_goleador")

	assert not conexion.c.fetchall()

def test_obtener_partido_goleador_no_existen(conexion):

	assert not conexion.obtenerGoleadoresPartido("20190622")

def test_obtener_partido_goleador(conexion_entorno):

	assert conexion_entorno.obtenerGoleadoresPartido("20190622")