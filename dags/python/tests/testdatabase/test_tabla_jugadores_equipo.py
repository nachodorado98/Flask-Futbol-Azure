def test_tabla_partido_jugadores_equipo_vacia(conexion):

	conexion.c.execute("SELECT * FROM jugadores_equipo")

	assert not conexion.c.fetchall()

def test_insertar_equipo_jugador(conexion):

	conexion.insertarJugador("nacho")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoJugador(("nacho", "atleti-madrid", 1, 1, 1))

	conexion.c.execute("SELECT * FROM jugadores_equipo")

	assert len(conexion.c.fetchall())==1

def test_existe_equipo_jugador_no_existe(conexion):

	assert not conexion.existe_equipo_jugador("nacho", "atleti-madrid")

def test_existe_equipo_jugador(conexion):

	conexion.insertarJugador("nacho")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoJugador(("nacho", "atleti-madrid", 1, 1, 1))

	assert conexion.existe_equipo_jugador("nacho", "atleti-madrid")

def test_actualizar_equipo_jugador_no_existe(conexion):

	assert not conexion.existe_equipo_jugador("nacho", "atleti-madrid")

	datos_equipo_jugador=[1, 1, 1]

	conexion.actualizarDatosEquipoJugador(datos_equipo_jugador, "nacho", "atleti-madrid")

	assert not conexion.existe_equipo_jugador("nacho", "atleti-madrid")

def test_actualizar_equipo_jugador_no_existe_jugador(conexion):

	conexion.insertarJugador("nacho")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoJugador(("nacho", "atleti-madrid", 1, 1, 1))

	datos_equipo_jugador=[2, 2, 2]

	conexion.actualizarDatosEquipoJugador(datos_equipo_jugador, "no-existo", "atleti-madrid")

	conexion.c.execute("SELECT * FROM jugadores_equipo WHERE Jugador_Id='nacho'AND Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["temporadas"]==1
	assert datos_actualizados["goles"]==1
	assert datos_actualizados["partidos"]==1

def test_actualizar_equipo_jugador_no_existe_equipo(conexion):

	conexion.insertarJugador("nacho")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoJugador(("nacho", "atleti-madrid", 1, 1, 1))

	datos_equipo_jugador=[2, 2, 2]

	conexion.actualizarDatosEquipoJugador(datos_equipo_jugador, "nacho", "no-existo")

	conexion.c.execute("SELECT * FROM jugadores_equipo WHERE Jugador_Id='nacho'AND Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["temporadas"]==1
	assert datos_actualizados["goles"]==1
	assert datos_actualizados["partidos"]==1

def test_actualizar_equipo_jugador(conexion):

	conexion.insertarJugador("nacho")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoJugador(("nacho", "atleti-madrid", 1, 1, 1))

	datos_equipo_jugador=[2, 2, 2]

	conexion.actualizarDatosEquipoJugador(datos_equipo_jugador, "nacho", "atleti-madrid")

	conexion.c.execute("SELECT * FROM jugadores_equipo WHERE Jugador_Id='nacho'AND Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["temporadas"]==2
	assert datos_actualizados["goles"]==2
	assert datos_actualizados["partidos"]==2