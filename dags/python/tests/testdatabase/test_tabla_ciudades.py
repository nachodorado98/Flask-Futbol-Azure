import pytest

def test_tabla_ciudades_llena(conexion):
 
	conexion.c.execute("SELECT * FROM ciudades")
 
	assert conexion.c.fetchall()

def test_obtener_ciudades_mas_cercanas_muy_lejanas(conexion):

	ciudades=conexion.obtenerCiudadesMasCercanas(0, 0)

	assert ciudades[0][2]>500
	assert ciudades[1][2]>500

@pytest.mark.parametrize(["latitud", "longitud"],
	[
		(40.4523667, -3.6907254),
		(39.4745279, -0.35815663617491666),
		(37.383878, -5.970467),
		(40.34037465, -3.760651172703595)
	]
)
def test_obtener_ciudades_mas_cercanas_una_ciudad(conexion, latitud, longitud):

	ciudades=conexion.obtenerCiudadesMasCercanas(latitud, longitud)

	assert len(ciudades)==1

@pytest.mark.parametrize(["latitud", "longitud"],
	[
		(40.436052950000004, -3.599715809726445),
		(37.35653544999999, -5.981756556248882),
		(47.8163956, 12.998243910546709),
		(40.325724699999995, -3.714932645209058)
	]
)
def test_obtener_ciudades_mas_cercanas(conexion, latitud, longitud):

	ciudades=conexion.obtenerCiudadesMasCercanas(latitud, longitud)

	assert len(ciudades)==2