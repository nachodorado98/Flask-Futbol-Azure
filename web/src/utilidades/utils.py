import re
from datetime import datetime
from passlib.context import CryptContext
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict

from .configutils import CORREO_LOGIN, CONTRASENA_LOGIN, SERVIDOR_CORREO, PUERTO_CORREO

def usuario_correcto(usuario:str)->bool:

    return bool(usuario and usuario.isalnum())

def nombre_correcto(nombre:str)->bool:

    return bool(nombre and nombre.isalpha())

def apellido_correcto(apellido:str)->bool:

    return nombre_correcto(apellido)

def contrasena_correcta(contrasena:str)->bool:

    if not contrasena:

        return None

    patron=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    return bool(re.match(patron, contrasena))

def fecha_correcta(fecha:str, minimo:str="1900-01-01")->bool:

    hoy=datetime.today()

    ano_maximo=hoy.year-18

    fecha_maxima=f"{ano_maximo}-{hoy.month:02d}-{hoy.day:02d}"

    if hoy.month==2 and hoy.day==29:

        if not (ano_maximo%4==0 and (ano_maximo%100!=0 or ano_maximo%400==0)):

            fecha_maxima=f"{ano_maximo}-02-28"

    try:

        fecha_nacimiento=datetime.strptime(fecha, "%Y-%m-%d")

        return bool(datetime.strptime(minimo, "%Y-%m-%d")<=fecha_nacimiento<=datetime.strptime(fecha_maxima, "%Y-%m-%d"))

    except Exception:

        return False

def equipo_correcto(equipo:str)->bool:

    if not equipo:

        return False

    return bool(re.fullmatch(r"[a-zA-Z0-9-]+", equipo))

def correo_correcto(correo:str)->bool:

    if not correo:

        return False

    patron=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return bool(re.match(patron, correo))

def datos_correctos(usuario:str, nombre:str, apellido:str, contrasena:str, fecha_nacimiento:str, equipo:str, correo:str)->bool:

    return (usuario_correcto(usuario) and
            nombre_correcto(nombre) and
            apellido_correcto(apellido) and
            contrasena_correcta(contrasena) and
            fecha_correcta(fecha_nacimiento) and
            equipo_correcto(equipo) and
            correo_correcto(correo))

def generarHash(contrasena:str)->str:

    objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

    return objeto_hash.hash(contrasena)

def comprobarHash(contrasena:str, contrasena_hash:str)->bool:

    objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

    return objeto_hash.verify(contrasena, contrasena_hash)

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

def anadirPuntos(numero:str)->str:

    numero_con_puntos=""

    for indice, digito in enumerate(numero[::-1], 1):

        numero_con_puntos+=digito

        if indice%3==0 and indice!=len(numero[::-1]):

            numero_con_puntos+="."

    return numero_con_puntos[::-1]

def limpiarResultadosPartidos(partidos:List[tuple])->Dict:

    partidos_ganados=len(list(filter(lambda partido: partido[-3]==1, partidos)))

    partidos_perdidos=len(list(filter(lambda partido: partido[-2]==1, partidos)))

    partidos_empatados=len(list(filter(lambda partido: partido[-1]==1, partidos)))

    return {"ganados":partidos_ganados,
            "perdidos": partidos_perdidos,
            "empatados": partidos_empatados}