import pytest

def test_pagina_anadir_partido_asistido_sin_login(cliente):

	respuesta=cliente.get("/anadir_partido_asistido", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_anadir_partido_asistido_partidos_no_existen(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno_usuario.c.execute("""DELETE FROM partidos""")

		conexion_entorno_usuario.confirmar()

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' not in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' not in contenido
		assert '<button type="button" class="boton-todos-partidos"' not in contenido
		assert 'recientes.png' not in contenido
		assert '?todos=True' not in contenido
		assert 'todos.png' not in contenido
		assert '<p class="etiqueta">' not in contenido
		assert "No hay partidos disponibles para añadir..." in contenido
		assert '<div class="contenedor-comentario">' not in contenido
		assert '<div class="contenedor-checkbox-partido-favorito">' not in contenido
		assert '<div class="contenedor-imagen">' not in contenido
		assert '<div class="contenedor-seccion-on-tour">' not in contenido
		assert '<div class="contenedor-on-tour">' not in contenido

def test_pagina_anadir_partido_asistido_partidos_no_existen_equipo_usuario(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno_usuario.c.execute("""DELETE FROM partidos""")

		conexion_entorno_usuario.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival1'),('rival2')""")

		conexion_entorno_usuario.c.execute("""INSERT INTO partidos
										VALUES('20190622', 'rival1', 'rival2', '2019-06-22', '22:00', 'Liga', '1-0', 'Victoria'),
												('20190623', 'rival2', 'rival2', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria'),
												('20190624', 'rival1', 'rival1', '2019-06-24', '22:00', 'Liga', '1-0', 'Victoria'),
												('20190625', 'rival2', 'rival1', '2019-06-25', '22:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno_usuario.confirmar()

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' not in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' not in contenido
		assert '<button type="button" class="boton-todos-partidos"' not in contenido
		assert 'recientes.png' not in contenido
		assert '?todos=True' not in contenido
		assert 'todos.png' not in contenido
		assert '<p class="etiqueta">' not in contenido
		assert "No hay partidos disponibles para añadir..." in contenido
		assert '<div class="contenedor-comentario">' not in contenido
		assert '<div class="contenedor-checkbox-partido-favorito">' not in contenido
		assert '<div class="contenedor-imagen">' not in contenido
		assert '<div class="contenedor-seccion-on-tour">' not in contenido
		assert '<div class="contenedor-on-tour">' not in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_existen_recientes(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' in contenido
		assert '<button type="button" class="boton-todos-partidos"' in contenido
		assert 'recientes.png' in contenido
		assert '?todos=True' in contenido
		assert 'todos.png' not in contenido
		assert '<p class="etiqueta">' in contenido
		assert "No hay partidos disponibles para añadir..." not in contenido
		assert '<div class="contenedor-comentario">' in contenido
		assert '<div class="contenedor-checkbox-partido-favorito">' in contenido
		assert '<input type="checkbox" id="partido-favorito" name="partido-favorito">' in contenido
		assert '<p class="partido-favorito-texto"><strong>Partido Asistido Favorito</strong></p>' in contenido
		assert '<div class="contenedor-imagen">' in contenido
		assert '<div class="contenedor-seccion-on-tour">' in contenido
		assert '<div class="contenedor-on-tour">' in contenido
		assert '<div class="seccion-on-tour-partido-asistido"' in contenido
		assert '<div class="contenedor-datos-ida">' in contenido
		assert '<select id="pais-ida" name="pais-ida"' in contenido
		assert '<select id="ciudad-ida" name="ciudad-ida"' in contenido
		assert '<select id="ciudad-ida-estadio" name="ciudad-ida-estadio"' in contenido
		assert '<select id="transporte-ida" name="transporte-ida"' in contenido
		assert '<div class="contenedor-datos-vuelta">' in contenido
		assert '<select id="pais-vuelta" name="pais-vuelta"' in contenido
		assert '<select id="ciudad-vuelta" name="ciudad-vuelta"' in contenido
		assert '<select id="ciudad-vuelta-estadio" name="ciudad-vuelta-estadio"' in contenido
		assert '<select id="transporte-vuelta" name="transporte-vuelta"' in contenido
		assert '<option value="España" selected hidden>España</option>' in contenido
		assert '<option value="Madrid" selected>Madrid</option>' in contenido
		assert '<option value="Madrid">Metropolitano</option>' not in contenido
		assert '<div class="contenedor-checkbox-teletrabajo">' in contenido
		assert "max='2019-06-22'" not in contenido
		assert "min='2019-06-22'" not in contenido

@pytest.mark.parametrize(["codciudad", "ciudad", "pais"],
	[
		(103, "Madrid", "España"),
		(1, "Tokyo", "Japón"),
		(13, "Nueva York", "Estados Unidos"),
		(160, "Barcelona", "España"),
		(2081, "Valladolid", "España")
	]
)
def test_pagina_anadir_partido_asistido_partidos_no_asistidos_existen_recientes_ciudad_usuario(cliente, conexion_entorno, password_hash, codciudad, ciudad, pais):

	conexion_entorno.insertarUsuario("nacho98", "nacho@gmail.com", password_hash, "nacho", "dorado", "1998-02-16", codciudad, "atletico-madrid")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="contenedor-seccion-on-tour">' in contenido
		assert '<div class="contenedor-on-tour">' in contenido
		assert '<div class="seccion-on-tour-partido-asistido"' in contenido
		assert '<div class="contenedor-datos-ida">' in contenido
		assert '<select id="pais-ida" name="pais-ida"' in contenido
		assert '<select id="ciudad-ida" name="ciudad-ida"' in contenido
		assert '<select id="ciudad-ida-estadio" name="ciudad-ida-estadio"' in contenido
		assert '<select id="transporte-ida" name="transporte-ida"' in contenido
		assert '<div class="contenedor-datos-vuelta">' in contenido
		assert '<select id="pais-vuelta" name="pais-vuelta"' in contenido
		assert '<select id="ciudad-vuelta" name="ciudad-vuelta"' in contenido
		assert '<select id="ciudad-vuelta-estadio" name="ciudad-vuelta-estadio"' in contenido
		assert '<select id="transporte-vuelta" name="transporte-vuelta"' in contenido
		assert f'<option value="{pais}" selected hidden>{pais}</option>' in contenido
		assert f'<option value="{ciudad}" selected>{ciudad}</option>' in contenido
		assert '<option value="Madrid">Metropolitano</option>' not in contenido
		assert '<div class="contenedor-checkbox-teletrabajo">' in contenido
		assert "max='2019-06-22'" not in contenido
		assert "min='2019-06-22'" not in contenido

def test_pagina_anadir_partido_asistido_partido_no_asistidos_no_existen_recientes(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_entorno_usuario.insertarPartidoAsistido("20190622", "nacho98", "comentario")

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' not in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' not in contenido
		assert '<button type="button" class="boton-todos-partidos"' not in contenido
		assert 'recientes.png' not in contenido
		assert '?todos=True' not in contenido
		assert 'todos.png' not in contenido
		assert '<p class="etiqueta">' not in contenido
		assert "No hay partidos disponibles para añadir..." in contenido
		assert '<div class="contenedor-comentario">' not in contenido
		assert '<div class="contenedor-checkbox-partido-favorito">' not in contenido
		assert '<div class="contenedor-imagen">' not in contenido
		assert '<div class="contenedor-seccion-on-tour">' not in contenido
		assert '<div class="contenedor-on-tour">' not in contenido
		assert '<div class="seccion-on-tour-partido-asistido"' not in contenido
		assert '<div class="contenedor-datos-ida">' not in contenido
		assert '<select id="pais-ida" name="pais-ida"' not in contenido
		assert '<select id="ciudad-ida" name="ciudad-ida"' not in contenido
		assert '<select id="ciudad-ida-estadio" name="ciudad-ida-estadio"' not in contenido
		assert '<select id="transporte-ida" name="transporte-ida"' not in contenido
		assert '<div class="contenedor-datos-vuelta">' not in contenido
		assert '<select id="pais-vuelta" name="pais-vuelta"' not in contenido
		assert '<select id="ciudad-vuelta" name="ciudad-vuelta"' not in contenido
		assert '<select id="ciudad-vuelta-estadio" name="ciudad-vuelta-estadio"' not in contenido
		assert '<select id="transporte-vuelta" name="transporte-vuelta"' not in contenido
		assert '<option value="España" selected hidden>España</option>' not in contenido
		assert '<option value="Madrid" selected>Madrid</option>' not in contenido
		assert '<option value="Madrid">Metropolitano</option>' not in contenido
		assert '<div class="contenedor-checkbox-teletrabajo">' not in contenido
		assert "max='2019-06-22'" not in contenido
		assert "min='2019-06-22'" not in contenido

def test_pagina_obtener_fecha_partido_sin_partido_id(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/fecha_partido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==400
		assert "error" in contenido
		assert "fecha_ida" not in contenido

def test_pagina_obtener_fecha_partido_partido_id_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/fecha_partido?partido_id=no_existo")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==404
		assert "error" in contenido
		assert "fecha_ida" not in contenido

def test_pagina_obtener_fecha_partido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/fecha_partido?partido_id=20190622")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==404
		assert "error" not in contenido
		assert "fecha_ida" in contenido
		assert "2019-06-22" in contenido

def test_pagina_obtener_ciudades_pais_trayectos_sin_pais(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/ciudades_pais_trayectos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==400
		assert "error" in contenido

def test_pagina_obtener_ciudades_pais_trayectos_pais_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/ciudades_pais_trayectos?pais=no_existo")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==404
		assert "error" in contenido

def test_pagina_obtener_ciudades_pais_trayectos(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/ciudades_pais_trayectos?pais=España")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==404
		assert "error" not in contenido

def test_pagina_obtener_estadio_partido_sin_partido_id(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio_partido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==400
		assert "error" in contenido
		assert "estadio" not in contenido

def test_pagina_obtener_estadio_partido_partido_id_no_existe(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio_partido?partido_id=no_existo")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==404
		assert "error" in contenido
		assert "estadio" not in contenido

def test_pagina_obtener_estadio_partido(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/estadio_partido?partido_id=20190622")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==404
		assert "error" not in contenido
		assert "estadio" in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_existen_todos(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido?todos=True")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'div class="tarjeta-anadir-partido-asistido">' in contenido
		assert '<p class="titulo-pagina-anadir-partido-asistido">' in contenido
		assert '<button type="button" class="boton-todos-partidos"' in contenido
		assert 'recientes.png' not in contenido
		assert '?todos=True' not in contenido
		assert 'todos.png' in contenido
		assert '<p class="etiqueta">' in contenido
		assert "No hay partidos disponibles para añadir..." not in contenido
		assert '<div class="contenedor-comentario">' in contenido
		assert '<div class="contenedor-checkbox-partido-favorito">' in contenido
		assert '<div class="contenedor-imagen">' in contenido
		assert '<div class="contenedor-seccion-on-tour">' in contenido
		assert '<div class="contenedor-on-tour">' in contenido
		assert '<div class="seccion-on-tour-partido-asistido"' in contenido
		assert '<div class="contenedor-datos-ida">' in contenido
		assert '<select id="pais-ida" name="pais-ida"' in contenido
		assert '<select id="ciudad-ida" name="ciudad-ida"' in contenido
		assert '<select id="ciudad-ida-estadio" name="ciudad-ida-estadio"' in contenido
		assert '<select id="transporte-ida" name="transporte-ida"' in contenido
		assert '<div class="contenedor-datos-vuelta">' in contenido
		assert '<select id="pais-vuelta" name="pais-vuelta"' in contenido
		assert '<select id="ciudad-vuelta" name="ciudad-vuelta"' in contenido
		assert '<select id="ciudad-vuelta-estadio" name="ciudad-vuelta-estadio"' in contenido
		assert '<select id="transporte-vuelta" name="transporte-vuelta"' in contenido
		assert '<option value="España" selected hidden>España</option>' in contenido
		assert '<option value="Madrid" selected>Madrid</option>' in contenido
		assert '<option value="Madrid">Metropolitano</option>' not in contenido
		assert '<div class="contenedor-checkbox-teletrabajo">' in contenido
		assert "max='2019-06-22'" not in contenido
		assert "min='2019-06-22'" not in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_partido_no_defecto(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<option value="sin-seleccion" selected disabled hidden>' in contenido
		assert '<option value="sin-seleccion" disabled hidden>' not in contenido
		assert '<option value="20190622" selected>' not in contenido
		assert '<option value="20190622">' in contenido
		assert '<option value="metropolitano">Metropolitano</option>' not in contenido
		assert "max='2019-06-22'" not in contenido
		assert "min='2019-06-22'" not in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_partido_defecto(cliente, conexion_entorno_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido?partido_id=20190622&todos=True")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<option value="sin-seleccion" selected disabled hidden>' not in contenido
		assert '<option value="sin-seleccion" disabled hidden>' in contenido
		assert '<option value="20190622" selected>' in contenido
		assert '<option value="20190622">' not in contenido
		assert '<div class="contenedor-seccion-on-tour">' in contenido
		assert '<div class="contenedor-on-tour">' in contenido
		assert '<div class="seccion-on-tour-partido-asistido"' in contenido
		assert '<div class="contenedor-datos-ida">' in contenido
		assert '<select id="pais-ida" name="pais-ida"' in contenido
		assert '<select id="ciudad-ida" name="ciudad-ida"' in contenido
		assert '<select id="ciudad-ida-estadio" name="ciudad-ida-estadio"' in contenido
		assert '<select id="transporte-ida" name="transporte-ida"' in contenido
		assert '<div class="contenedor-datos-vuelta">' in contenido
		assert '<select id="pais-vuelta" name="pais-vuelta"' in contenido
		assert '<select id="ciudad-vuelta" name="ciudad-vuelta"' in contenido
		assert '<select id="ciudad-vuelta-estadio" name="ciudad-vuelta-estadio"' in contenido
		assert '<select id="transporte-vuelta" name="transporte-vuelta"' in contenido
		assert '<option value="España" selected hidden>España</option>' in contenido
		assert '<option value="Madrid" selected>Madrid</option>' in contenido
		assert '<option value="Madrid">Metropolitano</option>' in contenido
		assert '<div class="contenedor-checkbox-teletrabajo">' in contenido
		assert "max='2019-06-22'" in contenido
		assert "min='2019-06-22'" in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_partido_defecto_sin_estadio(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("DELETE FROM estadios")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido?partido_id=20190622&todos=True")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<option value="sin-seleccion" selected disabled hidden>' not in contenido
		assert '<option value="sin-seleccion" disabled hidden>' in contenido
		assert '<option value="20190622" selected>' in contenido
		assert '<option value="20190622">' not in contenido
		assert '<div class="contenedor-seccion-on-tour">' in contenido
		assert '<div class="contenedor-on-tour">' in contenido
		assert '<div class="seccion-on-tour-partido-asistido"' in contenido
		assert '<div class="contenedor-datos-ida">' in contenido
		assert '<select id="pais-ida" name="pais-ida"' in contenido
		assert '<select id="ciudad-ida" name="ciudad-ida"' in contenido
		assert '<select id="ciudad-ida-estadio" name="ciudad-ida-estadio"' in contenido
		assert '<select id="transporte-ida" name="transporte-ida"' in contenido
		assert '<div class="contenedor-datos-vuelta">' in contenido
		assert '<select id="pais-vuelta" name="pais-vuelta"' in contenido
		assert '<select id="ciudad-vuelta" name="ciudad-vuelta"' in contenido
		assert '<select id="ciudad-vuelta-estadio" name="ciudad-vuelta-estadio"' in contenido
		assert '<select id="transporte-vuelta" name="transporte-vuelta"' in contenido
		assert '<option value="España" selected hidden>España</option>' in contenido
		assert '<option value="Madrid" selected>Madrid</option>' in contenido
		assert '<option value="Madrid">Metropolitano</option>' not in contenido
		assert '<div class="contenedor-checkbox-teletrabajo">' in contenido
		assert "max='2019-06-22'" in contenido
		assert "min='2019-06-22'" in contenido

def test_pagina_anadir_partido_asistido_partidos_no_asistidos_partido_defecto_sin_ciudad_estadio(cliente, conexion_entorno_usuario):

	conexion_entorno_usuario.c.execute("UPDATE estadios SET Ciudad=NULL")

	conexion_entorno_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_partido_asistido?partido_id=20190622&todos=True")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<option value="sin-seleccion" selected disabled hidden>' not in contenido
		assert '<option value="sin-seleccion" disabled hidden>' in contenido
		assert '<option value="20190622" selected>' in contenido
		assert '<option value="20190622">' not in contenido
		assert '<div class="contenedor-seccion-on-tour">' in contenido
		assert '<div class="contenedor-on-tour">' in contenido
		assert '<div class="seccion-on-tour-partido-asistido"' in contenido
		assert '<div class="contenedor-datos-ida">' in contenido
		assert '<select id="pais-ida" name="pais-ida"' in contenido
		assert '<select id="ciudad-ida" name="ciudad-ida"' in contenido
		assert '<select id="ciudad-ida-estadio" name="ciudad-ida-estadio"' in contenido
		assert '<select id="transporte-ida" name="transporte-ida"' in contenido
		assert '<div class="contenedor-datos-vuelta">' in contenido
		assert '<select id="pais-vuelta" name="pais-vuelta"' in contenido
		assert '<select id="ciudad-vuelta" name="ciudad-vuelta"' in contenido
		assert '<select id="ciudad-vuelta-estadio" name="ciudad-vuelta-estadio"' in contenido
		assert '<select id="transporte-vuelta" name="transporte-vuelta"' in contenido
		assert '<option value="España" selected hidden>España</option>' in contenido
		assert '<option value="Madrid" selected>Madrid</option>' in contenido
		assert '<option value="Madrid">Metropolitano</option>' not in contenido
		assert '<div class="contenedor-checkbox-teletrabajo">' in contenido
		assert "max='2019-06-22'" in contenido
		assert "min='2019-06-22'" in contenido