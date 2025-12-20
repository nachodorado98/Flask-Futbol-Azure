def test_tabla_entrenador_titulo_vacia(conexion):

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	assert not conexion.c.fetchall()

def test_obtener_titulos_entrenador_no_existen(conexion):

	assert not conexion.obtenerTitulosEntrenador("diego-pablo")

def test_obtener_titulos_entrenador(conexion_entorno):

	assert conexion_entorno.obtenerTitulosEntrenador("diego-pablo")