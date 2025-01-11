import pytest

def test_tabla_partido_jugadores_seleccion_vacia(conexion):

	conexion.c.execute("SELECT * FROM jugadores_seleccion")

	assert not conexion.c.fetchall()

def test_insertar_seleccion_jugador(conexion):

	conexion.insertarJugador("nacho")

	conexion.insertarSeleccionJugador(("nacho", 22, 1, 2, 3))

	conexion.c.execute("SELECT * FROM jugadores_seleccion")

	assert len(conexion.c.fetchall())==1

def test_existe_seleccion_jugador_no_existe(conexion):

	assert not conexion.existe_seleccion_jugador("nacho")

def test_existe_seleccion_jugador(conexion):

	conexion.insertarJugador("nacho")

	conexion.insertarSeleccionJugador(("nacho", 22, 1, 2, 3))

	assert conexion.existe_seleccion_jugador("nacho")

def test_actualizar_seleccion_jugador_no_existe_jugador(conexion):

	conexion.insertarJugador("nacho")

	conexion.insertarSeleccionJugador(("nacho", 13, 1, 1, 1))

	datos_seleccion_jugador=[22, 2, 3, 4]

	conexion.actualizarDatosSeleccionJugador(datos_seleccion_jugador, "no-existo")

	conexion.c.execute("SELECT * FROM jugadores_seleccion WHERE Jugador_Id='nacho'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["codigo_seleccion"]==13
	assert datos_actualizados["convocatorias"]==1
	assert datos_actualizados["goles"]==1
	assert datos_actualizados["asistencias"]==1

def test_actualizar_seleccion_jugador(conexion):

	conexion.insertarJugador("nacho")

	conexion.insertarSeleccionJugador(("nacho", 13, 1, 1, 1))

	datos_seleccion_jugador=[22, 2, 3, 4]

	conexion.actualizarDatosSeleccionJugador(datos_seleccion_jugador, "nacho")

	conexion.c.execute("SELECT * FROM jugadores_seleccion WHERE Jugador_Id='nacho'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["codigo_seleccion"]==22
	assert datos_actualizados["convocatorias"]==2
	assert datos_actualizados["goles"]==3
	assert datos_actualizados["asistencias"]==4

def test_obtener_codigo_selecciones_jugadores_no_hay(conexion):

	assert not conexion.obtenerCodigoSeleccionesJugadores()

@pytest.mark.parametrize(["datos", "numero_selecciones"],
	[
		([("julian-alvarez-13",2),("f-torres-29366",1),("a-griezmann-32465",3)], 3),
		([("julian-alvarez-13",2),("f-torres-29366",1),("a-griezmann-32465",None)], 2),
		([("julian-alvarez-13",2),("f-torres-29366",1),("a-griezmann-32465",None),("samu-lino-1324",4)], 3),
		([("julian-alvarez-13",2),("f-torres-29366",None),("a-griezmann-32465",None)], 1)
	]
)
def test_obtener_codigo_selecciones_jugadores(conexion, datos, numero_selecciones):

	for jugador, seleccion in datos:

		conexion.insertarJugador(jugador)

		conexion.insertarSeleccionJugador((jugador, seleccion, 1, 1, 1))
	
	selecciones=conexion.obtenerCodigoSeleccionesJugadores()

	assert len(selecciones)==numero_selecciones