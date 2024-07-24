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