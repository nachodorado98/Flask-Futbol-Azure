import pytest
from src.utilidades.utils import enviarCorreo, correo_enviado, convertirMensaje, obtenerCorreoNombre

def HTML()->str:

	return 	"""<html>
					<body>
						<h1>¡Hola!</h1>
						<p>Este es un <b>correo electrónico</b> enviado desde un script</p>
					</body>
				</html>
			"""

def test_enviar_correo_error():

	with pytest.raises(Exception):

		enviarCorreo("ignaciodoradoruiz@gmail.com", "asunto", HTML(), "ignaciodoradoruiz@gmail.com", "1234")

def test_enviar_correo():

	assert not enviarCorreo("ignaciodoradoruiz@gmail.com", "asunto", HTML())

def test_correo_enviado_no_enviado():

	assert not correo_enviado("ignaciodoradoruiz@gmail.com", "nombre", "ignaciodoradoruiz@gmail.com", "1234")

def test_correo_enviado():

	assert correo_enviado("ignaciodoradoruiz@gmail.com", "nombre")

def test_convertir_mensaje_error():

	assert not convertirMensaje("mensaje")

def test_convertir_mensaje():

	mensaje_diccionario=convertirMensaje('{"mensaje":"Hola"}')

	assert isinstance(mensaje_diccionario, dict)
	assert mensaje_diccionario=={"mensaje":"Hola"}

def test_obtener_correo_nombre_error():

	assert not obtenerCorreoNombre("mensaje")

def test_obtener_correo_nombre_error_claves():

	assert not obtenerCorreoNombre('{"mensaje":"Hola"}')

def test_obtener_correo_nombre_error_claves():

	correo, nombre=obtenerCorreoNombre('{"correo":"correo", "nombre":"nombre"}')

	assert correo=="correo"
	assert nombre=="nombre"