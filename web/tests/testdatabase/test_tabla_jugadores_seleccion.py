import pytest

def test_tabla_jugadores_seleccion_vacia(conexion):

	conexion.c.execute("SELECT * FROM jugadores_seleccion")

	assert not conexion.c.fetchall()

def test_obtener_seleccion_jugador_no_existe_jugador(conexion):

	assert not conexion.obtenerSeleccionJugador("julian-alvarez")

def test_obtener_seleccion_jugador_no_tiene(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO jugadores
								VALUES('nacho', 'Nacho', 'atletico-madrid', 'es', '1324', 100, 100.0, 9, 'DC')""")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerSeleccionJugador("nacho")

def test_obtener_seleccion_jugador(conexion_entorno):

	assert conexion_entorno.obtenerSeleccionJugador("julian-alvarez")