import pytest

def test_tabla_jugadores_vacia(conexion):

	conexion.c.execute("SELECT * FROM jugadores")

	assert not conexion.c.fetchall()

def test_insertar_jugador(conexion):

	conexion.insertarJugador("jugador")

	conexion.c.execute("SELECT * FROM jugadores")

	assert len(conexion.c.fetchall())==1

def test_existe_jugador_no_existe(conexion):

	assert not conexion.existe_jugador("jugador")

def test_existe_jugador_existe(conexion):

	conexion.insertarJugador("jugador")

	assert conexion.existe_jugador("jugador")

def test_actualizar_datos_jugador_no_existe(conexion):

	assert not conexion.existe_jugador("jugador")

	datos=["Julian", "atletico-madrid", "ar", "1", 100, 100.0, 19, "DEL"]

	conexion.actualizarDatosJugador(datos, "jugador")

	assert not conexion.existe_jugador("jugador")

@pytest.mark.parametrize(["datos_nuevos"],
	[
		(["Julian", "atletico-madrid", "ar", "1", 100, 100.0, 19, "DEL"],),
		([None, "atletico-madrid", "ar", "1", 100, 100.0, 19, "DEL"],),
		(["Julian", None, "ar", "1", 100, 100.0, 19, "DEL"],),
		(["Julian", "atletico-madrid", None, "1", 100, 100.0, 19, "DEL"],),
		(["Julian", "atletico-madrid", "ar", None, 100, 100.0, 19, "DEL"],),
		(["Julian", "atletico-madrid", "ar", "1", None, 100.0, 19, "DEL"],),
		(["Julian", "atletico-madrid", "ar", "1", 100, None, 19, "DEL"],),
		(["Julian", "atletico-madrid", "ar", "1", 100, 100.0, None, "DEL"],),
		(["Julian", "atletico-madrid", "ar", "1", 100, 100.0, 19, None],)
	]
)
def test_actualizar_datos_jugador(conexion, datos_nuevos):

	conexion.insertarJugador("jugador")

	assert conexion.existe_jugador("jugador")

	conexion.actualizarDatosJugador(datos_nuevos, "jugador")

	conexion.c.execute("SELECT * FROM jugadores WHERE Jugador_Id='jugador'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]==datos_nuevos[0]
	assert datos_actualizados["equipo_id"]==datos_nuevos[1]
	assert datos_actualizados["codigo_pais"]==datos_nuevos[2]
	assert datos_actualizados["codigo_jugador"]==datos_nuevos[3]
	assert datos_actualizados["puntuacion"]==datos_nuevos[4]
	assert datos_actualizados["valor"]==datos_nuevos[5]
	assert datos_actualizados["dorsal"]==datos_nuevos[6]
	assert datos_actualizados["posicion"]==datos_nuevos[7]

def test_obtener_jugadores_no_hay(conexion):

	assert not conexion.obtenerJugadores()

def test_obtener_jugadores(conexion):

	for numero in range(1,11):

		conexion.insertarJugador(f"jugador-{numero}")

	jugadores=conexion.obtenerJugadores()

	assert len(jugadores)==10