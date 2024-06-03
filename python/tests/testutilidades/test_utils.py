import pytest

from src.utils import limpiarCodigoImagen, limpiarFecha, limpiarTiempo

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