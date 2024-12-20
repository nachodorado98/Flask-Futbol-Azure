def test_tabla_entrenadores_vacia(conexion):

	conexion.c.execute("SELECT * FROM entrenadores")

	assert not conexion.c.fetchall()

def test_existe_entrenador_no_existe(conexion):

	assert not conexion.existe_entrenador("diego-pablo")

def test_existe_entrenador_existe(conexion_entorno):

	assert conexion_entorno.existe_entrenador("diego-pablo")

def test_obtener_entrenador_no_existe(conexion):

	assert not conexion.obtenerDatosEntrenador("diego-pablo")

def test_obtener_entrenador(conexion_entorno):

	assert conexion_entorno.obtenerDatosEntrenador("diego-pablo")