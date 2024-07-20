import pytest

def test_pagina_partidos_sin_partidos(cliente, conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.confirmar()

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Partidos del None" in contenido
	assert f'<img src="/static/imagenes/favoritos/atletico-madrid.png'in contenido
	assert "No hay ningun partido disponible del None..." in contenido
	assert '<div class="tarjetas-partidos">' not in contenido
	assert '<div class="tarjetas-partidos-wrapper">' not in contenido
	assert '<div class="tarjeta-partido">' not in contenido
	assert '<div class="info-partido">' not in contenido

def test_pagina_partidos_con_partido(cliente, conexion_entorno):

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Partidos del None" in contenido
	assert f'<img src="/static/imagenes/favoritos/atletico-madrid.png'in contenido
	assert "No hay ningun partido disponible del None..." not in contenido
	assert '<div class="tarjetas-partidos">' in contenido
	assert '<div class="tarjetas-partidos-wrapper">' in contenido
	assert '<div class="tarjeta-partido">' in contenido
	assert '<div class="info-partido">' in contenido

@pytest.mark.parametrize(["nombre_completo"],
	[("atleti",),("atm",),("Club Atletico de Madrid",)]
)
def test_pagina_partidos_con_nombre_equipo(cliente, conexion, nombre_completo):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre_Completo)
						VALUES('atletico-madrid', %s)""", (nombre_completo,))

	conexion.confirmar()

	cliente.post("/singin", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
									"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
									"fecha-nacimiento":"1998-02-16",
									"equipo":"atletico-madrid"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f"Partidos del {nombre_completo}" in contenido