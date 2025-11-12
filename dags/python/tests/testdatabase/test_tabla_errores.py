def test_tabla_errores_vacia(conexion):

	conexion.c.execute("SELECT * FROM errores")

	assert not conexion.c.fetchall()

def test_insertar_error(conexion):

	conexion.insertarError("jugador", "detalle", "juli")

	conexion.c.execute("SELECT * FROM errores")

	errores=conexion.c.fetchall()

	assert len(errores)==1
	assert errores[0]["numero_errores"]==1

def test_existe_error_no_existe(conexion):

	assert not conexion.existe_error("jugador", "detalle", "juli")

def test_existe_error_existe(conexion):

	conexion.insertarError("jugador", "detalle", "juli")

	assert conexion.existe_error("jugador", "detalle", "juli")

def test_obtener_numero_errores_no_existe(conexion):

	numero_errores=conexion.obtenerNumeroErrores("jugador", "detalle", "juli")

	assert numero_errores==0

def test_obtener_numero_errores(conexion):

	conexion.insertarError("jugador", "detalle", "juli")

	numero_errores=conexion.obtenerNumeroErrores("jugador", "detalle", "juli")

	assert numero_errores==1

def test_actualizar_numero_errores_no_existe(conexion):

	assert not conexion.existe_error("jugador", "detalle", "juli")

	conexion.actualizarNumeroErrores("jugador", "detalle", "juli")

	assert not conexion.existe_error("jugador", "detalle", "juli")

def test_actualizar_numero_errores(conexion):

	conexion.insertarError("jugador", "detalle", "juli")

	assert conexion.existe_error("jugador", "detalle", "juli")

	conexion.actualizarNumeroErrores("jugador", "detalle", "juli")

	numero_errores=conexion.obtenerNumeroErrores("jugador", "detalle", "juli")

	assert numero_errores==2

def test_actualizar_numero_errores_varios(conexion):

	conexion.insertarError("jugador", "detalle", "juli")

	assert conexion.existe_error("jugador", "detalle", "juli")

	for _ in range(10):

		conexion.actualizarNumeroErrores("jugador", "detalle", "juli")

	numero_errores=conexion.obtenerNumeroErrores("jugador", "detalle", "juli")

	assert numero_errores==11