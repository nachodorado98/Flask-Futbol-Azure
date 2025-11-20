def test_tabla_equipo_titulo_vacia(conexion):

	conexion.c.execute("SELECT * FROM equipo_titulo")

	assert not conexion.c.fetchall()

def test_insertar_titulo_equipo(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarTituloEquipo(("atleti-madrid", "primera", "Primera", 10, "2019"))

	conexion.c.execute("SELECT * FROM equipo_titulo")

	assert len(conexion.c.fetchall())==1

def test_existe_titulo_equipo_no_existe(conexion):

	assert not conexion.existe_titulo_equipo("primera", "atleti-madrid")

def test_existe_titulo_equipo(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarTituloEquipo(("atleti-madrid", "primera", "Primera", 10, "2019"))

	assert conexion.existe_titulo_equipo("primera", "atleti-madrid")

def test_actualizar_titulo_equipo_no_existe(conexion):

	assert not conexion.existe_titulo_equipo("primera", "atleti-madrid")

	datos_titulo_equipo=["Primera Division", 1, "22"]

	conexion.actualizarDatosTituloEquipo(datos_titulo_equipo, "primera", "atleti-madrid")

	assert not conexion.existe_titulo_equipo("primera", "atleti-madrid")

def test_actualizar_titulo_equipo_no_existe_competicion(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarTituloEquipo(("atleti-madrid", "primera", "Primera", 10, "2019"))

	datos_titulo_equipo=["Primera Division", 1, "22"]

	conexion.actualizarDatosTituloEquipo(datos_titulo_equipo, "no-existo", "atleti-madrid")

	conexion.c.execute("SELECT * FROM equipo_titulo WHERE Competicion_Id='primera'AND Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]=="Primera"
	assert datos_actualizados["numero"]==10
	assert datos_actualizados["annos"]=="2019"

def test_actualizar_titulo_equipo_no_existe_equipo(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarTituloEquipo(("atleti-madrid", "primera", "Primera", 10, "2019"))

	datos_titulo_equipo=["Primera Division", 1, "22"]

	conexion.actualizarDatosTituloEquipo(datos_titulo_equipo, "primera", "no-existo")

	conexion.c.execute("SELECT * FROM equipo_titulo WHERE Competicion_Id='primera'AND Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]=="Primera"
	assert datos_actualizados["numero"]==10
	assert datos_actualizados["annos"]=="2019"

def test_actualizar_titulo_equipo(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarTituloEquipo(("atleti-madrid", "primera", "Primera", 10, "2019"))

	datos_titulo_equipo=["Primera Division", 1, "22"]

	conexion.actualizarDatosTituloEquipo(datos_titulo_equipo, "primera", "atleti-madrid")

	conexion.c.execute("SELECT * FROM equipo_titulo WHERE Competicion_Id='primera'AND Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]=="Primera Division"
	assert datos_actualizados["numero"]==1
	assert datos_actualizados["annos"]=="22"