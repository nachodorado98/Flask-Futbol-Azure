def test_tabla_paises_llena(conexion):

	conexion.c.execute("SELECT * FROM paises")

	assert conexion.c.fetchall()

def test_obtener_paises_existen(conexion):

	assert conexion.obtenerPaises()