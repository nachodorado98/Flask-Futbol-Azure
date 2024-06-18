def test_tabla_variables_llena(conexion):

	conexion.c.execute("SELECT * FROM variables")

	assert conexion.c.fetchall()

def test_obtener_valor_variable_no_existe(conexion):

	assert not conexion.obtenerValorVariable("no_existo")

def test_obtener_valor_variable(conexion):

	conexion.c.execute("INSERT INTO variables VALUES ('existo', 'True')")

	conexion.confirmar()

	assert conexion.obtenerValorVariable("existo")=="True"

	conexion.c.execute("DELETE FROM variables WHERE Nombre='existo'")

	conexion.confirmar()

def test_actualizar_valor_variable_no_existe(conexion):

	assert not conexion.obtenerValorVariable("no_existo")

	conexion.actualizarValorVariable("no_existo", "valor")

	assert not conexion.obtenerValorVariable("no_existo")

def test_actualizar_valor_variable_no_existe(conexion):

	conexion.c.execute("INSERT INTO variables VALUES ('existo', 'True')")

	conexion.confirmar()

	assert conexion.obtenerValorVariable("existo")=="True"

	conexion.actualizarValorVariable("existo", "nuevo_valor")

	assert conexion.obtenerValorVariable("existo")=="nuevo_valor"

	conexion.c.execute("DELETE FROM variables WHERE Nombre='existo'")

	conexion.confirmar()