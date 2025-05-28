import pytest

def test_tabla_ciudades_llena(conexion):

	conexion.c.execute("SELECT * FROM ciudades")

	assert conexion.c.fetchall()

def test_obtener_ciudades_pais_no_existe(conexion):

	assert not conexion.obtenerCiudadesPais("No existo")

def test_obtener_ciudades_pais(conexion):

	assert conexion.obtenerCiudadesPais("España")

@pytest.mark.parametrize(["poblacion", "cantidad"],
	[(10000, 650),(100000, 61),(1000000, 2)]
)
def test_obtener_ciudades_pais_poblacion_limite(conexion, poblacion, cantidad):

	ciudades=conexion.obtenerCiudadesPais("España", poblacion)

	assert len(ciudades)==cantidad

@pytest.mark.parametrize(["ciudad"],
	[("jkjkjkjjk",), ("MADRID",), ("barna",), ("londres",), ("Andorra La Vella",), ("Tokio",)]
)
def test_obtener_codigo_ciudad_no_existe(conexion, ciudad):

	assert not conexion.obtenerCodigoCiudad(ciudad)

@pytest.mark.parametrize(["ciudad", "codigo_ciudad"],
	[
		("Tokyo", 1),
		("Delhi", 3),
		("Londres", 34),
		("Porto", 2438),
		("Barcelona", 160),
		("Andorra la Vella", 809),
		("Madrid", 103),
		("Merida Mex", 917)
	]
)
def test_obtener_codigo_ciudad(conexion, ciudad, codigo_ciudad):

	assert conexion.obtenerCodigoCiudad(ciudad)==codigo_ciudad

@pytest.mark.parametrize(["codigo_ciudad"],
	[(0,), (100000,), (-1,), (24354366,)]
)
def test_existe_codigo_ciudad_no_existe(conexion, codigo_ciudad):

	assert not conexion.existe_codigo_ciudad(codigo_ciudad)

@pytest.mark.parametrize(["codigo_ciudad"],
	[(1,), (10000,), (22,), (13,), (103,)]
)
def test_existe_codigo_ciudad(conexion, codigo_ciudad):

	assert conexion.existe_codigo_ciudad(codigo_ciudad)

def test_obtener_ciudad_no_existe_ciudad(conexion):

	assert not conexion.obtenerCiudad("no_existo", "es")

def test_obtener_ciudad_no_existe_estadio(conexion):

	assert not conexion.obtenerCiudad("Madrid", "es")

def test_obtener_ciudad_no_existe_codigo_pais(conexion_entorno):

	conexion_entorno.c.execute("UPDATE estadios SET Codigo_Pais=NULL")

	assert not conexion_entorno.obtenerCiudad("Madrid", "es")

def test_obtener_ciudad(conexion_entorno):

	assert conexion_entorno.obtenerCiudad("Madrid", "es")

@pytest.mark.parametrize(["ciudad", "pais"],
	[
		("Tokyo", "Pais"),
		("No Existo", "España"),
		("porto", "Portugal"),
		("BaRcElOnA",  "España"),
		("Madrid", "españa"),
		("Merida", "Mexico")
	]
)
def test_obtener_codigo_ciudad_pais_no_existe(conexion, ciudad, pais):

	assert not conexion.obtenerCodigoCiudadPais(ciudad, pais)

@pytest.mark.parametrize(["ciudad", "pais", "codigo_ciudad"],
	[
		("Tokyo", "Japón", 1),
		("Delhi", "India", 3),
		("Londres", "Reino Unido", 34),
		("Porto", "Portugal", 2438),
		("Barcelona", "España", 160),
		("Andorra la Vella", "Andorra", 809),
		("Madrid", "España", 103),
		("Merida Mex", "México", 917),
		("Merida", "España", 5809)
	]
)
def test_obtener_codigo_ciudad_pais(conexion, ciudad, pais, codigo_ciudad):

	assert conexion.obtenerCodigoCiudadPais(ciudad, pais)==codigo_ciudad

@pytest.mark.parametrize(["codigo_ciudad"],
	[(0,),(-1,),(100000,)]
)
def test_obtener_coordenadas_ciudad_no_existe(conexion, codigo_ciudad):

	assert not conexion.obtenerCoordenadasCiudad(codigo_ciudad)

@pytest.mark.parametrize(["codigo_ciudad"],
	[(1,),(103,),(34,),(160,)]
)
def test_obtener_coordenadas_ciudad(conexion, codigo_ciudad):

	coordenadas=conexion.obtenerCoordenadasCiudad(codigo_ciudad)

	assert len(coordenadas)==2