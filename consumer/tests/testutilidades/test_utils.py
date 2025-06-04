import pytest

from src.utilidades.utils import enviarCorreo, correo_enviado, convertirMensaje, obtenerClave, obtenerCorreoUsuarioNombre
from src.utilidades.utils import crearCarpetaDataLakeUsuario, crearCarpetaDataLakeUsuarios

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

def test_obtener_clave_error():

	assert not obtenerClave("mensaje", "clave")

def test_obtener_clave_error_claves():

	assert not obtenerClave('{"mensaje":"Hola"}', "clave")

def test_obtener_clave():

	clave=obtenerClave('{"clave":"clave"}', "clave")

	assert clave=="clave"

def test_obtener_correo_usuario_nombre_error():

	assert not obtenerCorreoUsuarioNombre("mensaje")

def test_obtener_correo_usuario_nombre_error_claves():

	assert not obtenerCorreoUsuarioNombre('{"mensaje":"Hola"}')

def test_obtener_correo_usuario_nombre():

	correo, usuario, nombre=obtenerCorreoUsuarioNombre('{"correo":"correo", "usuario":"usuario", "nombre":"nombre"}')

	assert correo=="correo"
	assert usuario=="usuario"
	assert nombre=="nombre"

def test_crear_carpeta_data_lake_usuario_no_existe(datalake, entorno):

	datalake.eliminarCarpeta(entorno, "usuarios")

	assert not datalake.existe_carpeta(entorno, "usuarios")

	crearCarpetaDataLakeUsuario(entorno)

	assert datalake.existe_carpeta(entorno, "usuarios")

	datalake.cerrarConexion()

def test_crear_carpeta_data_lake_usuario_existe(datalake, entorno):

	assert datalake.existe_carpeta(entorno, "usuarios")

	crearCarpetaDataLakeUsuario(entorno)

	assert datalake.existe_carpeta(entorno, "usuarios")

	datalake.cerrarConexion()

def test_crear_carpeta_data_lake_usuarios_no_existe(datalake, entorno):

	datalake.eliminarCarpeta(entorno, "usuarios")

	crearCarpetaDataLakeUsuario(entorno)

	assert datalake.existe_carpeta(entorno, "usuarios")
	assert not datalake.existe_carpeta(entorno, "usuarios/nacho")

	crearCarpetaDataLakeUsuarios("nacho", entorno)

	assert datalake.existe_carpeta(entorno, "usuarios/nacho")

	datalake.cerrarConexion()

def test_crear_carpeta_data_lake_usuarios_existe(datalake, entorno):

	assert datalake.existe_carpeta(entorno, "usuarios")
	assert datalake.existe_carpeta(entorno, "usuarios/nacho")

	crearCarpetaDataLakeUsuarios("nacho", entorno)

	assert datalake.existe_carpeta(entorno, "usuarios/nacho")

	datalake.cerrarConexion()