def test_tabla_partido_entrenador_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_entrenador")

	assert not conexion.c.fetchall()

def test_obtener_partido_entrenadores_no_existen(conexion):

	assert not conexion.obtenerEntrenadoresPartido("20190622")

def test_obtener_partido_entrenadores(conexion_entorno):

	assert conexion_entorno.obtenerEntrenadoresPartido("20190622")