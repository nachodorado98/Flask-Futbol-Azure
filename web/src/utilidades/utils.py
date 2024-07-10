import re
from datetime import datetime
from passlib.context import CryptContext

def usuario_correcto(usuario:str)->bool:

    return bool(usuario and usuario.isalnum())

def nombre_correcto(nombre:str)->bool:

    return bool(nombre and nombre.isalpha())

def apellido_correcto(apellido:str)->bool:

    return nombre_correcto(apellido)

def contrasena_correcta(contrasena:str)->bool:

    if not contrasena:

        return None

    patron=re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

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

    return bool(re.fullmatch(r'[a-zA-Z0-9-]+', equipo))

def datos_correctos(usuario:str, nombre:str, apellido:str, contrasena:str, fecha_nacimiento:str, equipo:str)->bool:

    return (usuario_correcto(usuario) and
            nombre_correcto(nombre) and
            apellido_correcto(apellido) and
            contrasena_correcta(contrasena) and
            fecha_correcta(fecha_nacimiento) and
            equipo_correcto(equipo))

def generarHash(contrasena:str)->str:

    objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

    return objeto_hash.hash(contrasena)

def comprobarHash(contrasena:str, contrasena_hash:str)->bool:

    objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

    return objeto_hash.verify(contrasena, contrasena_hash)