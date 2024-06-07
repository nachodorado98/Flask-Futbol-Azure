def test_tabla_ligas_llena(conexion):

	conexion.c.execute("SELECT * FROM ligas")

	assert conexion.c.fetchall()