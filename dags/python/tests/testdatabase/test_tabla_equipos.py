import pytest

def test_tabla_equipos_vacia(conexion):

	conexion.c.execute("SELECT * FROM equipos")

	assert not conexion.c.fetchall()

def test_insertar_equipo(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.c.execute("SELECT * FROM equipos")

	assert len(conexion.c.fetchall())==1

def test_existe_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atleti-madrid")

def test_existe_equipo_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	assert conexion.existe_equipo("atleti-madrid")

def test_actualizar_datos_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atleti-madrid")

	datos=["Club Atletico de Madrid", "Atleti", "ATM", "España", "es", "Madrid", "Primera", "primera",
			22, "Calderon", 1903, "Nacho", "nacho-dorado", 16]

	conexion.actualizarDatosEquipo(datos, "atleti-madrid")

	assert not conexion.existe_equipo("atleti-madrid")

@pytest.mark.parametrize(["datos_nuevos"],
	[
		(["Club Atletico de Madrid", "Atleti", "ATM", "España", "es", "Madrid", "Primera", "primera",
			22, "Calderon", 1903, "Nacho", "nacho-dorado", 16],),
		(["Club Atletico", "AtletiMadrid", "ATM", "Españita", "aa", "Madrid", "Primera","primera",
			22, "Calderon", 1903, "Golden", "nacho-dorado", 16],),
		(["Club Atletico de Madrid", "Atleti", "ATM", "España", "es", "Piramides", "Primera Division",
			"primera-division", 2019, "Eterno Calderon", 2019, "Golden", "nacho-dorado", None],)
	]
)
def test_actualizar_datos_equipo(conexion, datos_nuevos):

	conexion.insertarEquipo("atleti-madrid")

	assert conexion.existe_equipo("atleti-madrid")

	conexion.actualizarDatosEquipo(datos_nuevos, "atleti-madrid")

	conexion.c.execute("SELECT * FROM equipos WHERE Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre_completo"]==datos_nuevos[0]
	assert datos_actualizados["nombre"]==datos_nuevos[1]
	assert datos_actualizados["siglas"]==datos_nuevos[2]
	assert datos_actualizados["pais"]==datos_nuevos[3]
	assert datos_actualizados["codigo_pais"]==datos_nuevos[4]
	assert datos_actualizados["ciudad"]==datos_nuevos[5]
	assert datos_actualizados["competicion"]==datos_nuevos[6]
	assert datos_actualizados["codigo_competicion"]==datos_nuevos[7]
	assert datos_actualizados["temporadas"]==datos_nuevos[8]
	assert datos_actualizados["estadio"]==datos_nuevos[9]
	assert datos_actualizados["fundacion"]==datos_nuevos[10]
	assert datos_actualizados["presidente"]==datos_nuevos[11]
	assert datos_actualizados["presidente_url"]==datos_nuevos[12]
	assert datos_actualizados["codigo_presidente"]==datos_nuevos[13]

def test_obtener_equipos_no_hay(conexion):

	assert not conexion.obtenerEquipos()

def test_obtener_equipos(conexion):

	for numero in range(1,11):

		conexion.insertarEquipo(f"atleti-madrid-{numero}")

	equipos=conexion.obtenerEquipos()

	assert len(equipos)==10

def test_actualizar_escudo_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atleti-madrid")

	datos=[1234, 99]

	conexion.actualizarEscudoEquipo(datos, "atleti-madrid")

	assert not conexion.existe_equipo("atleti-madrid")

@pytest.mark.parametrize(["datos_nuevos"],
	[
		([1234, 99],),
		([0, 999],),
		([124356, 0],),
		([1, 1],)
	]
)
def test_actualizar_escudo_equipo(conexion, datos_nuevos):

	conexion.insertarEquipo("atleti-madrid")

	assert conexion.existe_equipo("atleti-madrid")

	conexion.actualizarEscudoEquipo(datos_nuevos, "atleti-madrid")

	conexion.c.execute("SELECT * FROM equipos WHERE Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["escudo"]==datos_nuevos[0]
	assert datos_actualizados["puntuacion"]==datos_nuevos[1]

def test_actualizar_entrenador_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atleti-madrid")

	datos=["Cholo", "cholo-simeone", 22, 1000]

	conexion.actualizarEntrenadorEquipo(datos, "atleti-madrid")

	assert not conexion.existe_equipo("atleti-madrid")

@pytest.mark.parametrize(["datos_nuevos"],
	[
		(["Cholo", "cholo-simeone", 22, 1000],),
		(["Ole ole ole", "cholo-simeone", 22, None],),
		(["Nacho", "cholo-simeone", 13, 1000],),
		(["Cholo", "Golden", None, 1000],)
	]
)
def test_actualizar_entrenador_equipo(conexion, datos_nuevos):

	conexion.insertarEquipo("atleti-madrid")

	assert conexion.existe_equipo("atleti-madrid")

	conexion.actualizarEntrenadorEquipo(datos_nuevos, "atleti-madrid")

	conexion.c.execute("SELECT * FROM equipos WHERE Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["entrenador"]==datos_nuevos[0]
	assert datos_actualizados["entrenador_url"]==datos_nuevos[1]
	assert datos_actualizados["codigo_entrenador"]==datos_nuevos[2]
	assert datos_actualizados["partidos"]==datos_nuevos[3]

def test_obtener_codigo_escudos_no_hay(conexion):

	assert not conexion.obtenerCodigoEscudos()

@pytest.mark.parametrize(["datos", "numero_escudos"],
	[
		([("atleti-madrid", 1), ("atleti", 2), ("atm", 3)], 3),
		([("atleti-madrid", 1), ("atleti", 2), ("atm", None)], 2),
		([("atleti-madrid", 1), ("atleti", 2), ("atm", 3), ("equipo", None)], 3),
		([("atleti-madrid", None), ("atleti", None), ("atm", 3)], 1)
	]
)
def test_obtener_codigo_escudos(conexion, datos, numero_escudos):

	for equipo, escudo in datos:

		conexion.insertarEquipo(equipo)

		conexion.actualizarEscudoEquipo([escudo, 100], equipo)

	escudos=conexion.obtenerCodigoEscudos()

	assert len(escudos)==numero_escudos

def test_obtener_codigo_entrenadores_no_hay(conexion):

	assert not conexion.obtenerCodigoEntrenadores()

@pytest.mark.parametrize(["datos", "numero_entrenadores"],
	[
		([("atleti-madrid", 1), ("atleti", 2), ("atm", 3)], 3),
		([("atleti-madrid", 1), ("atleti", 2), ("atm", None)], 2),
		([("atleti-madrid", 1), ("atleti", 2), ("atm", 3), ("equipo", None)], 3),
		([("atleti-madrid", None), ("atleti", None), ("atm", 3)], 1)
	]
)
def test_obtener_codigo_entrenadores(conexion, datos, numero_entrenadores):

	for equipo, codigo in datos:

		conexion.insertarEquipo(equipo)

		conexion.actualizarEntrenadorEquipo(["cholo", "simeone", codigo, 100], equipo)

	codigo_entrenadores=conexion.obtenerCodigoEntrenadores()

	assert len(codigo_entrenadores)==numero_entrenadores

def test_obtener_codigo_presidentes_no_hay(conexion):

	assert not conexion.obtenerCodigoPresidentes()

@pytest.mark.parametrize(["datos", "numero_presidentes"],
	[
		([("atleti-madrid", 1), ("atleti", 2), ("atm", 3)], 3),
		([("atleti-madrid", 1), ("atleti", 2), ("atm", None)], 2),
		([("atleti-madrid", 1), ("atleti", 2), ("atm", 3), ("equipo", None)], 3),
		([("atleti-madrid", None), ("atleti", None), ("atm", 3)], 1)
	]
)
def test_obtener_codigo_presidentes(conexion, datos, numero_presidentes):

	for equipo, codigo in datos:

		conexion.insertarEquipo(equipo)

		conexion.c.execute("""UPDATE equipos
							SET Codigo_Presidente=%s
							WHERE Equipo_Id=%s""",
							(codigo, equipo))

		conexion.confirmar()

	codigo_presidentes=conexion.obtenerCodigoPresidentes()

	assert len(codigo_presidentes)==numero_presidentes

def test_obtener_codigo_paises_equipos_no_hay(conexion):

	assert not conexion.obtenerCodigoPaisesEquipos()

def test_obtener_codigo_paises_equipos_son_nulos(conexion):

	for numero in range(1,11):

		conexion.insertarEquipo(f"atleti-madrid-{numero}")

	assert not conexion.obtenerCodigoPaisesEquipos()

@pytest.mark.parametrize(["datos", "numero_paises"],
	[
		([["Argentina", "ar"], [None, "ar"], ["Argentina", None], ["España", "es"]], 2),
		([["Argentina", "ar"], [None, "ar"], ["Argentina", None], ["Argentina", "ar"]], 1),
		([["Argentina", None], [None, "ar"], ["Argentina", None], ["España", "es"]], 2),
		([["Argentina", "ar"], [None, "ar"], ["Argentina", None], ["España", "es"], ["Francia", "fr"]], 3),
	]
)
def test_obtener_codigo_paises_equipos(conexion, datos, numero_paises):

	for numero, dato in enumerate(datos):

		conexion.insertarEquipo(f"atleti-madrid-{numero}")

		datos=["Club Atletico de Madrid", "Atleti", "ATM", dato[0], dato[1], "Madrid", "Primera", "primera",
				22, "Calderon", 1903, "Nacho", "nacho-dorado", 16]

		conexion.actualizarDatosEquipo(datos, f"atleti-madrid-{numero}")

	paises=conexion.obtenerCodigoPaisesEquipos()

	assert len(paises)==numero_paises

def test_obtener_equipos_sin_nombre_no_hay(conexion):

	assert not conexion.obtenerEquiposNombreVacio()

def test_obtener_equipos_sin_nombre(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.c.execute("UPDATE equipos SET Nombre='Nombre', Nombre_Completo='Nombre'")

	for numero in range(1,11):

		conexion.insertarEquipo(f"atleti-madrid-{numero}")

	equipos=conexion.obtenerEquiposNombreVacio()

	assert len(equipos)==10

def test_obtener_equipos_sin_escudo_no_hay(conexion):

	assert not conexion.obtenerEquiposEscudoVacio()

def test_obtener_equipos_sin_escudo(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.c.execute("UPDATE equipos SET Escudo=1")

	for numero in range(1,11):

		conexion.insertarEquipo(f"atleti-madrid-{numero}")

	equipos=conexion.obtenerEquiposEscudoVacio()

	assert len(equipos)==10

def test_obtener_equipos_sin_entrenador_no_hay(conexion):

	assert not conexion.obtenerEquiposEntrenadorVacio()

def test_obtener_equipos_sin_entrenador(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.c.execute("UPDATE equipos SET Entrenador='Entrenador'")

	for numero in range(1,11):

		conexion.insertarEquipo(f"atleti-madrid-{numero}")

	equipos=conexion.obtenerEquiposEntrenadorVacio()

	assert len(equipos)==10

def test_obtener_equipos_sin_estadio_no_hay(conexion):

	assert not conexion.obtenerEquiposEstadioVacio()

def test_obtener_equipos_sin_estadio(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEstadio(['metropolitano', 23, 'Metropolitano', 'Av Luis Aragones', 40.436, -3.599, 'Madrid', 100000,
							2017, 105, 68, 'Telefono', 'Cedped'])

	conexion.insertarEquipoEstadio(('atleti-madrid', 'metropolitano'))

	for numero in range(1,11):

		conexion.insertarEquipo(f"atleti-madrid-{numero}")

	equipos=conexion.obtenerEquiposEstadioVacio()

	assert len(equipos)==10

def test_obtener_equipos_sin_palmares_no_hay(conexion):

	assert not conexion.obtenerEquiposPalmaresVacio()

def test_obtener_equipos_sin_palmares(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarCompeticion("primera")

	conexion.insertarTituloEquipo(("atleti-madrid", "primera", "Primera", 10, "2019"))

	for numero in range(1,11):

		conexion.insertarEquipo(f"atleti-madrid-{numero}")

	equipos=conexion.obtenerEquiposPalmaresVacio()

	assert len(equipos)==10