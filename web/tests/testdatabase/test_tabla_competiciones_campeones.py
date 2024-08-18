def test_tabla_competiciones_campeones_vacia(conexion):

	conexion.c.execute("SELECT * FROM competiciones_campeones")

	assert not conexion.c.fetchall()

def test_obtener_competiciones_campeones_no_existen(conexion):

	assert not conexion.obtenerCampeonesCompeticion("primera")

def test_obtener_competiciones_campeones(conexion_entorno):

	assert conexion_entorno.obtenerCampeonesCompeticion("primera")