def test_tabla_competiciones_vacia(conexion):

	conexion.c.execute("SELECT * FROM competiciones")

	assert not conexion.c.fetchall()

def test_existe_competicion_no_existe(conexion):

	assert not conexion.existe_competicion("primera")

def test_existe_competicion_existe(conexion_entorno):

	assert conexion_entorno.existe_competicion("primera")

def test_obtener_competicion_no_existe(conexion):

	assert not conexion.obtenerDatosCompeticion("primera")

def test_obtener_competicion(conexion_entorno):

	assert conexion_entorno.obtenerDatosCompeticion("primera")

def test_obtener_competiciones_no_existen(conexion):

	assert not conexion.obtenerDatosCompeticiones()

def test_obtener_competiciones(conexion_entorno):

	assert conexion_entorno.obtenerDatosCompeticiones()