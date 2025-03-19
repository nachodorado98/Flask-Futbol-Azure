def test_tabla_paises_llena(conexion):
 
 	conexion.c.execute("SELECT * FROM paises")
 
 	assert conexion.c.fetchall()