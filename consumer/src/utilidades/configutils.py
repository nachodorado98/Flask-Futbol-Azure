import os

CORREO_LOGIN=os.environ.get("EMAIL_ACCOUNT") # Correo para enviar los correos de la aplicacion
CONTRASENA_LOGIN=os.environ.get("EMAIL_PASSWORD") # Contrasena del correo anterior
SERVIDOR_CORREO="smtp.gmail.com"
PUERTO_CORREO=587