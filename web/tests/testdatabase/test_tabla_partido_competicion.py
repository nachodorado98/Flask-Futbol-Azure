def test_tabla_partido_competicion_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_competicion")

	assert not conexion.c.fetchall()

def test_obtener_partido_competicion_no_existen(conexion):

	assert not conexion.obtenerPartidosCompeticion("primera")

def test_obtener_partido_competicion(conexion_entorno):

	assert conexion_entorno.obtenerPartidosCompeticion("primera")