import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from typing import Optional, Dict

from .configutils import CORREO_LOGIN, CONTRASENA_LOGIN, SERVIDOR_CORREO, PUERTO_CORREO

from src.datalake.conexion_data_lake import ConexionDataLake

from src.config import CONTENEDOR

def enviarCorreo(destino:str, asunto:str, template_correo:str,
				origen:str=CORREO_LOGIN, contrasena:str=CONTRASENA_LOGIN)->None:

	mensaje=MIMEMultipart()

	mensaje["From"]=origen
	mensaje["To"]=destino
	mensaje["Subject"]=asunto

	mensaje.attach(MIMEText(template_correo, "html"))

	try:

		servidor=smtplib.SMTP(SERVIDOR_CORREO, PUERTO_CORREO)

		servidor.starttls()

		servidor.login(origen, contrasena)

		cuerpo=mensaje.as_string()

		servidor.sendmail(origen, destino, cuerpo)

	except Exception:

		raise Exception(f"Error al enviar el correo a {destino}")

	finally:

		servidor.quit()

def correo_enviado(destino:str, nombre:str, origen:str=CORREO_LOGIN, contrasena:str=CONTRASENA_LOGIN)->bool:

	asunto="¡Bienvenido a nuestra familia!"

	html="""
			<!DOCTYPE html>
			<html lang="es">
			<head>
				<meta charset="UTF-8">
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<title>Correo Aplicacion Futbol</title>
				<style>
					body {{
						font-family: Arial, sans-serif;
						background-color: #f4f4f4;
						margin: 0;
						padding: 0;
					}}
					.container {{
						max-width: 600px;
						margin: 0 auto;
						background-color: #ffffff;
						padding: 20px;
						box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
					}}
					.header {{
						text-align: center;
						padding: 20px;
						background-color: #333333;
						color: #ffffff;
					}}
					.content {{
						padding: 20px;
						color: #333333;
					}}
					.content h1 {{
						font-size: 24px;
						color: #333333;
					}}
					.content p {{
						font-size: 16px;
						line-height: 1.5;
						color: #666666;
					}}
					.content a {{
						color: #333333;
						text-decoration: none;
					}}
					.footer {{
						text-align: center;
						padding: 20px;
						background-color: #f4f4f4;
						color: #777777;
						font-size: 12px;
					}}
				</style>
			</head>
			<body>
				<div class="container">
					<div class="header">
						<h1>Futbol App</h1>
					</div>
					<div class="content">
						<h1>Hola, {nombre}:</h1>
						<p>Te escribimos para confirmar que tu registro en nuestro aplicación ha sido exitoso.</p>
						<p>Gracias por unirte a nosotros. Ahora puedes disfrutar de todas las funcionalidades de nuestra web de futbol.</p>
						<p>Atentamente,<br>el equipo de Futbol App<br></p>
					</div>
					<div class="footer">
						<p>Este es un correo electrónico automatizado. Por favor, no respondas a este mensaje.</p>
						<p>&copy; 2024 Futbol App. Todos los derechos reservados.</p>
					</div>
				</div>
			</body>
			</html>
			"""

	try:

		enviarCorreo(destino, asunto, html.format(nombre=nombre), origen, contrasena)

		return True

	except Exception:

		return False

def convertirMensaje(mensaje:str)->Optional[Dict]:

	try:

		return json.loads(mensaje)

	except Exception as e:

		print(f"Error convirtiendo mensaje a diccionario: {e}")
		return

def obtenerClave(mensaje:str, clave:str)->Optional[str]:

	try:

		mensaje_diccionario=convertirMensaje(mensaje)

		return mensaje_diccionario[clave]

	except Exception:

		return

def obtenerCorreoUsuarioNombre(mensaje:str)->Optional[tuple]:

	correo=obtenerClave(mensaje, "correo")
	usuario=obtenerClave(mensaje, "usuario")
	nombre=obtenerClave(mensaje, "nombre")

	return (correo, usuario, nombre) if correo and usuario and nombre else None

def crearCarpetaDataLakeUsuario()->bool:

	try:

		dl=ConexionDataLake()

		if not dl.existe_carpeta(CONTENEDOR, "usuarios"):

			dl.crearCarpeta(CONTENEDOR, "usuarios")

		dl.cerrarConexion()

		return True

	except Exception as e:

		print(f"Error en conexion con datalake: {e}")

		return False

def crearCarpetaDataLakeUsuarios(usuario:str)->bool:

	try:

		dl=ConexionDataLake()

		if not dl.existe_carpeta(CONTENEDOR, f"usuarios/{usuario}"):

			dl.crearCarpeta(CONTENEDOR, f"usuarios/{usuario}/perfil")

			dl.crearCarpeta(CONTENEDOR, f"usuarios/{usuario}/imagenes")

		dl.cerrarConexion()

		return True

	except Exception as e:

		print(f"Error en conexion con datalake: {e}")

		return False