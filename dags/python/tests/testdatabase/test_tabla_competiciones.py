import pytest

def test_tabla_competiciones_vacia(conexion):

	conexion.c.execute("SELECT * FROM competiciones")

	assert not conexion.c.fetchall()

def test_insertar_competicion(conexion):

	conexion.insertarCompeticion("competicion")

	conexion.c.execute("SELECT * FROM competiciones")

	assert len(conexion.c.fetchall())==1

def test_existe_competicion_no_existe(conexion):

	assert not conexion.existe_competicion("competicion")

def test_existe_competicion_existe(conexion):

	conexion.insertarCompeticion("competicion")

	assert conexion.existe_competicion("competicion")

def test_actualizar_datos_competicion_no_existe(conexion):

	assert not conexion.existe_competicion("competicion")

	datos=["Primera", "primera", "es"]

	conexion.actualizarDatosCompeticion(datos, "competicion")

	assert not conexion.existe_competicion("competicion")

@pytest.mark.parametrize(["datos_nuevos"],
	[
		(["Primera", "primera", "es"],),
		(["Segunda", "seg", "es"],),
		(["Primera", None, "es"],),
		(["Primera", "primera", None],),
		([None, "primera", "es"],)
	]
)
def test_actualizar_datos_competicion(conexion, datos_nuevos):

	conexion.insertarCompeticion("primera")

	assert conexion.existe_competicion("primera")

	conexion.actualizarDatosCompeticion(datos_nuevos, "primera")

	conexion.c.execute("SELECT * FROM competiciones WHERE Competicion_Id='primera'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]==datos_nuevos[0]
	assert datos_actualizados["codigo_logo"]==datos_nuevos[1]
	assert datos_actualizados["codigo_pais"]==datos_nuevos[2]

def test_obtener_competiciones_no_hay(conexion):

	assert not conexion.obtenerCompeticiones()

def test_obtener_competiciones(conexion):

	for numero in range(1,11):

		conexion.insertarCompeticion(f"primera-{numero}")

	competiciones=conexion.obtenerCompeticiones()

	assert len(competiciones)==10

def test_obtener_competiciones_equipos_no_hay(conexion):

	assert not conexion.obtenerCompeticionesEquipos()

def test_obtener_competiciones_equipos_unicas(conexion):

	for numero in range(1,11):

		conexion.c.execute(f"""INSERT INTO equipos (Equipo_Id, Codigo_Competicion) VALUES('atletico-madrid-{numero}', 'primera-{numero}')""")

	conexion.confirmar()

	competiciones=conexion.obtenerCompeticionesEquipos()

	assert len(competiciones)==10

def test_obtener_competiciones_equipos_duplicados(conexion):

	for numero in range(1,11):

		conexion.c.execute(f"""INSERT INTO equipos (Equipo_Id, Codigo_Competicion) VALUES('atletico-madrid-{numero}', 'primera')""")

	conexion.confirmar()

	competiciones=conexion.obtenerCompeticionesEquipos()

	assert len(competiciones)==1

def test_obtener_codigo_logo_competiciones_no_hay(conexion):

	assert not conexion.obtenerCodigoLogoCompeticiones()

@pytest.mark.parametrize(["datos", "numero_logos"],
	[
		([("primera", "primera-ea"), ("segunda", "segundadiv"), ("bundesliga", "bundes")], 3),
		([("primera", "primera-ea"), ("segunda", "segundadiv"), ("bundesliga", None)], 2),
		([("primera", "primera-ea"), ("segunda", "segundadiv"), ("bundesliga", None), ("premier", "logo")], 3),
		([("primera", "primera-ea"), ("segunda", None), ("bundesliga", None)], 1)
	]
)
def test_obtener_codigo_logo_competiciones(conexion, datos, numero_logos):

	for competicion, logo in datos:

		conexion.insertarCompeticion(competicion)

		conexion.actualizarDatosCompeticion(["Nombre", logo, "Pais"], competicion)

	logos=conexion.obtenerCodigoLogoCompeticiones()

	assert len(logos)==numero_logos

def test_obtener_codigo_paises_no_hay(conexion):

	assert not conexion.obtenerCodigoPaises()

@pytest.mark.parametrize(["datos", "numero_paises"],
	[
		([("primera", "es"), ("segunda", "es"), ("bundesliga", "al")], 2),
		([("primera", "es"), ("segunda", "as"), ("bundesliga", None)], 2),
		([("primera", "es"), ("segunda", "es"), ("bundesliga", None), ("premier", "en")], 2),
		([("primera", "es"), ("segunda", None), ("bundesliga", None)], 1)
	]
)
def test_obtener_codigo_paises(conexion, datos, numero_paises):

	for competicion, pais in datos:

		conexion.insertarCompeticion(competicion)

		conexion.actualizarDatosCompeticion(["Nombre", "Logo", pais], competicion)

	paises=conexion.obtenerCodigoPaises()

	assert len(paises)==numero_paises

def test_obtener_competicion_por_logo_no_existe(conexion):

	assert not conexion.obtenerCompeticionPorLogo("primera-ea")

def test_obtener_competicion_por_logo(conexion):

	conexion.insertarCompeticion("primera")

	conexion.actualizarDatosCompeticion(["Nombre", "primera-ea", "Pais"], "primera")

	assert conexion.obtenerCompeticionPorLogo("primera-ea")=="primera"

def test_actualizar_titulo_competicion_no_existe(conexion):

	assert not conexion.existe_competicion("competicion")

	conexion.actualizarTituloCompeticion("1", "competicion")

	assert not conexion.existe_competicion("competicion")

def test_actualizar_titulo_competicion(conexion):

	conexion.insertarCompeticion("primera")

	assert conexion.existe_competicion("primera")

	conexion.actualizarTituloCompeticion("1", "primera")

	conexion.c.execute("SELECT * FROM competiciones WHERE Competicion_Id='primera'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["codigo_titulo"]=="1"

def test_obtener_codigo_titulo_competiciones_no_hay(conexion):

	assert not conexion.obtenerCodigoTituloCompeticiones()

@pytest.mark.parametrize(["datos", "numero_titulos"],
	[
		([("primera","1"),("segunda","22"),("champions",None)], 2),
		([("primera","1"),("segunda","22"),("champions","13")], 3),
		([("primera","1"),("segunda",None),("champions","no_foto")], 2),
		([("primera","1"),("segunda","22"),("champions","nofoto")], 2),
		([("primera","1"),("segunda",None),("champions","a_nofoto_b")], 1)
	]
)
def test_obtener_codigo_titulo_competiciones(conexion, datos, numero_titulos):

	for competicion, codigo_titulo in datos:

		conexion.insertarCompeticion(competicion)

		conexion.actualizarTituloCompeticion(codigo_titulo, competicion)
	
	codigos_titulos=conexion.obtenerCodigoTituloCompeticiones()

	assert len(codigos_titulos)==numero_titulos

def test_obtener_competiciones_sin_nombre_no_hay(conexion):

	assert not conexion.obtenerCompeticionesNombreVacio()

def test_obtener_competiciones_sin_nombre(conexion):

	conexion.insertarCompeticion("primera")

	conexion.actualizarDatosCompeticion(["Primera", "ea", "es"], "primera")

	for numero in range(1,11):

		conexion.insertarCompeticion(f"primera-{numero}")

	competiciones=conexion.obtenerCompeticionesNombreVacio()

	assert len(competiciones)==10

def test_obtener_competiciones_sin_campeones_no_hay(conexion):

	assert not conexion.obtenerCompeticionesCampeonesVacio()

def test_obtener_competiciones_sin_campeones(conexion):

	conexion.insertarCompeticion("primera")

	datos=["primera", 2025, "atleti"]

	conexion.insertarCampeonCompeticion(datos)

	for numero in range(1,11):

		conexion.insertarCompeticion(f"primera-{numero}")

	competiciones=conexion.obtenerCompeticionesCampeonesVacio()

	assert len(competiciones)==10