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
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
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
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

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
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

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
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_insertar_partido_asistido_on_tour_trayectos_estadio_no_existente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM estadios")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "ciudad-ida-estadio":"Madrid", "fecha-ida":"2019-06-22",
			"transporte-ida":"Pie", "ciudad-vuelta":"Madrid", "ciudad-vuelta-estadio":"Madrid", "fecha-vuelta":"2019-06-22", "transporte-vuelta":"Coche", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_insertar_partido_asistido_on_tour_trayectos_ciudad_estadio_no_existente(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("UPDATE estadios SET Ciudad=NULL")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "ciudad-ida-estadio":"Madrid", "fecha-ida":"2019-06-22",
			"transporte-ida":"Pie", "ciudad-vuelta":"Madrid", "ciudad-vuelta-estadio":"Madrid", "fecha-vuelta":"2019-06-22", "transporte-vuelta":"Coche", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_insertar_partido_asistido_on_tour_trayectos_ciudad_estadio_diferente(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "ciudad-ida-estadio":"Barcelona", "fecha-ida":"2019-06-22",
			"transporte-ida":"Coche", "ciudad-vuelta":"Madrid", "ciudad-vuelta-estadio":"Barcelona", "fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

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
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

def test_pagina_insertar_partido_asistido_on_tour_trayectos_sin_fecha(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":"Madrid", "ciudad-ida-estadio":"Madrid",
			"transporte-ida":"Pie", "ciudad-vuelta":"Madrid", "ciudad-vuelta-estadio":"Madrid", "transporte-vuelta":"Coche", "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos WHERE on_tour=True")

		assert not conexion_entorno_usuario.c.fetchall()

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert not conexion_entorno_usuario.c.fetchall()

@pytest.mark.parametrize(["ciudad_ida", "pais_ida", "codigo_ciudad_ida", "transporte_ida", "ciudad_vuelta", "pais_vuelta", "codigo_ciudad_vuelta", "transporte_vuelta"],
	[
		("Madrid", "España", 103, "Avion", "Madrid", "España", 103, "Pie"),
		("Madrid", "España", 103, "Pie", "Madrid", "España", 103, "Tren"),
		("Madrid", "España", 103, "Pie", "Tokyo", "Japón", 1, "Pie"),
		("Londres", "Reino Unido", 34, "Coche", "Madrid", "España", 103, "Pie"),
		("Verona", "Italia", 2329, "Cercanias", "Verona", "Italia", 2329, "Avion"),
		("Merida", "España", 5809, "Metro", "Madrid", "España", 103, "Metro"),
		("Merida Mex", "México", 917, "Autobus", "Madrid", "España", 103, "Autobus Urbano"),
		("Merida Mex", "México", 917, "Avion", "Leganés", "España", 2947, "Avion"),
		("Getafe", "España", 3025, "Avion", "Leganés", "España", 2947, "Metro"),
		("Getafe", "España", 3025, "Cercanias", "Leganés", "España", 2947, "Tren")
	]
)
def test_pagina_insertar_partido_asistido_on_tour_trayectos_transporte_inadecuado(cliente, conexion_entorno_usuario, ciudad_ida, pais_ida, codigo_ciudad_ida,
																					transporte_ida, ciudad_vuelta, pais_vuelta, codigo_ciudad_vuelta, transporte_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":ciudad_ida, "pais-ida":pais_ida, "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":transporte_ida, "ciudad-vuelta":ciudad_vuelta, "pais-vuelta":pais_vuelta, "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":transporte_vuelta, "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

@pytest.mark.parametrize(["ciudad_ida", "pais_ida", "codigo_ciudad_ida", "transporte_ida", "ciudad_vuelta", "pais_vuelta", "codigo_ciudad_vuelta", "transporte_vuelta"],
	[
		("Madrid", "España", 103, "Pie", "Madrid", "España", 103, "Metro"),
		("Madrid", "España", 103, "Coche", "Tokyo", "Japón", 1, "Avion"),
		("Londres", "Reino Unido", 34, "Autobus", "Madrid", "España", 103, "Cercanias"),
		("Verona", "Italia", 2329, "Avion", "Verona", "Italia", 2329, "Avion"),
		("Merida", "España", 5809, "Autobus", "Madrid", "España", 103, "Autobus Interurbano"),
		("Merida Mex", "México", 917, "Avion", "Madrid", "España", 103, "Autobus Urbano"),
		("Merida Mex", "México", 917, "Avion", "Merida", "España", 5809, "Tren"),
		("Pamplona", "España", 2720, "Autobus", "Sevilla", "España", 1095, "Tren"),
		("Vitoria-Gasteiz", "España", 2362, "Coche", "Valencia", "España", 987, "Tren"),
		("Valladolid", "España", 2081, "Autobus", "Valladolid", "España", 2081, "Tren"),
		("Paris", "Francia", 35, "Avion", "Lisboa", "Portugal", 735, "Autobus")
	]
)
def test_pagina_insertar_partido_asistido_on_tour_trayectos(cliente, conexion_entorno_usuario, ciudad_ida, pais_ida, codigo_ciudad_ida,
															transporte_ida, ciudad_vuelta, pais_vuelta, codigo_ciudad_vuelta, transporte_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "ciudad-ida":ciudad_ida, "pais-ida":pais_ida, "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":transporte_ida, "ciudad-vuelta":ciudad_vuelta, "pais-vuelta":pais_vuelta, "ciudad-vuelta-estadio":"Madrid",
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

		registros=conexion_entorno_usuario.c.fetchall()

		assert len(registros)==2

		ida=registros[0]
		vuelta=registros[1]

		assert ida["trayecto_id"]=="id_20190622_nacho98_I_0"
		assert vuelta["trayecto_id"]=="id_20190622_nacho98_V_0"
		assert ida["tipo_trayecto"]=="I"
		assert vuelta["tipo_trayecto"]=="V"
		assert ida["codciudad_origen"]==codigo_ciudad_ida
		assert vuelta["codciudad_origen"]==103
		assert ida["codciudad_destino"]==103
		assert vuelta["codciudad_destino"]==codigo_ciudad_vuelta

def test_pagina_insertar_partido_asistido_on_tour_trayectos_paradas_no_existen(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario","ciudad-ida":"Madrid", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Pie", "ciudad-vuelta":"Madrid", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Metro", "teletrabajo":True, "transporte-parada-ida[]":[], "pais-parada-ida[]":[], 
			"ciudad-parada-ida[]":[], "transporte-parada-vuelta[]":[], "pais-parada-vuelta[]":[], "ciudad-parada-vuelta[]":[]}

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

@pytest.mark.parametrize(["transportes_ida", "paises_ida", "ciudades_ida", "transportes_vuelta", "paises_vuelta", "ciudades_vuelta"],
	[
		(["", ""], ["", ""], ["", ""], [], [], []),
		(["", ""], [], ["", ""], [], [], []),
		(["Bus"], ["", ""], ["Madrid"], [], [], []),
		(["Bus"], ["España", "Francia"], ["Madrid"], [], [], []),
		([], [], [], ["", ""], ["", ""], ["", ""]),
		([], [], [], ["", ""], [], ["", ""]),
		([], [], [], ["Bus"], ["", ""], ["Madrid"]),
		([], [], [], ["Bus"], ["España", "Francia"], ["Madrid"]),
		(["", ""], [], ["", ""], ["", ""], ["", ""], ["", ""]),
		(["Bus"], ["", ""], ["Madrid"], ["", ""], [], ["", ""]),
		(["Bus"], ["España", "Francia"], ["Madrid"], ["Bus"], ["", ""], ["Madrid"]),
		(["", ""], ["", ""], ["", ""], ["Bus"], ["España", "Francia"], ["Madrid"])
	]
)
def test_pagina_insertar_partido_asistido_on_tour_trayectos_paradas_incompletas(cliente, conexion_entorno_usuario, transportes_ida, paises_ida, ciudades_ida,
																					transportes_vuelta, paises_vuelta, ciudades_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario","ciudad-ida":"Madrid", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Pie", "ciudad-vuelta":"Madrid", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Metro", "teletrabajo":True, "transporte-parada-ida[]":transportes_ida, "pais-parada-ida[]":paises_ida, 
			"ciudad-parada-ida[]":ciudades_ida, "transporte-parada-vuelta[]":transportes_vuelta, "pais-parada-vuelta[]":paises_vuelta, "ciudad-parada-vuelta[]":ciudades_vuelta}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

@pytest.mark.parametrize(["transportes_ida", "paises_ida", "ciudades_ida", "transportes_vuelta", "paises_vuelta", "ciudades_vuelta"],
	[
		(["Autobus", "Avion"], ["España", "Francia"], ["Madrid", "Paris"], [], [], []),
		([], [], [], ["Autobus", "Avion"], ["España", "Francia"], ["Madrid", "Paris"]),
		(["Autobus"], ["España"], ["Madrid"], ["Tren"], ["España"], ["Getafe"]),
		(["Autobus"], ["España"], ["Getafe"], ["Tren"], ["España"], ["Madrid"]),
		(["Autobus"], ["España"], ["Madrid"], ["Tren"], ["España"], ["Madrid"]),
		(["Autobus", "Avion"], ["España", "Francia"], ["Sevilla", "Paris"], ["Autobus", "Avion"], ["España", "Francia"], ["Madrid", "Paris"]),
		(["Autobus", "Avion"], ["España", "Francia"], ["Madrid", "Paris"], ["Autobus", "Avion"], ["España", "Francia"], ["Valencia", "Paris"]),
		(["Autobus", "Avion"], ["España", "Francia"], ["Madrid", "Paris"], ["Autobus", "Avion"], ["España", "Francia"], ["Madrid", "Paris"])
	]
)
def test_pagina_insertar_partido_asistido_on_tour_trayectos_paradas_no_unicas(cliente, conexion_entorno_usuario, transportes_ida, paises_ida, ciudades_ida,
																					transportes_vuelta, paises_vuelta, ciudades_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario","ciudad-ida":"Barcelona", "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":"Avion", "ciudad-vuelta":"Barcelona", "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":"Avion", "teletrabajo":True, "transporte-parada-ida[]":transportes_ida, "pais-parada-ida[]":paises_ida, 
			"ciudad-parada-ida[]":ciudades_ida, "transporte-parada-vuelta[]":transportes_vuelta, "pais-parada-vuelta[]":paises_vuelta, "ciudad-parada-vuelta[]":ciudades_vuelta}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido?partido_id=20190622&todos=True"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno_usuario.c.fetchall()

@pytest.mark.parametrize(["transportes_ida", "paises_ida", "ciudades_ida", "transportes_vuelta", "paises_vuelta", "ciudades_vuelta", "ciudad_ida", "transporte_ida", "ciudad_vuelta", "transporte_vuelta", "trayectos_ida", "trayectos_vuelta"],
	[
		(["Avion", "Cercanias"], ["España", "España"], ["Getafe", "Leganés"], [], [], [], "Barcelona", "Cercanias", "Barcelona", "Avion", 3, 1),
		(["Avion", "Tren"], ["España", "España"], ["Sevilla", "Leganés"], [], [], [], "Valencia", "Autobus Urbano", "Zaragoza", "Tren", 3, 1),
		(["Autobus", "Coche"], ["España", "España"], ["Granada", "Elche"], [], [], [], "Sevilla", "Tren", "Vigo", "Avion", 3, 1),
		(["Autobus", "Coche", "Tren"], ["España", "España", "España"], ["Murcia", "Alicante", "Alcorcon"], [], [], [], "Malaga", "Metro", "A Coruña", "Avion", 4, 1),
		(["Avion"], ["España"], ["Getafe"], [], [], [], "Barcelona", "Cercanias", "Barcelona", "Avion", 2, 1),
		(["Autobus", "Coche", "Tren", "Cercanias"], ["España", "España", "España", "España"], ["Murcia", "Alicante", "Alcorcon", "Getafe"], [], [], [], "Malaga", "Metro", "A Coruña", "Avion", 5, 1),
		(["Avion", "Avion"], ["Reino Unido", "Francia"], ["Glasgow", "Marsella"], [], [], [], "Barcelona", "Avion", "Sevilla", "Tren", 3, 1),
		(["Avion", "Tren"], ["Italia", "Italia"], ["Milan", "Verona"], [], [], [], "Barcelona", "Avion", "Valencia", "Tren", 3, 1),
		([], [], [], ["Metro", "Avion"], ["España", "Francia"], ["Getafe", "Paris"], "Barcelona", "Autobus", "Barcelona", "Avion", 1, 3),
		([], [], [], ["Coche", "Avion"], ["España", "Francia"], ["Getafe", "Paris"], "Valencia", "Autobus", "Zaragoza", "Avion", 1, 3),
		([], [], [], ["Coche", "Tren"], ["España", "España"], ["Gijon", "Valladolid"], "Vigo", "Autobus", "Oviedo", "Autobus", 1, 3),
		([], [], [], ["Avion", "Avion", "Avion"], ["Reino Unido", "Alemania", "España"], ["Londres", "Berlin", "Palma"], "Malaga", "Autobus", "Barcelona", "Autobus", 1, 4),
		([], [], [], ["Metro"], ["España"], ["Getafe"], "Barcelona", "Autobus", "Barcelona", "Avion", 1, 2),
		([], [], [], ["Avion", "Avion", "Avion", "Avion"], ["Reino Unido", "Alemania", "Francia", "España"], ["Londres", "Berlin", "Paris", "Palma"], "Malaga", "Autobus", "Barcelona", "Autobus", 1, 5),
		([], [], [], ["Avion", "Tren", "Avion", "Tren"], ["Alemania", "Alemania", "Francia", "Bélgica"], ["Munich", "Berlin", "Paris", "Bruselas"], "Guadalajara", "Cercanias", "Barcelona", "Avion", 1, 5)
	]
)
def test_pagina_insertar_partido_asistido_on_tour_trayectos_paradas_ida_o_vuelta(cliente, conexion_entorno_usuario, transportes_ida, paises_ida, ciudades_ida,
																					transportes_vuelta, paises_vuelta, ciudades_vuelta, ciudad_ida, transporte_ida,
																					ciudad_vuelta, transporte_vuelta, trayectos_ida, trayectos_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario","ciudad-ida":ciudad_ida, "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":transporte_ida, "ciudad-vuelta":ciudad_vuelta, "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":transporte_vuelta, "teletrabajo":True, "transporte-parada-ida[]":transportes_ida, "pais-parada-ida[]":paises_ida, 
			"ciudad-parada-ida[]":ciudades_ida, "transporte-parada-vuelta[]":transportes_vuelta, "pais-parada-vuelta[]":paises_vuelta, "ciudad-parada-vuelta[]":ciudades_vuelta}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos WHERE  on_tour=True")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido WHERE Tipo_Trayecto='I'")

		idas=conexion_entorno_usuario.c.fetchall()

		assert len(idas)==trayectos_ida

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido WHERE Tipo_Trayecto='V'")

		vueltas=conexion_entorno_usuario.c.fetchall()

		assert len(vueltas)==trayectos_vuelta

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert len(conexion_entorno_usuario.c.fetchall())==trayectos_ida+trayectos_vuelta

		for numero_trayecto in range(trayectos_ida):

			if trayectos_ida==1:

				assert idas[numero_trayecto]["trayecto_id"]=="id_20190622_nacho98_I_0"

			else:

				assert idas[numero_trayecto]["trayecto_id"]==f"id_20190622_nacho98_I_{numero_trayecto+1}"
				assert idas[numero_trayecto]["tipo_trayecto"]=="I"

		assert idas[-1]["codciudad_destino"]==103

		for numero_trayecto in range(trayectos_vuelta):

			if trayectos_vuelta==1:

				assert vueltas[numero_trayecto]["trayecto_id"]=="id_20190622_nacho98_V_0"

			else:

				assert vueltas[numero_trayecto]["trayecto_id"]==f"id_20190622_nacho98_V_{numero_trayecto+1}"
				assert vueltas[numero_trayecto]["tipo_trayecto"]=="V"

		assert vueltas[0]["codciudad_origen"]==103

@pytest.mark.parametrize(["transportes_ida", "paises_ida", "ciudades_ida", "transportes_vuelta", "paises_vuelta", "ciudades_vuelta", "ciudad_ida", "transporte_ida", "ciudad_vuelta", "transporte_vuelta", "trayectos_ida", "trayectos_vuelta"],
	[
		(["Avion", "Cercanias"], ["España", "España"], ["Getafe", "Leganés"], ["Metro", "Avion"], ["España", "Francia"], ["Getafe", "Paris"], "Barcelona", "Cercanias", "Barcelona", "Avion", 3, 3),
		(["Avion", "Tren"], ["España", "España"], ["Sevilla", "Leganés"], ["Coche", "Avion"], ["España", "Francia"], ["Getafe", "Paris"], "Valencia", "Autobus Urbano", "Zaragoza", "Tren", 3, 3),
		(["Autobus", "Coche"], ["España", "España"], ["Granada", "Elche"], ["Coche", "Tren"], ["España", "España"], ["Gijon", "Valladolid"], "Sevilla", "Tren", "Oviedo", "Autobus", 3, 3),
		(["Autobus", "Coche", "Tren"], ["España", "España", "España"], ["Murcia", "Alicante", "Alcorcon"], ["Metro"], ["España"], ["Getafe"], "Malaga", "Metro", "Barcelona", "Autobus", 4, 2),
		(["Avion"], ["España"], ["Getafe"], ["Avion", "Avion", "Avion"], ["Reino Unido", "Alemania", "España"], ["Londres", "Berlin", "Palma"], "Barcelona", "Cercanias", "Barcelona", "Autobus", 2, 4),
		(["Autobus", "Coche", "Tren", "Cercanias"], ["España", "España", "España", "España"], ["Murcia", "Alicante", "Alcorcon", "Getafe"], ["Avion", "Tren", "Avion", "Tren"], ["Alemania", "Alemania", "Francia", "Bélgica"], ["Munich", "Berlin", "Paris", "Bruselas"], "Malaga", "Metro", "Barcelona", "Avion", 5, 5),
		(["Avion", "Avion"], ["Reino Unido", "Francia"], ["Glasgow", "Marsella"], ["Avion", "Avion", "Avion", "Avion"], ["Reino Unido", "Alemania", "Francia", "España"], ["Londres", "Berlin", "Paris", "Alicante"], "Barcelona", "Avion", "Barcelona", "Tren", 3, 5),
		(["Avion", "Tren"], ["Italia", "Italia"], ["Milan", "Verona"], ["Coche"], ["España"], ["Alicante"], "Barcelona", "Avion", "Valencia", "Tren", 3, 2)
	]
)
def test_pagina_insertar_partido_asistido_on_tour_trayectos_paradas_ambas(cliente, conexion_entorno_usuario, transportes_ida, paises_ida, ciudades_ida,
																			transportes_vuelta, paises_vuelta, ciudades_vuelta, ciudad_ida, transporte_ida,
																			ciudad_vuelta, transporte_vuelta, trayectos_ida, trayectos_vuelta):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario","ciudad-ida":ciudad_ida, "pais-ida":"España", "ciudad-ida-estadio":"Madrid",
			"fecha-ida":"2019-06-22", "transporte-ida":transporte_ida, "ciudad-vuelta":ciudad_vuelta, "pais-vuelta":"España", "ciudad-vuelta-estadio":"Madrid",
			"fecha-vuelta":"2019-06-22", "transporte-vuelta":transporte_vuelta, "teletrabajo":True, "transporte-parada-ida[]":transportes_ida, "pais-parada-ida[]":paises_ida, 
			"ciudad-parada-ida[]":ciudades_ida, "transporte-parada-vuelta[]":transportes_vuelta, "pais-parada-vuelta[]":paises_vuelta, "ciudad-parada-vuelta[]":ciudades_vuelta}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno_usuario.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos WHERE  on_tour=True")

		assert len(conexion_entorno_usuario.c.fetchall())==1

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido WHERE Tipo_Trayecto='I'")

		idas=conexion_entorno_usuario.c.fetchall()

		assert len(idas)==trayectos_ida

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido WHERE Tipo_Trayecto='V'")

		vueltas=conexion_entorno_usuario.c.fetchall()

		assert len(vueltas)==trayectos_vuelta

		conexion_entorno_usuario.c.execute("SELECT * FROM trayecto_partido_asistido")

		assert len(conexion_entorno_usuario.c.fetchall())==trayectos_ida+trayectos_vuelta

		for numero_trayecto in range(trayectos_ida):

			assert idas[numero_trayecto]["trayecto_id"]==f"id_20190622_nacho98_I_{numero_trayecto+1}"
			assert idas[numero_trayecto]["tipo_trayecto"]=="I"

		assert idas[-1]["codciudad_destino"]==103

		for numero_trayecto in range(trayectos_vuelta):

			assert vueltas[numero_trayecto]["trayecto_id"]==f"id_20190622_nacho98_V_{numero_trayecto+1}"
			assert vueltas[numero_trayecto]["tipo_trayecto"]=="V"

		assert vueltas[0]["codciudad_origen"]==103