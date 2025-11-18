def test_tabla_partido_entrenadores_equipo_vacia(conexion):

	conexion.c.execute("SELECT * FROM entrenadores_equipo")

	assert not conexion.c.fetchall()

def test_insertar_entrenador_jugador(conexion):

	conexion.insertarEntrenador("cholo")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoEntrenador(("cholo", "atleti-madrid", 100, "2012-2027", 50, 30, 20, "4-4-2"))

	conexion.c.execute("SELECT * FROM entrenadores_equipo")

	assert len(conexion.c.fetchall())==1

def test_existe_equipo_entrenador_no_existe(conexion):

	assert not conexion.existe_equipo_entrenador("cholo", "atleti-madrid")

def test_existe_equipo_entrenador(conexion):

	conexion.insertarEntrenador("cholo")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoEntrenador(("cholo", "atleti-madrid", 100, "2012-2027", 50, 30, 20, "4-4-2"))

	assert conexion.existe_equipo_entrenador("cholo", "atleti-madrid")

def test_actualizar_equipo_entrenador_no_existe(conexion):

	assert not conexion.existe_equipo_entrenador("cholo", "atleti-madrid")

	datos_equipo_entrenador=[100, "2012-2027", 50, 30, 20, "4-4-2"]

	conexion.actualizarDatosEquipoEntrenador(datos_equipo_entrenador, "cholo", "atleti-madrid")

	assert not conexion.existe_equipo_entrenador("cholo", "atleti-madrid")

def test_actualizar_equipo_entrenador_no_existe_entrenador(conexion):

	conexion.insertarEntrenador("cholo")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoEntrenador(("cholo", "atleti-madrid", 100, "2012-2027", 50, 30, 20, "4-4-2"))

	datos_equipo_entrenador=[200, "1998-1999", 140, 20, 40, "4-3-3"]

	conexion.actualizarDatosEquipoEntrenador(datos_equipo_entrenador, "no-existo", "atleti-madrid")

	conexion.c.execute("SELECT * FROM entrenadores_equipo WHERE Entrenador_Id='cholo' AND Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["partidos_totales"]==100
	assert datos_actualizados["duracion"]=="2012-2027"
	assert datos_actualizados["ganados"]==50
	assert datos_actualizados["empatados"]==30
	assert datos_actualizados["perdidos"]==20
	assert datos_actualizados["tactica"]=="4-4-2"

def test_actualizar_equipo_entrenador_no_existe_equipo(conexion):

	conexion.insertarEntrenador("cholo")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoEntrenador(("cholo", "atleti-madrid", 100, "2012-2027", 50, 30, 20, "4-4-2"))

	datos_equipo_entrenador=[200, "1998-1999", 140, 20, 40, "4-3-3"]

	conexion.actualizarDatosEquipoEntrenador(datos_equipo_entrenador, "cholo", "no-existo")

	conexion.c.execute("SELECT * FROM entrenadores_equipo WHERE Entrenador_Id='cholo' AND Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["partidos_totales"]==100
	assert datos_actualizados["duracion"]=="2012-2027"
	assert datos_actualizados["ganados"]==50
	assert datos_actualizados["empatados"]==30
	assert datos_actualizados["perdidos"]==20
	assert datos_actualizados["tactica"]=="4-4-2"

def test_actualizar_equipo_entrenador(conexion):

	conexion.insertarEntrenador("cholo")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoEntrenador(("cholo", "atleti-madrid", 100, "2012-2027", 50, 30, 20, "4-4-2"))

	datos_equipo_entrenador=[200, "1998-1999", 140, 20, 40, "4-3-3"]

	conexion.actualizarDatosEquipoEntrenador(datos_equipo_entrenador, "cholo", "atleti-madrid")

	conexion.c.execute("SELECT * FROM entrenadores_equipo WHERE Entrenador_Id='cholo' AND Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["partidos_totales"]==200
	assert datos_actualizados["duracion"]=="1998-1999"
	assert datos_actualizados["ganados"]==140
	assert datos_actualizados["empatados"]==20
	assert datos_actualizados["perdidos"]==40
	assert datos_actualizados["tactica"]=="4-3-3"