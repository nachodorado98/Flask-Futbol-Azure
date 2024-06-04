import pytest

from src.utils import limpiarCodigoImagen, limpiarFecha, limpiarTiempo, normalizarNombre
from src.utils import obtenerCoordenadasEstadio, limpiarTamano

def test_limpiar_codigo_imagen_cadena_vacia():

	assert not limpiarCodigoImagen("")

@pytest.mark.parametrize(["codigo", "resultado"],
	[
		("hola","hola"),
		("imagen.png", "imagen"),
		("fsddfg/codigo.jpg/dgfd755", "codigo")
	]
)
def test_limpiar_codigo_imagen(codigo, resultado):

	assert limpiarCodigoImagen(codigo)==resultado

@pytest.mark.parametrize(["fecha"],
	[("",),("fecha",),("2019-06-22",),("22/6/19",),("22/13/2019",)]
)
def test_limpiar_fecha_incorrecta(fecha):

	assert not limpiarFecha(fecha)

@pytest.mark.parametrize(["fecha", "resultado"],
	[
		("22/6/2019", "2019-06-22"),
		("13/12/2023","2023-12-13")
	]
)
def test_limpiar_fecha(fecha, resultado):

	assert limpiarFecha(fecha)==resultado

@pytest.mark.parametrize(["tiempo"],
	[("",),("tiempo",),("tiempo meses",),("hola anos",)]
)
def test_limpiar_tiempo_incorrecto(tiempo):

	assert not limpiarTiempo(tiempo)

@pytest.mark.parametrize(["tiempo", "resultado"],
	[
		("10 años", 10),
		("1 meses", 1),
		("10 meses años", 10),
	]
)
def test_limpiar_tiempo(tiempo, resultado):

	assert limpiarTiempo(tiempo)==resultado

@pytest.mark.parametrize(["nombre", "nombre_normalizado"],
	[
		("Cívitas Metropolitano", "Civitas Metropolitano"),
		("El Molinón", "El Molinon"),
		("Estádio Do Dragão", "Estadio Do Dragao")
	]
)
def test_normalizar_nombre(nombre, nombre_normalizado):

	assert normalizarNombre(nombre)==nombre_normalizado

@pytest.mark.parametrize(["estadio"],
	[
		("Cívitas Metropolitano",),
		("Estadio El Molinón-Enrique Castro Quini",),
		("Estádio Do Dragão",),
		("Estadio La Rosaleda",),
		("Municipal Football Santa Amalia",),
		("estadio afdhfdhfghgfja",)
	]
)
def test_obtener_coordenadas_estadio(estadio):

	coordenadas=obtenerCoordenadasEstadio(estadio)

	assert isinstance(coordenadas, tuple)

def test_limpiar_tamano_vacio():

	tamano_limpio=limpiarTamano("")

	assert tamano_limpio.count(None)==2

@pytest.mark.parametrize(["tamano"],
	[("105 x 10",),("105x10",),("105 X 10",),("105X10",),("105 X 10 metros",),("105 x 10 metros",)]
)
def test_limpiar_tamano(tamano):

	tamano_limpio=limpiarTamano(tamano)

	assert tamano_limpio.count(None)==0