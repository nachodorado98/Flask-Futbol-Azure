import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_equipo import ScraperEquipo
from src.scrapers.excepciones_scrapers import PaginaError, EquipoError

def test_crear_objeto_scraper_equipo():

	scraper=ScraperEquipo("equipo")

def test_scraper_equipo_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperEquipo("redireccion_equipo")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_equipo_realizar_peticion(scraper_equipo):

	contenido=scraper_equipo._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_equipo_obtener_tabla_info(scraper_equipo):

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	assert tabla_info is not None

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),("kakamega-homeboyz",),("sporting-gijon",)]
)
def test_scraper_equipo_obtener_informacion_nombre_alias_siglas(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	nombre_alias_siglas=scraper_equipo._ScraperEquipo__informacion_nombre(tabla_info)

	assert len(nombre_alias_siglas)==3
	assert "" not in nombre_alias_siglas

def test_scraper_equipo_obtener_informacion_datos(scraper_equipo):

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	datos=scraper_equipo._ScraperEquipo__informacion_datos(tabla_info)

	assert datos is not None

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),("kakamega-homeboyz",),("sporting-gijon",)]
)
def test_scraper_equipo_obtener_tabla_general(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	datos=scraper_equipo._ScraperEquipo__informacion_datos(tabla_info)

	tabla_general=scraper_equipo._ScraperEquipo__tabla_general(datos)

	assert len(tabla_general)==5
	assert "" not in tabla_general

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),("kakamega-homeboyz",),("sporting-gijon",)]
)
def test_scraper_equipo_obtener_informacion_general(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	general=scraper_equipo._ScraperEquipo__informacion_general(tabla_info)

	assert len(general)==5
	assert "" not in general

def test_scraper_equipo_obtener_informacion_lista(scraper_equipo):

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	lista=scraper_equipo._ScraperEquipo__informacion_lista(tabla_info)

	assert lista is not None

@pytest.mark.parametrize(["equipo"],
	[("seleccion-santa-amalia",),("kakamega-homeboyz",),("cd-valdehornillo-a-senior",)]
)
def test_scraper_equipo_obtener_tabla_presidente_no_presidente(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	lista=scraper_equipo._ScraperEquipo__informacion_lista(tabla_info)

	presidente=scraper_equipo._ScraperEquipo__tabla_presidente(lista)

	assert len(presidente)==9
	assert presidente.count("")==9

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("villarreal",),("sporting-gijon",)]
)
def test_scraper_equipo_obtener_tabla_presidente_datos_correctos(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	lista=scraper_equipo._ScraperEquipo__informacion_lista(tabla_info)

	presidente=scraper_equipo._ScraperEquipo__tabla_presidente(lista)

	assert len(presidente)==9
	assert "" not in presidente

@pytest.mark.parametrize(["equipo"],
	[("albacete",)]
)
def test_scraper_equipo_obtener_tabla_presidente_datos_semi_correctos(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	lista=scraper_equipo._ScraperEquipo__informacion_lista(tabla_info)

	presidente=scraper_equipo._ScraperEquipo__tabla_presidente(lista)

	assert len(presidente)==9
	#assert presidente.count("")==2 # Antes tenia dos datos faltantes pero ahora parece que faltan mas en la web

@pytest.mark.parametrize(["equipo"],
	[("seleccion-santa-amalia",),("kakamega-homeboyz",),("cd-valdehornillo-a-senior",)]
)
def test_scraper_equipo_informacion_presidente_no_presidente(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	presidente=scraper_equipo._ScraperEquipo__informacion_presidente(tabla_info)

	assert len(presidente)==9
	assert presidente.count("")==9

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("villarreal",),("sporting-gijon",)]
)
def test_scraper_equipo_informacion_presidente_datos_correctos(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	presidente=scraper_equipo._ScraperEquipo__informacion_presidente(tabla_info)

	assert len(presidente)==9
	assert "" not in presidente

@pytest.mark.parametrize(["equipo"],
	[("albacete",)]
)
def test_scraper_equipo_informacion_presidente_datos_semi_correctos(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	presidente=scraper_equipo._ScraperEquipo__informacion_presidente(tabla_info)

	assert len(presidente)==9
	#assert presidente.count("")==2 # Antes tenia dos datos faltantes pero ahora parece que faltan mas en la web

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",)]
)
def test_scraper_equipo_obtener_tabla_datos_tecnicos_datos_correctos(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	lista=scraper_equipo._ScraperEquipo__informacion_lista(tabla_info)

	datos_tecnicos=scraper_equipo._ScraperEquipo__tabla_datos_tecnicos(lista)

	assert len(datos_tecnicos)==3
	assert "" not in datos_tecnicos

@pytest.mark.parametrize(["equipo"],
	[("sporting-gijon",)]
)
def test_scraper_equipo_obtener_tabla_datos_tecnicos_dato_faltante(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	lista=scraper_equipo._ScraperEquipo__informacion_lista(tabla_info)

	datos_tecnicos=scraper_equipo._ScraperEquipo__tabla_datos_tecnicos(lista)

	assert len(datos_tecnicos)==3
	#assert datos_tecnicos.count("")==1 # Antes tenia un dato faltante pero ahora parece que lo han añadido en la web

@pytest.mark.parametrize(["equipo"],
	[("kakamega-homeboyz",),("cd-valdehornillo-a-senior",)]
)
def test_scraper_equipo_obtener_tabla_datos_tecnicos_datos_faltantes(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	lista=scraper_equipo._ScraperEquipo__informacion_lista(tabla_info)

	datos_tecnicos=scraper_equipo._ScraperEquipo__tabla_datos_tecnicos(lista)

	assert len(datos_tecnicos)==3
	assert datos_tecnicos.count("")==2

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("albacete",)]
)
def test_scraper_equipo_informacion_datos_tecnicos_datos_correctos(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	datos_tecnicos=scraper_equipo._ScraperEquipo__informacion_datos_tecnicos(tabla_info)

	assert len(datos_tecnicos)==3
	assert "" not in datos_tecnicos

@pytest.mark.parametrize(["equipo"],
	[("sporting-gijon",)]
)
def test_scraper_equipo_informacion_datos_tecnicos_dato_faltante(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	datos_tecnicos=scraper_equipo._ScraperEquipo__informacion_datos_tecnicos(tabla_info)

	assert len(datos_tecnicos)==3
	#assert datos_tecnicos.count("")==1 # Antes tenia un dato faltante pero ahora parece que lo han añadido en la web

@pytest.mark.parametrize(["equipo"],
	[("kakamega-homeboyz",),("cd-valdehornillo-a-senior",)]
)
def test_scraper_equipo_informacion_datos_tecnicos_datos_faltantes(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	datos_tecnicos=scraper_equipo._ScraperEquipo__informacion_datos_tecnicos(tabla_info)

	assert len(datos_tecnicos)==3
	assert datos_tecnicos.count("")==2

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),("kakamega-homeboyz",),("sporting-gijon",), ("albacete",)]
)
def test_scraper_equipo_obtener_data_limpia(equipo):

	scraper_equipo=ScraperEquipo(equipo)

	contenido=scraper_equipo._Scraper__realizarPeticion()

	tabla_info=scraper_equipo._ScraperEquipo__contenido_tabla_info(contenido)

	data_limpia=scraper_equipo._ScraperEquipo__obtenerDataLimpia(tabla_info)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_equipo_obtener_detalle_equipo_error(endpoint):

	scraper=ScraperEquipo(endpoint)

	with pytest.raises(EquipoError):

		scraper.obtenerDetalleEquipo()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),
	("kakamega-homeboyz",),("sporting-gijon",),("albacete",)]
)
def test_scraper_equipo_obtener_detalle_equipo(equipo):

	scraper=ScraperEquipo(equipo)

	df_detalle=scraper.obtenerDetalleEquipo()

	assert isinstance(df_detalle, pd.DataFrame)