def test_tabla_ligas_llena(conexion):

	conexion.c.execute("SELECT * FROM ligas_scrapear")

	assert conexion.c.fetchall()

def test_obtener_ligas(conexion):

	ligas=conexion.obtenerLigas()

	assert len(ligas)>0