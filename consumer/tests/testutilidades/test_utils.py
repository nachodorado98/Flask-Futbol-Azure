import pytest
import os

from src.utilidades.utils import enviarCorreo, correo_enviado, convertirMensaje, obtenerClave, obtenerCorreoUsuarioNombre
from src.utilidades.utils import crearCarpetaDataLakeUsuario, crearCarpetaDataLakeUsuarios, listarImagenesCarpetaDatalake
from src.utilidades.utils import existe_imagen_datalake, eliminarImagenDatalake

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

def test_listar_imagenes_carpeta_datalake_carpeta_no_existe(datalake, entorno):

	assert not datalake.existe_carpeta(entorno, "usuarios/no_existo/imagenes")

	assert not listarImagenesCarpetaDatalake("no_existo", entorno)

	datalake.cerrarConexion()

def test_listar_imagenes_carpeta_datalake_imagenes_no_existen(datalake, entorno):

	assert datalake.existe_carpeta(entorno, "usuarios/nacho/imagenes")

	assert not listarImagenesCarpetaDatalake("nacho", entorno)

	datalake.cerrarConexion()

def borrarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		os.rmdir(ruta)

def crearCarpeta(ruta:str)->None:

	if not os.path.exists(ruta):

		os.mkdir(ruta)

def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			os.remove(os.path.join(ruta, archivo))

def crearArchivoTXT(ruta:str, nombre:str)->None:

	ruta_archivo=os.path.join(ruta, nombre)

	with open(ruta_archivo, "w") as file:

	    file.write("Nacho")

def test_listar_imagenes_carpeta_datalake(datalake, entorno):

	ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

	nombre_archivo="archivo.txt"

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	crearArchivoTXT(ruta_carpeta, nombre_archivo)

	assert datalake.existe_carpeta(entorno, "usuarios/nacho/imagenes")

	datalake.subirArchivo(entorno, "usuarios/nacho/imagenes", ruta_carpeta, nombre_archivo)

	archivos=listarImagenesCarpetaDatalake("nacho", entorno)

	assert nombre_archivo in archivos

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

	datalake.cerrarConexion()

def test_existe_imagen_datalake_carpeta_no_existe(datalake, entorno):

	assert not datalake.existe_carpeta(entorno, "usuarios/no_existo/imagenes")

	assert not existe_imagen_datalake("no_existo", "archivo.txt", entorno)

	datalake.cerrarConexion()

def test_existe_imagen_datalake_imagen_no_existe(datalake, entorno):

	assert datalake.existe_carpeta(entorno, "usuarios/nacho/imagenes")

	assert not existe_imagen_datalake("nacho", "nacho.txt", entorno)

	datalake.cerrarConexion()

def test_existe_imagen_datalake(datalake, entorno):

	assert datalake.existe_carpeta(entorno, "usuarios/nacho/imagenes")

	assert existe_imagen_datalake("nacho", "archivo.txt", entorno)

	datalake.cerrarConexion()

def test_eliminar_imagen_datalake_carpeta_no_existe(datalake, entorno):

	assert not datalake.existe_carpeta(entorno, "usuarios/no_existo/imagenes")

	assert not eliminarImagenDatalake("no_existo", "archivo.txt", entorno)

	datalake.cerrarConexion()

def test_eliminar_imagen_datalake_imagen_no_existe(datalake, entorno):

	assert datalake.existe_carpeta(entorno, "usuarios/nacho/imagenes")

	assert not existe_imagen_datalake("nacho", "nacho.txt", entorno)

	assert not eliminarImagenDatalake("nacho", "nacho.txt", entorno)

	datalake.cerrarConexion()

def test_existe_imagen_datalake(datalake, entorno):

	assert datalake.existe_carpeta(entorno, "usuarios/nacho/imagenes")

	assert existe_imagen_datalake("nacho", "archivo.txt", entorno)

	assert eliminarImagenDatalake("nacho", "archivo.txt", entorno)

	assert not existe_imagen_datalake("nacho", "archivo.txt", entorno)

	datalake.cerrarConexion()