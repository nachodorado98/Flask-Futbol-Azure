import pytest
import os

from src.utilidades.utils import vaciarCarpeta
from src.config import CONTENEDOR

def test_pagina_insertar_partido_asistido_sin_login(cliente):

	data={"partido_anadir":"20190622"}

	respuesta=cliente.post("/insertar_partido_asistido", data=data, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_insertar_partido_asistido_partido_no_existente(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"no_existo", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_no_existo.png")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido_partido_asistido_existente(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno_usuario.insertarPartidoAsistido("20190622", "nacho98", "comentario")

		conexion_entorno_usuario.confirmar()

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

@pytest.mark.parametrize(["caracteres"],
	[(300,),(256,),(1000,),(43575,)]
)
def test_pagina_insertar_partido_asistido_comentario_demasiado_extenso(cliente, conexion_entorno_usuario, caracteres):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"a"*caracteres}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido_sin_comentario(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":None}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		partidos=conexion_entorno_usuario.c.fetchall()

		assert len(partidos)==1
		assert partidos[0]["comentario"] is None

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno_usuario.c.fetchone()

		assert not registro["on_tour"]
		assert not registro["fecha_ida"]
		assert not registro["fecha_vuelta"]
		assert not registro["teletrabajo"]

def test_pagina_insertar_partido_asistido_comentario_limite(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"a"*255}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido_con_imagen_no_valida(cliente, conexion_entorno_usuario, datalake):

	datalake.crearCarpeta(CONTENEDOR, "usuarios/nacho98/imagenes")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests_no_valida.txt")

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests_no_valida.txt")

			respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1
		
		assert datalake.existe_carpeta(CONTENEDOR, "usuarios/nacho98/imagenes")

		objeto_archivo_imagen=datalake.obtenerFile(CONTENEDOR, "usuarios/nacho98/imagenes", "nacho98_20190622.txt")

		assert not objeto_archivo_imagen.exists()

		datalake.eliminarCarpeta(CONTENEDOR, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.txt")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido_con_imagen(cliente, conexion_entorno_usuario, datalake):

	datalake.crearCarpeta(CONTENEDOR, "usuarios/nacho98/imagenes")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpeg")

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		assert datalake.existe_carpeta(CONTENEDOR, "usuarios/nacho98/imagenes")
		
		objeto_archivo_imagen=datalake.obtenerFile(CONTENEDOR, "usuarios/nacho98/imagenes", "nacho98_20190622.jpeg")
		
		assert objeto_archivo_imagen.exists()

		datalake.eliminarCarpeta(CONTENEDOR, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.jpeg")

		assert not os.path.exists(ruta_imagen)

		vaciarCarpeta(ruta_carpeta_imagenes)

def test_pagina_insertar_partido_asistido_no_existe_partido_asistido_favorito_no_favorito(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		assert not conexion_entorno_usuario.c.execute("SELECT * FROM partido_asistido_favorito")

def test_pagina_insertar_partido_asistido_no_existe_partido_asistido_favorito_si_favorito(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "partido-favorito":"on"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno_usuario.c.fetchall())==1

def test_pagina_insertar_partido_asistido_existe_partido_asistido_favorito_no_favorito(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
						VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno_usuario.insertarPartidoAsistido("20190623", "nacho98", "comentario")

		conexion_entorno_usuario.insertarPartidoAsistidoFavorito("20190623", "nacho98")

		conexion_entorno_usuario.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno_usuario.c.fetchall())==1

def test_pagina_insertar_partido_asistido_existe_partido_asistido_favorito_si_favorito(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("""INSERT INTO partidos
										VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno_usuario.insertarPartidoAsistido("20190623", "nacho98", "comentario")

		conexion_entorno_usuario.insertarPartidoAsistidoFavorito("20190623", "nacho98")

		conexion_entorno_usuario.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		data={"partido_anadir":"20190622", "comentario":"comentario", "partido-favorito":"on"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno_usuario.c.fetchall())==1

def test_pagina_insertar_partido_asistido_on_tour_sin_fecha_ida_sin_fecha_vuelta(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno_usuario.c.fetchone()

		assert not registro["on_tour"]
		assert not registro["fecha_ida"]
		assert not registro["fecha_vuelta"]
		assert not registro["teletrabajo"]

def test_pagina_insertar_partido_asistido_on_tour_con_fecha_ida_sin_fecha_vuelta(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-ida":"2019-06-22"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno_usuario.c.fetchone()

		assert not registro["on_tour"]
		assert not registro["fecha_ida"]
		assert not registro["fecha_vuelta"]
		assert not registro["teletrabajo"]

def test_pagina_insertar_partido_asistido_on_tour_sin_fecha_ida_con_fecha_vuelta(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-vuelta":"2019-06-22"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")
		
		registro=conexion_entorno_usuario.c.fetchone()

		assert not registro["on_tour"]
		assert not registro["fecha_ida"]
		assert not registro["fecha_vuelta"]
		assert not registro["teletrabajo"]

@pytest.mark.parametrize(["fecha_ida", "fecha_vuelta"],
	[
		("fecha1", "2019-06-23"),
		("2018-11-01", "fecha2"),
		("201811-01", "2019-06-23"),
		("2018-11-01", "2019-0623"),
		("01-11-2018", "2019-06-23"),
		("2018-11-01", "23-06-2019"),
		("2018-11-01", "2019-06-21"),
		("2019-06-23", "2019-06-24"),
		("2019-06-24", "2019-06-23")
	]
)
def test_pagina_insertar_partido_asistido_on_tour_fechas_invalidas(cliente, conexion_entorno_usuario, fecha_ida, fecha_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-ida":fecha_ida, "fecha-vuelta":fecha_vuelta}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno_usuario.c.fetchone()

		assert not registro["on_tour"]
		assert not registro["fecha_ida"]
		assert not registro["fecha_vuelta"]
		assert not registro["teletrabajo"]

@pytest.mark.parametrize(["fecha_ida", "fecha_vuelta"],
	[
		("2018-11-01", "2019-06-22"),
		("2019-06-22", "2019-06-24"),
		("2019-06-21", "2019-06-23")
	]
)
def test_pagina_insertar_partido_asistido_on_tour_sin_teletrabajo(cliente, conexion_entorno_usuario, fecha_ida, fecha_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-ida":fecha_ida, "fecha-vuelta":fecha_vuelta}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos  WHERE on_tour=True")

		registro=conexion_entorno_usuario.c.fetchone()

		assert registro["on_tour"]
		assert registro["fecha_ida"].strftime("%Y-%m-%d")==fecha_ida
		assert registro["fecha_vuelta"].strftime("%Y-%m-%d")==fecha_vuelta
		assert not registro["teletrabajo"]

@pytest.mark.parametrize(["fecha_ida", "fecha_vuelta"],
	[
		("2018-11-01", "2019-06-22"),
		("2019-06-22", "2019-06-24"),
		("2019-06-21", "2019-06-23")
	]
)
def test_pagina_insertar_partido_asistido_on_tour_con_teletrabajo(cliente, conexion_entorno_usuario, fecha_ida, fecha_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-ida":fecha_ida, "fecha-vuelta":fecha_vuelta, "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos WHERE on_tour=True")

		registro=conexion_entorno_usuario.c.fetchone()

		assert registro["on_tour"]
		assert registro["fecha_ida"].strftime("%Y-%m-%d")==fecha_ida
		assert registro["fecha_vuelta"].strftime("%Y-%m-%d")==fecha_vuelta
		assert registro["teletrabajo"]

@pytest.mark.parametrize(["ciudad_ida", "ciudad_ida_estadio", "transporte_ida", "ciudad_vuelta", "ciudad_vuelta_estadio", "transporte_vuelta"],
	[
		("ciudad_ida", "Madrid", "Avion", "Madrid", "Madrid", "Avion"),
		("Madrid", "ciudad_ida_estadio", "Avion", "Madrid", "Madrid", "Avion"),
		("Madrid", "Madrid", "Avion", "ciudad_vuelta", "Madrid", "Avion"),
		("Madrid", "Madrid", "Avion", "Madrid", "ciudad_vuelta_estadio", "Avion"),
		("Madrid", "ciudad_ida_estadio", "Avion", "Madrid", "ciudad_vuelta_estadio", "Avion"),
		("Madrid", "Madrid", "transporte", "Madrid", "Madrid", "Avion"),
		("Madrid", "Madrid", "Avion", "Madrid", "Madrid", "transporte")
	]
)
def test_pagina_insertar_partido_asistido_on_tour_trayectos_datos_error(cliente, conexion_entorno_usuario, ciudad_ida, ciudad_ida_estadio, transporte_ida, ciudad_vuelta, ciudad_vuelta_estadio, transporte_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":ciudad_ida, "ciudad-ida-estadio":ciudad_ida_estadio,
			"fecha-ida":"2019-06-22", "transporte-ida":transporte_ida, "ciudad-vuelta":ciudad_vuelta, "ciudad-vuelta-estadio":ciudad_vuelta_estadio,
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":transporte_vuelta, "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos WHERE  on_tour=True")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_insertar_partido_asistido_on_tour_trayectos_estadio_no_existente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM estadios")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "ciudad-ida-estadio":"Madrid", "fecha-ida":"2019-06-22",
			"transporte-ida":"Avion", "ciudad-vuelta":"Madrid", "ciudad-vuelta-estadio":"Madrid", "fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos  WHERE on_tour=True")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_insertar_partido_asistido_on_tour_trayectos_ciudad_estadio_no_existente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("UPDATE estadios SET Ciudad=NULL")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "ciudad-ida-estadio":"Madrid", "fecha-ida":"2019-06-22",
			"transporte-ida":"Avion", "ciudad-vuelta":"Madrid", "ciudad-vuelta-estadio":"Madrid", "fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos  WHERE on_tour=True")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_insertar_partido_asistido_on_tour_trayectos_ciudad_estadio_diferente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("UPDATE estadios SET Ciudad=NULL")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "ciudad-ida-estadio":"Barcelona", "fecha-ida":"2019-06-22",
			"transporte-ida":"Avion", "ciudad-vuelta":"Madrid", "ciudad-vuelta-estadio":"Barcelona", "fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos  WHERE on_tour=True")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_insertar_partido_asistido_on_tour_trayectos_ciudad_estadio_erroneas(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("UPDATE estadios SET Ciudad='No Existo'")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "ciudad-ida-estadio":"No Existo", "fecha-ida":"2019-06-22",
			"transporte-ida":"Avion", "ciudad-vuelta":"Madrid", "ciudad-vuelta-estadio":"No Existo", "fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos  WHERE on_tour=True")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_insertar_partido_asistido_on_tour_trayectos_sin_fecha(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "ciudad-ida-estadio":"Madrid",
			"transporte-ida":"Avion", "ciudad-vuelta":"Madrid", "ciudad-vuelta-estadio":"Madrid", "transporte-vuelta":"Avion", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos  WHERE on_tour=True")

		assert not conexion_entorno_usuario.c.fetchall()

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert not conexion_entorno_usuario.c.fetchall()

@pytest.mark.parametrize(["ciudad_ida", "codigo_ciudad_ida", "ciudad_vuelta", "codigo_ciudad_vuelta"],
	[
		("Madrid", 103, "Madrid", 103),
		("Madrid", 103, "Tokyo", 1),
		("London", 34, "Madrid", 103),
		("Verona", 2329, "Verona", 2329)
	]
)
def test_pagina_insertar_partido_asistido_on_tour_trayectos(cliente, conexion_entorno_usuario, ciudad_ida, codigo_ciudad_ida, ciudad_vuelta, codigo_ciudad_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":ciudad_ida, "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Avion", "ciudad-vuelta":ciudad_vuelta, "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos WHERE  on_tour=True")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		registros=conexion_entorno_usuario.c.fetchall()

		assert len(registros)==2

		ida=registros[0]
		vuelta=registros[1]

		assert ida["trayecto_id"]=="id_20190622_nacho98_I"
		assert vuelta["trayecto_id"]=="id_20190622_nacho98_V"
		assert ida["tipo_trayecto"]=="I"
		assert vuelta["tipo_trayecto"]=="V"
		assert ida["codciudad_origen"]==codigo_ciudad_ida
		assert vuelta["codciudad_origen"]==103
		assert ida["codciudad_destino"]==103
		assert vuelta["codciudad_destino"]==codigo_ciudad_vuelta