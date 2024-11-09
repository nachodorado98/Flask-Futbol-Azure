import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_estadio import ScraperEstadio
from src.scrapers.excepciones_scrapers import PaginaError, EstadioError

def test_crear_objeto_scraper_estadio():

	scraper=ScraperEstadio("estadio")

def test_scraper_estadio_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperEstadio("redireccion_equipo")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_estadio_realizar_peticion(scraper_estadio):

	contenido=scraper_estadio._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

@pytest.mark.parametrize(["estadio"],
	[("riyadh-air-metropolitano-23",),("municipal-football-santa-amalia-4902",),("celtic-park-82",),("stadion-feijenoord-71",)]
)
def test_scraper_estadio_obtener_tabla_estadio(estadio):

	scraper_estadio=ScraperEstadio(estadio)

	contenido=scraper_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_estadio._ScraperEstadio__contenido_tabla_estadio(contenido)

	assert tabla_estadio is not None

def test_scraper_estadio_obtener_imagen_estadio(scraper_estadio):

	contenido=scraper_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_estadio._ScraperEstadio__contenido_tabla_estadio(contenido)

	imagen_estadio=scraper_estadio._ScraperEstadio__imagen_estadio(tabla_estadio)

	assert imagen_estadio.endswith(".png") or imagen_estadio.endswith(".jpg")
	assert "estadio_nofoto" not in imagen_estadio
	assert imagen_estadio.startswith("https://cdn.resfu.com/img_data/estadios/original_new")

def test_scraper_estadio_obtener_imagen_estadio_no_tiene():

	scraper_estadio=ScraperEstadio("municipal-football-santa-amalia-4902")

	contenido=scraper_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_estadio._ScraperEstadio__contenido_tabla_estadio(contenido)

	imagen_estadio=scraper_estadio._ScraperEstadio__imagen_estadio(tabla_estadio)

	assert imagen_estadio.endswith(".jpg") or imagen_estadio.endswith(".png")
	assert "estadio_nofoto" in imagen_estadio
	assert imagen_estadio.startswith("https://cdn.resfu.com/img_data/estadios/original_new")

def test_scraper_estadio_obtener_informacion_datos_estadio(scraper_estadio):

	contenido=scraper_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_estadio._ScraperEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_estadio._ScraperEstadio__informacion_datos_estadio(tabla_estadio)

	assert tabla_info_datos is not None

@pytest.mark.parametrize(["estadio"],
	[
		("benito-villamarin-33",),
		("abanca-balaidos-30",),
		("san-mames-22",),
		("mestalla-22",)
	]
)
def test_scraper_estadio_obtener_tabla_ubicacion_localidad_pais_datos_correctos(estadio):

	scraper_estadio=ScraperEstadio(estadio)

	contenido=scraper_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_estadio._ScraperEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_estadio._ScraperEstadio__informacion_datos_estadio(tabla_estadio)

	direccion_localidad_pais=scraper_estadio._ScraperEstadio__tabla_ubicacion_pais(tabla_info_datos)

	assert len(direccion_localidad_pais)==4
	assert "" not in direccion_localidad_pais

@pytest.mark.parametrize(["estadio"],
	[
		("riyadh-air-metropolitano-23",),
		("municipal-football-santa-amalia-4902",),
		("celtic-park-82",),
		("stadion-feijenoord-71",),
		("estadio-olimpico-lluis-companys-2978",)
	]
)
def test_scraper_estadio_obtener_tabla_ubicacion_localidad_pais_datos_faltantes(estadio):

	scraper_estadio=ScraperEstadio(estadio)

	contenido=scraper_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_estadio._ScraperEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_estadio._ScraperEstadio__informacion_datos_estadio(tabla_estadio)

	direccion_localidad_pais=scraper_estadio._ScraperEstadio__tabla_ubicacion_pais(tabla_info_datos)

	assert len(direccion_localidad_pais)==4
	assert "" in direccion_localidad_pais

@pytest.mark.parametrize(["estadio"],
	[
		("benito-villamarin-33",),
		("abanca-balaidos-30",),
		("san-mames-22",),
		("mestalla-22",)
	]
)
def test_scraper_estadio_obtener_informacion_ubicacion_localidad_pais_datos_correctos(estadio):

	scraper_estadio=ScraperEstadio(estadio)

	contenido=scraper_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_estadio._ScraperEstadio__contenido_tabla_estadio(contenido)

	direccion_pais=scraper_estadio._ScraperEstadio__informacion_ubicacion_pais(tabla_estadio)

	assert len(direccion_pais)==4
	assert "" not in direccion_pais

@pytest.mark.parametrize(["estadio"],
	[
		("riyadh-air-metropolitano-23",),
		("municipal-football-santa-amalia-4902",),
		("celtic-park-82",),
		("stadion-feijenoord-71",),
		("estadio-olimpico-lluis-companys-2978",)
	]
)
def test_scraper_estadio_obtener_informacion_ubicacion_localidad_pais_datos_faltantes(estadio):

	scraper_estadio=ScraperEstadio(estadio)

	contenido=scraper_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_estadio._ScraperEstadio__contenido_tabla_estadio(contenido)

	direccion_pais=scraper_estadio._ScraperEstadio__informacion_ubicacion_pais(tabla_estadio)

	assert len(direccion_pais)==4
	assert "" in direccion_pais

@pytest.mark.parametrize(["estadio"],
	[
		("riyadh-air-metropolitano-23",),
		("municipal-football-santa-amalia-4902",),
		("celtic-park-82",),
		("stadion-feijenoord-71",),
		("estadio-olimpico-lluis-companys-2978",),
		("benito-villamarin-33",),
		("abanca-balaidos-30",),
		("san-mames-22",),
		("mestalla-22",)
	]
)
def test_scraper_estadio_obtener_data_limpia(estadio):

	scraper_estadio=ScraperEstadio(estadio)

	contenido=scraper_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_estadio._ScraperEstadio__contenido_tabla_estadio(contenido)

	data_limpia=scraper_estadio._ScraperEstadio__obtenerDataLimpia(tabla_estadio)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_estadio_obtener_estadio_equipo_error(endpoint):

	scraper=ScraperEstadio(endpoint)

	with pytest.raises(EstadioError):

		scraper.obtenerEstadio()

@pytest.mark.parametrize(["estadio"],
	[
		("riyadh-air-metropolitano-23",),
		("municipal-football-santa-amalia-4902",),
		("celtic-park-82",),
		("stadion-feijenoord-71",),
		("estadio-olimpico-lluis-companys-2978",),
		("benito-villamarin-33",),
		("abanca-balaidos-30",),
		("san-mames-22",),
		("mestalla-22",)
	]
)
def test_scraper_estadio_obtener_estadio(estadio):

	scraper=ScraperEstadio(estadio)

	df_estadio=scraper.obtenerEstadio()

	assert isinstance(df_estadio, pd.DataFrame)