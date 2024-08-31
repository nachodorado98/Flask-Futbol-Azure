import pytest

def test_tabla_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM partidos")

	assert not conexion.c.fetchall()

def test_obtener_partidos_equipo_no_existe_equipo(conexion):

	assert not conexion.obtenerPartidosEquipo("atletico-madrid")

def test_obtener_partidos_equipo_no_existe_partido(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerPartidosEquipo("atletico-madrid")

def test_obtener_partidos_equipo(conexion_entorno):

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	assert len(partidos)==1

def test_obtener_partidos_equipo_ganado(conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('1', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria Visitante')""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	assert partidos[0][-1]==1

@pytest.mark.parametrize(["resultados", "ganados"],
	[
		(["Victoria Visitante", "Victoria Penaltis Visitante", "Victoria Visitante", "Victoria Local"], 1),
		(["Visitante", "Victoria Penaltis Local", "Victoria Visitante", "Local"], 2),
		(["Victoria Local", "Victoria Penaltis Local", "Local", "Local Victoria"], 4),
		(["Victoria", "Victoria Visitante Panaltis", "Victoria Visitante", "Empate"], 0)
	]
)
def test_obtener_partidos_equipo_ganados_local(conexion_entorno, resultados, ganados):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', %s)""",
									(numero+1, resultado))

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	partidos_ganados=list(filter(lambda partido: partido[-1]==1, partidos))

	partidos_no_ganados=list(filter(lambda partido: partido[-1]==0, partidos))

	assert len(partidos_ganados)==ganados
	assert len(partidos)==len(partidos_ganados)+len(partidos_no_ganados)

@pytest.mark.parametrize(["resultados", "ganados"],
	[
		(["Victoria Visitante", "Victoria Penaltis Visitante", "Victoria Visitante", "Victoria Local"], 3),
		(["Visitante", "Victoria Penaltis Local", "Victoria Visitante", "Victoria Local"], 2),
		(["Victoria Visitante", "Victoria Penaltis Visitante", "Victoria Visitante", "Visitante Victoria"], 4),
		(["Victoria", "Victoria Local Panaltis", "Victoria Local", "Empate"], 0)
	]
)
def test_obtener_partidos_equipo_ganados_visitante(conexion_entorno, resultados, ganados):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero, resultado in enumerate(resultados):

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', %s)""",
									(numero+1, resultado))

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	partidos_ganados=list(filter(lambda partido: partido[-1]==1, partidos))

	partidos_no_ganados=list(filter(lambda partido: partido[-1]==0, partidos))

	assert len(partidos_ganados)==ganados
	assert len(partidos)==len(partidos_ganados)+len(partidos_no_ganados)

def test_obtener_partidos_equipo_local(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('2', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	assert len(partidos)==2

def test_obtener_partidos_equipo_visitante(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('2', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	assert len(partidos)==2

def test_obtener_partidos_equipo_varios_partidos(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	for numero in range(2,10):

		conexion_entorno.c.execute(f"""INSERT INTO partidos
									VALUES('{numero}', 'rival', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosEquipo("atletico-madrid")

	assert len(partidos)==1

def test_obtener_partidos_equipo_equipo_diferente(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('rival')""")

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('2', 'rival', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerPartidosEquipo("atleti-madrid")

def test_obtener_partidos_local_equipo_no_existe_equipo(conexion):

	assert not conexion.obtenerPartidosEquipoLocal("atletico-madrid")

def test_obtener_partidos_local_equipo_no_existe_partido(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerPartidosEquipoLocal("atletico-madrid")

def test_obtener_partidos_local_equipo(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	partidos_local=conexion.obtenerPartidosEquipoLocal("atletico-madrid")

	assert len(partidos_local)==1

def test_obtener_partidos_local_equipo_varios(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('2', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('3', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('4', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	partidos_local=conexion.obtenerPartidosEquipoLocal("atletico-madrid")

	assert len(partidos_local)==3

def test_obtener_partidos_visitante_equipo_no_existe_equipo(conexion):

	assert not conexion.obtenerPartidosEquipoVisitante("atletico-madrid")

def test_obtener_partidos_visitante_equipo_no_existe_partido(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerPartidosEquipoVisitante("atletico-madrid")

def test_obtener_partidos_visitante_equipo(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	partidos_visitante=conexion.obtenerPartidosEquipoVisitante("atletico-madrid")

	assert len(partidos_visitante)==1

def test_obtener_partidos_visitante_equipo_varios(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('2', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('3', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('4', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.confirmar()

	partidos_visitante=conexion.obtenerPartidosEquipoVisitante("atletico-madrid")

	assert len(partidos_visitante)==2

def test_obtener_partidos_casa_no_existe_equipo(conexion):

	assert not conexion.obtenerPartidosCasa("atletico-madrid")

def test_obtener_partidos_casa_no_existe_partido(conexion_entorno):

	conexion_entorno.c.execute("""DELETE FROM partidos""")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerPartidosCasa("atletico-madrid")

def test_obtener_partidos_casa_no_existe_estadio(conexion_entorno):

	conexion_entorno.c.execute("""DELETE FROM estadios""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosCasa("atletico-madrid")

	assert not partidos[0][10]

def test_obtener_partidos_casa_existe_estadio(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id)
						VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio
							VALUES('1', 'metropolitano')""")

	conexion.confirmar()

	partidos=conexion.obtenerPartidosCasa("atletico-madrid")

	assert partidos[0][10]

def test_obtener_partidos_casa_local_fuera_de_casa(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id)
						VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio
							VALUES('1', 'estadio_rival')""")

	conexion.confirmar()

	partidos=conexion.obtenerPartidosCasa("atletico-madrid")

	assert len(partidos)==0

def test_obtener_partidos_casa_visitante_en_casa(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id)
						VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio
							VALUES('1', 'metropolitano')""")

	conexion.confirmar()

	partidos=conexion.obtenerPartidosCasa("atletico-madrid")

	assert len(partidos)==1

def test_obtener_partidos_casa_varios(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id)
						VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('2', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('3', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('4', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('5', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio
							VALUES('1', 'metropolitano'),
									('2','estadio_rival'),
									('3', 'metropolitano'),
									('4','estadio_rival'),
									('5', 'metropolitano')""")

	conexion.confirmar()

	partidos=conexion.obtenerPartidosCasa("atletico-madrid")

	assert len(partidos)==3

def test_obtener_partidos_fuera_no_existe_equipo(conexion):

	assert not conexion.obtenerPartidosFuera("atletico-madrid")

def test_obtener_partidos_fuera_no_existe_partido(conexion_entorno):

	conexion_entorno.c.execute("""DELETE FROM partidos""")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerPartidosFuera("atletico-madrid")

def test_obtener_partidos_fuera_no_existe_estadio(conexion_entorno):

	conexion_entorno.c.execute("""DELETE FROM estadios""")

	conexion_entorno.confirmar()

	partidos=conexion_entorno.obtenerPartidosFuera("atletico-madrid")

	assert not partidos[0][10]

def test_obtener_partidos_fuera_existe_estadio(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id)
						VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio
							VALUES('1', 'estadio_rival')""")

	conexion.confirmar()

	partidos=conexion.obtenerPartidosFuera("atletico-madrid")

	assert partidos[0][10]

def test_obtener_partidos_fuera_local_fuera_de_casa(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id)
						VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio
							VALUES('1', 'estadio_rival')""")

	conexion.confirmar()

	partidos=conexion.obtenerPartidosFuera("atletico-madrid")

	assert len(partidos)==1

def test_obtener_partidos_fuera_visitante_en_casa(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id)
						VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio
							VALUES('1', 'metropolitano')""")

	conexion.confirmar()

	partidos=conexion.obtenerPartidosFuera("atletico-madrid")

	assert len(partidos)==0

def test_obtener_partidos_fuera_varios(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO estadios (Estadio_Id)
						VALUES('metropolitano'),('estadio_rival')""")

	conexion.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid', 'metropolitano'),('rival', 'estadio_rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('2', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('3', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('4', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria'),
								('5', 'rival', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

	conexion.c.execute("""INSERT INTO partido_estadio
							VALUES('1', 'metropolitano'),
									('2','estadio_rival'),
									('3', 'metropolitano'),
									('4','estadio_rival'),
									('5','estadio_rival')""")

	conexion.confirmar()

	partidos=conexion.obtenerPartidosFuera("atletico-madrid")

	assert len(partidos)==3

def test_obtener_temporadas_equipo_no_existe_equipo(conexion):

	assert not conexion.obtenerTemporadasEquipo("atletico-madrid")

def test_obtener_temporadas_equipo_no_existe_partido(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerTemporadasEquipo("atletico-madrid")

def test_obtener_temporadas_equipo(conexion_entorno):

	temporadas=conexion_entorno.obtenerTemporadasEquipo("atletico-madrid")

	assert len(temporadas)==1
	assert temporadas[0]==2019

@pytest.mark.parametrize(["ids_partidos", "temporadas_unicas"],
	[
		(["2023986382", "20197589", "2020625", "201976809", "20195666", "20236517"], [2023,2020,2019]),
		(["2023986382", "20197589", "2021625", "201976809", "20195666", "20236517"], [2023,2021,2019]),
		(["2024986382", "20197589", "2020625", "201976809", "20195666", "20236517"], [2024,2023,2020,2019]),
		(["2023986382", "20197589", "2019625", "201976809", "20195666", "20236517"], [2023,2019]),
		(["2023986382", "20197589", "2020625", "201976809", "20195666", "20236517","20106363"], [2023,2020,2019,2010])
	]
)
def test_obtener_temporadas_equipo_varios_partidos(conexion_entorno, ids_partidos, temporadas_unicas):

	for id_partido in ids_partidos:

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'atletico-madrid', 'atletico-madrid', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria')""",
									(id_partido,))

	conexion_entorno.confirmar()

	temporadas=conexion_entorno.obtenerTemporadasEquipo("atletico-madrid")

	assert temporadas==temporadas_unicas

@pytest.mark.parametrize(["partido_id"],
	[("20190622",),("2023986382",),("20197589",),("2020625",),("201976809",),("20195666",),("20236517",)]
)
def test_existe_partido_no_existe(conexion, partido_id):

	assert not conexion.existe_partido(partido_id)

def test_existe_partido(conexion_entorno):

	assert conexion_entorno.existe_partido("20190622")

@pytest.mark.parametrize(["partido_id"],
	[("20190622",),("2023986382",),("20197589",),("2020625",),("201976809",),("20195666",),("20236517",)]
)
def test_obtener_partido_no_existe(conexion, partido_id):

	assert not conexion.obtenerPartido(partido_id)

def test_obtener_partido(conexion_entorno):

	assert conexion_entorno.obtenerPartido("20190622")

@pytest.mark.parametrize(["partido_id"],
	[("20190622",),("2023986382",),("20197589",),("2020625",),("201976809",),("20195666",),("20236517",)]
)
def test_equipo_partido_no_existe_partido(conexion, partido_id):

	assert not conexion.equipo_partido("atletico-madrid", partido_id)

def test_equipo_partido_equipo_no_pertecene(conexion_entorno):

	assert not conexion_entorno.equipo_partido("atm", "20190622")

def test_equipo_partido(conexion_entorno):

	assert conexion_entorno.equipo_partido("atletico-madrid", "20190622")

def test_obtener_partido_siguiente_no_existe_partido(conexion):

	assert not conexion.obtenerPartidoSiguiente("20190622", "atletico-madrid")

def test_obtener_partido_siguiente_existe_uno(conexion_entorno):

	assert not conexion_entorno.obtenerPartidoSiguiente("20190622", "atletico-madrid")

def test_obtener_partido_siguiente_no_existe_equipo(conexion_entorno):

	assert not conexion_entorno.obtenerPartidoSiguiente("20190622", "atm")

def test_obtener_partido_siguiente_existe_anterior(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190621', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerPartidoSiguiente("20190622", "atletico-madrid")

def test_obtener_partido_siguiente(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	partido_id=conexion_entorno.obtenerPartidoSiguiente("20190622", "atletico-madrid")

	assert partido_id=="20190623"

@pytest.mark.parametrize(["data", "partido_id_siguiente"],
	[
		([("667658", "2019-02-19"),("664657658", "2019-06-19"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "20197658"),
		([("667658", "2019-06-23"),("664657658", "2019-06-19"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "667658"),
		([("667658", "2019-02-19"),("664657658", "2019-06-25"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "664657658"),
		([("667658", "2019-02-19"),("664657658", "2019-06-19"),("20197658", "2019-07-19"),("661357658", "2019-07-18")], "661357658")
	]
)
def test_obtener_partido_siguiente_varios(conexion_entorno, data, partido_id_siguiente):

	for partido_id, fecha in data:

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'atletico-madrid', 'atletico-madrid', %s, '22:00', 'Liga', '1-0', 'Victoria')""",
									(partido_id, fecha))

	conexion_entorno.confirmar()

	partido_id=conexion_entorno.obtenerPartidoSiguiente("20190622", "atletico-madrid")

	assert partido_id==partido_id_siguiente

def test_obtener_partido_anterior_no_existe_partido(conexion):

	assert not conexion.obtenerPartidoAnterior("20190622", "atletico-madrid")

def test_obtener_partido_anterior_existe_uno(conexion_entorno):

	assert not conexion_entorno.obtenerPartidoAnterior("20190622", "atletico-madrid")

def test_obtener_partido_anterior_no_existe_equipo(conexion_entorno):

	assert not conexion_entorno.obtenerPartidoAnterior("20190622", "atm")

def test_obtener_partido_anterior_existe_siguiente(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190623', 'atletico-madrid', 'atletico-madrid', '2019-06-23', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerPartidoAnterior("20190622", "atletico-madrid")

def test_obtener_partido_anterior(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO partidos
								VALUES('20190621', 'atletico-madrid', 'atletico-madrid', '2019-06-21', '22:00', 'Liga', '1-0', 'Victoria')""")

	conexion_entorno.confirmar()

	partido_id=conexion_entorno.obtenerPartidoAnterior("20190622", "atletico-madrid")

	assert partido_id=="20190621"

@pytest.mark.parametrize(["data", "partido_id_anterior"],
	[
		([("667658", "2019-02-19"),("664657658", "2019-05-19"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "664657658"),
		([("667658", "2019-06-19"),("664657658", "2019-05-19"),("20197658", "2019-07-19"),("661357658", "2019-12-19")], "667658"),
		([("667658", "2019-02-19"),("664657658", "2019-05-19"),("20197658", "2019-05-20"),("661357658", "2019-12-19")], "20197658"),
		([("667658", "2019-02-19"),("664657658", "2019-05-19"),("20197658", "2019-07-19"),("661357658", "2019-06-13")], "661357658")
	]
)
def test_obtener_partido_anterior_varios(conexion_entorno, data, partido_id_anterior):

	for partido_id, fecha in data:

		conexion_entorno.c.execute("""INSERT INTO partidos
									VALUES(%s, 'atletico-madrid', 'atletico-madrid', %s, '22:00', 'Liga', '1-0', 'Victoria')""",
									(partido_id, fecha))

	conexion_entorno.confirmar()

	partido_id=conexion_entorno.obtenerPartidoAnterior("20190622", "atletico-madrid")

	assert partido_id==partido_id_anterior

def test_ultimo_partido_equipo_no_existe(conexion):

	assert not conexion.ultimoPartidoEquipo("atletico-madrid")

def test_ultimo_partido_equipo(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid'),('rival')""")

	conexion.c.execute("""INSERT INTO partidos
						VALUES('1', 'atletico-madrid', 'rival', '2019-06-22', '20:00', 'Liga', '1-0', 'Victoria Local'),
								('2', 'rival', 'atletico-madrid', '2019-07-22', '20:00', 'Liga', '1-0', 'Victoria Local'),
								('3', 'atletico-madrid', 'rival', '2024-06-22', '20:00', 'Liga', '1-0', 'Victoria Local'),
								('4', 'rival', 'atletico-madrid', '2020-12-02', '20:00', 'Liga', '1-0', 'Victoria Local'),
								('5', 'rival', 'atletico-madrid', '2019-04-13', '20:00', 'Liga', '1-0', 'Victoria Local')""")

	conexion.c.execute("""INSERT INTO competiciones
						VALUES('primera', 'Primera', 'primera-division-ea', 'es')""")

	conexion.c.execute("""INSERT INTO partido_competicion
						VALUES('1', 'primera'),('2', 'primera'),('3', 'primera'),('4', 'primera'),('5', 'primera')""")

	conexion.confirmar()

	assert conexion.ultimoPartidoEquipo("atletico-madrid")