def test_tabla_entrenador_titulo_vacia(conexion):

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	assert not conexion.c.fetchall()

def test_insertar_titulo_entrenador(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEntrenador("cholo")

	conexion.insertarTituloEntrenador(("cholo", "primera", "Primera", 10, "2019"))

	conexion.c.execute("SELECT * FROM entrenador_titulo")

	assert len(conexion.c.fetchall())==1

def test_existe_titulo_entrenador_no_existe(conexion):

	assert not conexion.existe_titulo_entrenador("primera", "cholo")

def test_existe_titulo_entrenador(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEntrenador("cholo")

	conexion.insertarTituloEntrenador(("cholo", "primera", "Primera", 10, "2019"))

	assert conexion.existe_titulo_entrenador("primera", "cholo")

def test_actualizar_titulo_entrenador_no_existe(conexion):

	assert not conexion.existe_titulo_entrenador("primera", "cholo")

	datos_titulo_entrenador=["Primera Division", 1, "22"]

	conexion.actualizarDatosTituloEntrenador(datos_titulo_entrenador, "primera", "cholo")

	assert not conexion.existe_titulo_entrenador("primera", "cholo")

def test_actualizar_titulo_entrenador_no_existe_competicion(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEntrenador("cholo")

	conexion.insertarTituloEntrenador(("cholo", "primera", "Primera", 10, "2019"))

	datos_titulo_entrenador=["Primera Division", 1, "22"]

	conexion.actualizarDatosTituloEntrenador(datos_titulo_entrenador, "primera", "no-existo")

	conexion.c.execute("SELECT * FROM entrenador_titulo WHERE Competicion_Id='primera' AND Entrenador_Id='cholo'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]=="Primera"
	assert datos_actualizados["numero"]==10
	assert datos_actualizados["annos"]=="2019"

def test_actualizar_titulo_entrenador_no_existe_entrenador(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEntrenador("cholo")

	conexion.insertarTituloEntrenador(("cholo", "primera", "Primera", 10, "2019"))

	datos_titulo_entrenador=["Primera Division", 1, "22"]

	conexion.actualizarDatosTituloEntrenador(datos_titulo_entrenador, "primera", "no-existo")

	conexion.c.execute("SELECT * FROM entrenador_titulo WHERE Competicion_Id='primera' AND Entrenador_Id='cholo'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]=="Primera"
	assert datos_actualizados["numero"]==10
	assert datos_actualizados["annos"]=="2019"

def test_actualizar_titulo_entrenador(conexion):

	conexion.insertarCompeticion("primera")

	conexion.insertarEntrenador("cholo")

	conexion.insertarTituloEntrenador(("cholo", "primera", "Primera", 10, "2019"))

	datos_titulo_entrenador=["Primera Division", 1, "22"]

	conexion.actualizarDatosTituloEntrenador(datos_titulo_entrenador, "primera", "cholo")

	conexion.c.execute("SELECT * FROM entrenador_titulo WHERE Competicion_Id='primera' AND Entrenador_Id='cholo'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]=="Primera Division"
	assert datos_actualizados["numero"]==1
	assert datos_actualizados["annos"]=="22"