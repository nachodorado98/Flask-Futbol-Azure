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