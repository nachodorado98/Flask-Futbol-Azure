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

def test_pagina_insertar_partido_asistido_partido_no_existente(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"no_existo", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno.c.fetchall()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_no_existo.png")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido_partido_asistido_existente(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno.insertarPartidoAsistido("20190622", "nacho98", "comentario")

		conexion_entorno.confirmar()

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

@pytest.mark.parametrize(["caracteres"],
	[(300,),(256,),(1000,),(43575,)]
)
def test_pagina_insertar_partido_asistido_comentario_demasiado_extenso(cliente, conexion_entorno, password_hash, caracteres):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"a"*caracteres}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/anadir_partido_asistido"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert not conexion_entorno.c.fetchall()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido_sin_comentario(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":None}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		partidos=conexion_entorno.c.fetchall()

		assert len(partidos)==1
		assert partidos[0]["comentario"] is None

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

		conexion_entorno.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno.c.fetchone()

		assert not registro["on_tour"]
		assert not registro["fecha_ida"]
		assert not registro["fecha_vuelta"]
		assert not registro["teletrabajo"]

def test_pagina_insertar_partido_asistido_comentario_limite(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"a"*255}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.png")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido_con_imagen_no_valida(cliente, conexion_entorno, datalake):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16",
											"equipo":"atletico-madrid"})

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

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1
		
		assert datalake.existe_carpeta(CONTENEDOR, "usuarios/nacho98/imagenes")

		objeto_archivo_imagen=datalake.obtenerFile(CONTENEDOR, "usuarios/nacho98/imagenes", "nacho98_20190622.txt")

		assert not objeto_archivo_imagen.exists()

		datalake.eliminarCarpeta(CONTENEDOR, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.txt")

		assert not os.path.exists(ruta_imagen)

def test_pagina_insertar_partido_asistido_con_imagen(cliente, conexion_entorno, datalake):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16",
											"equipo":"atletico-madrid"})

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

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		assert datalake.existe_carpeta(CONTENEDOR, "usuarios/nacho98/imagenes")
		
		objeto_archivo_imagen=datalake.obtenerFile(CONTENEDOR, "usuarios/nacho98/imagenes", "nacho98_20190622.jpeg")
		
		assert objeto_archivo_imagen.exists()

		datalake.eliminarCarpeta(CONTENEDOR, "usuarios/nacho98")

		datalake.cerrarConexion()

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "templates", "imagenes", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_20190622.jpeg")

		assert not os.path.exists(ruta_imagen)

		vaciarCarpeta(ruta_carpeta_imagenes)

def test_pagina_insertar_partido_asistido_no_existe_partido_asistido_favorito_no_favorito(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		assert not conexion_entorno.c.execute("SELECT * FROM partido_asistido_favorito")

def test_pagina_insertar_partido_asistido_no_existe_partido_asistido_favorito_si_favorito(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "partido-favorito":"on"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno.c.fetchall())==1

def test_pagina_insertar_partido_asistido_existe_partido_asistido_favorito_no_favorito(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO partidos
						VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno.insertarPartidoAsistido("20190623", "nacho98", "comentario")

		conexion_entorno.insertarPartidoAsistidoFavorito("20190623", "nacho98")

		conexion_entorno.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno.c.fetchall())==1

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno.c.fetchall())==1

def test_pagina_insertar_partido_asistido_existe_partido_asistido_favorito_si_favorito(cliente, conexion_entorno, password_hash):

	conexion_entorno.c.execute("""INSERT INTO partidos
						VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno.insertarPartidoAsistido("20190623", "nacho98", "comentario")

		conexion_entorno.insertarPartidoAsistidoFavorito("20190623", "nacho98")

		conexion_entorno.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno.c.fetchall())==1

		data={"partido_anadir":"20190622", "comentario":"comentario", "partido-favorito":"on"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partido_asistido_favorito")

		assert len(conexion_entorno.c.fetchall())==1

def test_pagina_insertar_partido_asistido_on_tour_sin_fecha_ida_sin_fecha_vuelta(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		conexion_entorno.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno.c.fetchone()

		assert not registro["on_tour"]
		assert not registro["fecha_ida"]
		assert not registro["fecha_vuelta"]
		assert not registro["teletrabajo"]

def test_pagina_insertar_partido_asistido_on_tour_con_fecha_ida_sin_fecha_vuelta(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-ida":"2019-06-22"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		conexion_entorno.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno.c.fetchone()

		assert not registro["on_tour"]
		assert not registro["fecha_ida"]
		assert not registro["fecha_vuelta"]
		assert not registro["teletrabajo"]

def test_pagina_insertar_partido_asistido_on_tour_sin_fecha_ida_con_fecha_vuelta(cliente, conexion_entorno, password_hash):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-vuelta":"2019-06-22"}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		conexion_entorno.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")
		
		registro=conexion_entorno.c.fetchone()

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
def test_pagina_insertar_partido_asistido_on_tour_fechas_invalidas(cliente, conexion_entorno, password_hash, fecha_ida, fecha_vuelta):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-ida":fecha_ida, "fecha-vuelta":fecha_vuelta}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		conexion_entorno.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno.c.fetchone()

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
def test_pagina_insertar_partido_asistido_on_tour_sin_teletrabajo(cliente, conexion_entorno, password_hash, fecha_ida, fecha_vuelta):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-ida":fecha_ida, "fecha-vuelta":fecha_vuelta}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		conexion_entorno.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno.c.fetchone()

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
def test_pagina_insertar_partido_asistido_on_tour_con_teletrabajo(cliente, conexion_entorno, password_hash, fecha_ida, fecha_vuelta):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		data={"partido_anadir":"20190622", "comentario":"comentario", "fecha-ida":fecha_ida, "fecha-vuelta":fecha_vuelta, "teletrabajo":True}

		respuesta=cliente_abierto.post("/insertar_partido_asistido", data=data)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/partidos/asistidos"
		assert "Redirecting..." in contenido

		conexion_entorno.c.execute("SELECT * FROM partidos_asistidos")

		assert len(conexion_entorno.c.fetchall())==1

		conexion_entorno.c.execute("SELECT On_Tour, Fecha_Ida, Fecha_Vuelta, Teletrabajo FROM partidos_asistidos")

		registro=conexion_entorno.c.fetchone()

		assert registro["on_tour"]
		assert registro["fecha_ida"].strftime("%Y-%m-%d")==fecha_ida
		assert registro["fecha_vuelta"].strftime("%Y-%m-%d")==fecha_vuelta
		assert registro["teletrabajo"]