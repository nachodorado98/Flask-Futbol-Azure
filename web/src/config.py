from .datalake.confconexiondatalake import CUENTA_DL, CLAVE_DL, CONTENEDOR_DL

CUENTA=CUENTA_DL
CLAVE=CLAVE_DL
CONTENEDOR=CONTENEDOR_DL

URL_DATALAKE=f"https://{CUENTA}.blob.core.windows.net/{CONTENEDOR}"
URL_DATALAKE_ESCUDOS=f"{URL_DATALAKE}/escudos/"
URL_DATALAKE_ESTADIOS=f"{URL_DATALAKE}/estadios/"
URL_DATALAKE_ENTRENADORES=f"{URL_DATALAKE}/entrenadores/"
URL_DATALAKE_PRESIDENTES=f"{URL_DATALAKE}/presidentes/"
URL_DATALAKE_PAISES=f"{URL_DATALAKE}/paises/"
URL_DATALAKE_COMPETICIONES=f"{URL_DATALAKE}/competiciones/"
URL_DATALAKE_JUGADORES=f"{URL_DATALAKE}/jugadores/"
URL_DATALAKE_SELECCIONES=f"{URL_DATALAKE}/selecciones/"
URL_DATALAKE_USUARIOS=f"{URL_DATALAKE}/usuarios/"

ESCUDOS="escudos"
ENTRENADORES="entrenadores"
PRESIDENTES="presidentes"
ESTADIOS="estadios"
COMPETICIONES="competiciones"
PAISES="paises"
JUGADORES="jugadores"
SELECCIONES="selecciones"
USUARIOS="usuarios"
PERFIL=f"{USUARIOS}/perfil"
IMAGENES=f"{USUARIOS}/imagenes"

CARPETAS=[ESCUDOS, ENTRENADORES, PRESIDENTES, ESTADIOS, COMPETICIONES, PAISES, JUGADORES, SELECCIONES, USUARIOS, PERFIL, IMAGENES]