import pytest

def test_tabla_proximos_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()

def test_obtener_proximos_partidos_equipo_no_existe_equipo(conexion):

	assert not conexion.obtenerProximosPartidosEquipo("atletico-madrid", 5)

def test_obtener_proximos_partidos_equipo_no_existe_partido(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerProximosPartidosEquipo("atletico-madrid", 5)

def test_obtener_proximos_partidos_equipo(conexion_entorno):

	proximos_partidos=conexion_entorno.obtenerProximosPartidosEquipo("atletico-madrid", 5)

	assert len(proximos_partidos)==1

def test_obtener_proximos_partidos_equipo_calendario_no_existe_equipo(conexion):

	assert not conexion.obtenerProximosPartidosEquipoCalendario("atletico-madrid", "2019-06")

def test_obtener_proximos_partidos_equipo_calendario_no_existe_partido(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerProximosPartidosEquipoCalendario("atletico-madrid", "2019-06")

def test_obtener_proximos_partidos_equipo_calendario_no_ano_mes(conexion_entorno):

	assert not conexion_entorno.obtenerProximosPartidosEquipoCalendario("atletico-madrid", "2019-06")

def test_obtener_proximos_partidos_equipo_calendario(conexion_entorno):

	proximos_partidos=conexion_entorno.obtenerProximosPartidosEquipoCalendario("atletico-madrid", "2020-06")

	assert len(proximos_partidos)==1

def test_obtener_fecha_minima_maxima_proximos_partidos_no_existe_equipo(conexion):

	assert not conexion.obtenerFechaMinimaMaximaProximosPartidos("atletico-madrid")

def test_obtener_fecha_minima_maxima_proximos_partidos_no_existen_partidos(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerFechaMinimaMaximaProximosPartidos("atletico-madrid")

def test_obtener_fecha_minima_maxima_proximos_partidos_un_solo_partido(conexion_entorno):

	fecha_minima, fecha_maxima=conexion_entorno.obtenerFechaMinimaMaximaProximosPartidos("atletico-madrid")

	assert fecha_minima=="2020-06-22"
	assert fecha_maxima=="2020-06-22"

@pytest.mark.parametrize(["fechas", "minima", "maxima"],
	[
		(["2019-06-22", "2020-01-20", "1998-02-16", "1999-08-06"], "1998-02-16", "2020-01-20"),
		(["2019-06-22", "2000-01-20", "1998-02-16", "1999-08-06"], "1998-02-16", "2019-06-22"),
		(["2019-06-22", "2020-01-20", "1999-08-06"], "1999-08-06", "2020-01-20"),
	]
)
def test_obtener_fecha_minima_maxima_proximos_partidos(conexion, fechas, minima, maxima):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	for numero, fecha in enumerate(fechas):

		conexion.c.execute(f"""INSERT INTO proximos_partidos
								VALUES('2020062{numero}', 'atletico-madrid', 'atletico-madrid', '{fecha}', '22:00', 'Liga')""")

	conexion.confirmar()
											
	fecha_minima, fecha_maxima=conexion.obtenerFechaMinimaMaximaProximosPartidos("atletico-madrid")

	assert fecha_minima==minima
	assert fecha_maxima==maxima

def test_obtener_fecha_primer_proximo_partido_no_existe_equipo(conexion):

	assert not conexion.obtenerFechaPrimerProximoPartido("atletico-madrid")

def test_obtener_fecha_primer_proximo_partido_no_existen_partidos(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerFechaPrimerProximoPartido("atletico-madrid")

def test_obtener_fecha_primer_proximo_partido_un_solo_partido(conexion_entorno):

	fecha=conexion_entorno.obtenerFechaPrimerProximoPartido("atletico-madrid")

	assert fecha=="2020-06-22"

@pytest.mark.parametrize(["fechas", "primer_fecha"],
	[
		(["2019-06-22", "2019-06-12", "2019-06-15", "2019-06-21", "2019-06-02"], "2019-06-02"),
		(["2019-12-22", "2019-07-12", "2019-01-15", "2019-11-21", "2019-12-12"], "2019-01-15"),
		(["2019-12-22", "2019-07-12", "2017-11-25", "2021-11-21", "2020-12-12"], "2017-11-25")
	]
)
def test_obtener_fecha_primer_proximo_partido_varios(conexion, fechas, primer_fecha):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid')""")

	for numero, fecha in enumerate(fechas):

		conexion.c.execute(f"""INSERT INTO proximos_partidos
								VALUES('{fecha}-id', 'atletico-madrid', 'atletico-madrid', '{fecha}', '22:00', 'Liga')""")

	conexion.confirmar()

	fecha=conexion.obtenerFechaPrimerProximoPartido("atletico-madrid")

	assert fecha==primer_fecha

@pytest.mark.parametrize(["partido_id"],
	[("20190622",),("2023986382",),("20197589",),("2020625",),("201976809",),("20195666",),("20236517",),("20200622",)]
)
def test_existe_proximo_partido_no_existe(conexion, partido_id):

	assert not conexion.existe_proximo_partido(partido_id)

def test_existe_proximo_partido(conexion_entorno):

	assert conexion_entorno.existe_proximo_partido("20200622")

@pytest.mark.parametrize(["partido_id"],
	[("20190622",),("2023986382",),("20197589",),("2020625",),("201976809",),("20195666",),("20236517",),("20200622",)]
)
def test_obtener_proximo_partido_no_existe(conexion, partido_id):

	assert not conexion.obtenerProximoPartido(partido_id)

def test_obtener_proximo_partido(conexion_entorno):

	assert conexion_entorno.obtenerProximoPartido("20200622")

def test_equipo_proximo_partido_no_existe_partido(conexion):

	assert not conexion.equipo_proximo_partido("atletico-madrid", "20200622")

def test_equipo_proximo_partido_no_existe_equipo(conexion_entorno):

	assert not conexion_entorno.equipo_proximo_partido("atletico", "20200622")

def test_equipo_proximo_partido_equipo_distinto(conexion_entorno):

	assert not conexion_entorno.equipo_proximo_partido("betis", "20200622")

def test_equipo_proximo_partido(conexion_entorno):

	assert conexion_entorno.equipo_proximo_partido("atletico-madrid", "20200622")

def test_obtener_proximo_partido_porra_no_existen_partidos(conexion):

	assert not conexion.obtenerProximoPartidoPorra("atletico-madrid")

def test_obtener_proximo_partido_porra(conexion_entorno):

	assert conexion_entorno.obtenerProximoPartidoPorra("atletico-madrid")

def test_obtener_proximo_partido_porra_existen_varios(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO proximos_partidos
									VALUES ('20210622', 'atletico-madrid', 'atletico-madrid', '2021-06-22', '22:00', 'Liga'),
									('20190622', 'atletico-madrid', 'atletico-madrid', '2019-06-22', '22:00', 'Liga'),
									('20250622', 'atletico-madrid', 'atletico-madrid', '2025-06-22', '22:00', 'Liga')""")

	conexion_entorno.confirmar()

	partido_id=conexion_entorno.obtenerProximoPartidoPorra("atletico-madrid")

	assert partido_id=="20190622"