import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_equipo_estadio import ScraperEquipoEstadio
from src.scrapers.excepciones_scrapers import PaginaError, EquipoEstadioError

def test_crear_objeto_scraper_equipo_estadio():

	scraper=ScraperEquipoEstadio("equipo")

def test_scraper_equipo_estadio_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperEquipoEstadio("redireccion_equipo")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_equipo_estadio_realizar_peticion(scraper_equipo_estadio):

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

@pytest.mark.parametrize(["equipo"],
	[("kakamega-homeboyz",),("cd-valdehornillo-a-senior",)]
)
def test_scraper_equipo_estadio_obtener_tabla_estadio_no_existe(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	with pytest.raises(EquipoEstadioError):

		scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("seleccion-santa-amalia",),("sporting-gijon",)]
)
def test_scraper_equipo_estadio_obtener_tabla_estadio(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	assert tabla_estadio is not None

def test_scraper_equipo_estadio_obtener_imagen_estadio(scraper_equipo_estadio):

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	imagen_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__imagen_estadio(tabla_estadio)

	assert imagen_estadio.endswith(".png") or imagen_estadio.endswith(".jpg")
	assert "estadio_nofoto" not in imagen_estadio
	assert imagen_estadio.startswith("https://cdn.resfu.com/img_data/estadios/original_new")

def test_scraper_equipo_estadio_obtener_imagen_estadio_no_tiene():

	scraper_equipo_estadio=ScraperEquipoEstadio("seleccion-santa-amalia")

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	imagen_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__imagen_estadio(tabla_estadio)

	assert imagen_estadio.endswith(".jpg") or imagen_estadio.endswith(".png")
	assert "estadio_nofoto" in imagen_estadio
	assert imagen_estadio.startswith("https://cdn.resfu.com/img_data/estadios/original_new")

def test_scraper_equipo_estadio_obtener_informacion_datos_estadio(scraper_equipo_estadio):

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_equipo_estadio._ScraperEquipoEstadio__informacion_datos_estadio(tabla_estadio)

	assert tabla_info_datos is not None

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_scraper_equipo_estadio_obtener_tabla_nombre_ubicacion_datos_correctos(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_equipo_estadio._ScraperEquipoEstadio__informacion_datos_estadio(tabla_estadio)

	nombre_ciudad_direccion=scraper_equipo_estadio._ScraperEquipoEstadio__tabla_nombre_ubicacion(tabla_info_datos)

	assert len(nombre_ciudad_direccion)==3
	assert "" not in nombre_ciudad_direccion

@pytest.mark.parametrize(["equipo"],
	[("seleccion-santa-amalia",)]
)
def test_scraper_equipo_estadio_obtener_tabla_nombre_ubicacion_dato_faltante(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_equipo_estadio._ScraperEquipoEstadio__informacion_datos_estadio(tabla_estadio)

	nombre_ciudad_direccion=scraper_equipo_estadio._ScraperEquipoEstadio__tabla_nombre_ubicacion(tabla_info_datos)

	assert len(nombre_ciudad_direccion)==3
	assert "" in nombre_ciudad_direccion

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),("seleccion-santa-amalia",)]
)
def test_scraper_equipo_estadio_obtener_informacion_nombre_ubicacion_datos_correctos(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	nombre_ciudad_direccion=scraper_equipo_estadio._ScraperEquipoEstadio__informacion_nombre_ubicacion(tabla_estadio)

	assert len(nombre_ciudad_direccion)==3

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_scraper_equipo_estadio_obtener_tabla_datos_tecnicos_datos_correctos(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_equipo_estadio._ScraperEquipoEstadio__informacion_datos_estadio(tabla_estadio)

	estadio=scraper_equipo_estadio._ScraperEquipoEstadio__tabla_datos_tecnicos(tabla_info_datos)

	assert len(estadio)==6
	#assert "" not in estadio # Antes no tenian datos faltantes pero ahora parece que los han eliminado en la web (ciudad, cesped, telfono)

@pytest.mark.parametrize(["equipo"],
	[("seleccion-santa-amalia",)]
)
def test_scraper_equipo_estadio_obtener_tabla_datos_tecnicos_dato_faltante(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_equipo_estadio._ScraperEquipoEstadio__informacion_datos_estadio(tabla_estadio)

	estadio=scraper_equipo_estadio._ScraperEquipoEstadio__tabla_datos_tecnicos(tabla_info_datos)

	assert len(estadio)==6
	#assert estadio.count("")==1 # Antes no tenian datos faltantes pero ahora parece que los han eliminado en la web (ciudad, cesped, telfono)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_scraper_equipo_estadio_obtener_informacion_datos_tecnicos_datos_correctos(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	estadio=scraper_equipo_estadio._ScraperEquipoEstadio__informacion_datos_tecnicos(tabla_estadio)

	assert len(estadio)==6
	#assert "" not in estadio # Antes no tenian datos faltantes pero ahora parece que los han eliminado en la web (ciudad, cesped, telfono)

@pytest.mark.parametrize(["equipo"],
	[("seleccion-santa-amalia",)]
)
def test_scraper_equipo_estadio_obtener_informacion_datos_tecnicos_datos_faltante(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	estadio=scraper_equipo_estadio._ScraperEquipoEstadio__informacion_datos_tecnicos(tabla_estadio)

	assert len(estadio)==6
	#assert estadio.count("")==1 # Antes no tenian datos faltantes pero ahora parece que los han eliminado en la web (ciudad, cesped, telfono)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),("seleccion-santa-amalia",)]
)
def test_scraper_equipo_estadio_obtener_data_limpia(equipo):

	scraper_equipo_estadio=ScraperEquipoEstadio(equipo)

	contenido=scraper_equipo_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_equipo_estadio._ScraperEquipoEstadio__contenido_tabla_estadio(contenido)

	data_limpia=scraper_equipo_estadio._ScraperEquipoEstadio__obtenerDataLimpia(tabla_estadio)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_equipo_estadio_obtener_estadio_equipo_error(endpoint):

	scraper=ScraperEquipoEstadio(endpoint)

	with pytest.raises(EquipoEstadioError):

		scraper.obtenerEstadioEquipo()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",),("seleccion-santa-amalia",)]
)
def test_scraper_equipo_estadio_obtener_estadio_equipo(equipo):

	scraper=ScraperEquipoEstadio(equipo)

	df_estadio=scraper.obtenerEstadioEquipo()

	assert isinstance(df_estadio, pd.DataFrame)