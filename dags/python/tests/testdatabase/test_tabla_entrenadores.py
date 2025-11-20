import pytest

def test_tabla_entrenadores_vacia(conexion):

	conexion.c.execute("SELECT * FROM entrenadores")

	assert not conexion.c.fetchall()

def test_insertar_entrenador(conexion):

	conexion.insertarEntrenador("entrenador")

	conexion.c.execute("SELECT * FROM entrenadores")

	assert len(conexion.c.fetchall())==1

def test_existe_entrenador_no_existe(conexion):

	assert not conexion.existe_entrenador("entrenador")

def test_existe_entrenador_existe(conexion):

	conexion.insertarEntrenador("entrenador")

	assert conexion.existe_entrenador("entrenador")

def test_actualizar_datos_entrenador_no_existe(conexion):

	assert not conexion.existe_entrenador("entrenador")

	datos=["Cholo", "atletico-madrid", "ar", "1", 100]

	conexion.actualizarDatosEntrenador(datos, "entrenador")

	assert not conexion.existe_entrenador("entrenador")

@pytest.mark.parametrize(["datos_nuevos"],
	[
		(["Cholo", "atletico-madrid", "ar", "1", 100],),
		([None, "atletico-madrid", "ar", "1", 100],),
		(["Cholo", None, "ar", "1", 100],),
		(["Cholo", "atletico-madrid", None, "1", 100],),
		(["Cholo", "atletico-madrid", "ar", None, 100],),
		(["Cholo", "atletico-madrid", "ar", "1", None],)
	]
)
def test_actualizar_datos_entrenador(conexion, datos_nuevos):

	conexion.insertarEntrenador("entrenador")

	assert conexion.existe_entrenador("entrenador")

	conexion.actualizarDatosEntrenador(datos_nuevos, "entrenador")

	conexion.c.execute("SELECT * FROM entrenadores WHERE Entrenador_Id='entrenador'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]==datos_nuevos[0]
	assert datos_actualizados["equipo_id"]==datos_nuevos[1]
	assert datos_actualizados["codigo_pais"]==datos_nuevos[2]
	assert datos_actualizados["codigo_entrenador"]==datos_nuevos[3]
	assert datos_actualizados["puntuacion"]==datos_nuevos[4]

def test_obtener_entrenador_no_hay(conexion):

	assert not conexion.obtenerEntrenadores()

def test_obtener_entrenador(conexion):

	for numero in range(1,11):

		conexion.insertarEntrenador(f"entrenador-{numero}")

	entrenadores=conexion.obtenerEntrenadores()

	assert len(entrenadores)==10

def test_obtener_entrenadores_equipos_no_hay(conexion):

	assert not conexion.obtenerEntrenadoresEquipos()

def test_obtener_entrenadores_equipos_unicos(conexion):

	for numero in range(1,11):

		conexion.c.execute(f"""INSERT INTO equipos (Equipo_Id, Entrenador_URL) VALUES('atletico-madrid-{numero}', 'entrenador-{numero}')""")

	conexion.confirmar()

	entrenadores=conexion.obtenerEntrenadoresEquipos()

	assert len(entrenadores)==10

def test_obtener_entrenadores_equipos_duplicados(conexion):

	for numero in range(1,11):

		conexion.c.execute(f"""INSERT INTO equipos (Equipo_Id, Entrenador_URL) VALUES('atletico-madrid-{numero}', 'entrenador')""")

	conexion.confirmar()

	entrenadores=conexion.obtenerEntrenadoresEquipos()

	assert len(entrenadores)==1

def test_obtener_codigo_paises_entrenadores_no_hay(conexion):

	assert not conexion.obtenerCodigoPaisesEntrenadores()

@pytest.mark.parametrize(["datos", "numero_paises"],
	[
		([("cholo-simeone-13","ar"),("f-torres-29366","es"),("luis-aragones-1","fr")], 3),
		([("cholo-simeone-13","ar"),("f-torres-29366","es"),("luis-aragones-1",None)], 2),
		([("cholo-simeone-13","ar"),("f-torres-29366","es"),("luis-aragones-1",None),("ranieri-10","it")], 3),
		([("cholo-simeone-13","ar"),("f-torres-29366",None),("luis-aragones-1",None)], 1)
	]
)
def test_obtener_codigo_paises_entrenadores(conexion, datos, numero_paises):

	for entrenador, pais in datos:

		conexion.insertarEntrenador(entrenador)

		conexion.actualizarDatosEntrenador(["Cholo", "atletico-madrid", pais, "1", 100], entrenador)
	
	paises=conexion.obtenerCodigoPaisesEntrenadores()

	assert len(paises)==numero_paises

def test_obtener_entrenadores_sin_nombre_no_hay(conexion):

	assert not conexion.obtenerEntrenadoresNombreVacio()

def test_obtener_emtrenadores_sin_nombre(conexion):

	conexion.insertarEntrenador("cholo")

	conexion.actualizarDatosEntrenador(["Cholo", "atletico-madrid", "es", "1", 100], "cholo")

	for numero in range(1,11):

		conexion.insertarEntrenador(f"cholo-{numero}")

	entrenadores=conexion.obtenerEntrenadoresNombreVacio()

	assert len(entrenadores)==10

def test_obtener_entrenadores_sin_equipos_no_hay(conexion):

	assert not conexion.obtenerEntrenadoresEquiposVacio()

def test_obtener_entrenadores_sin_equipos(conexion):

	conexion.insertarEntrenador("cholo")

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipoEntrenador(("cholo", "atleti-madrid", 100, "2012-2027", 50, 30, 20, "4-4-2"))

	for numero in range(1,11):

		conexion.insertarEntrenador(f"cholo-{numero}")

	entrenadores=conexion.obtenerEntrenadoresEquiposVacio()

	assert len(entrenadores)==10

def test_obtener_entrenadores_sin_palmares_no_hay(conexion):

	assert not conexion.obtenerEntrenadoresPalmaresVacio()

def test_obtener_entrenadores_sin_palmares(conexion):

	conexion.insertarEntrenador("cholo")

	conexion.insertarCompeticion("primera")

	conexion.insertarTituloEntrenador(("cholo", "primera", "Primera", 10, "2019"))

	for numero in range(1,11):

		conexion.insertarEntrenador(f"cholo-{numero}")

	entrenadores=conexion.obtenerEntrenadoresPalmaresVacio()

	assert len(entrenadores)==10