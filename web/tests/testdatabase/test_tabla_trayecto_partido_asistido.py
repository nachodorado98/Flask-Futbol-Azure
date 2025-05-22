import pytest
import pandas as pd

def test_tabla_trayecto_partido_asistido_vacia(conexion):

	conexion.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20190622", "nacho")]
)
def test_insertar_trayecto_partido_asistido(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido(partido_id, usuario, "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_I_0", partido_id, usuario, "I", 103, "Transporte", 103)

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	trayectos_partido_asistido=conexion_entorno.c.fetchall()

	assert len(trayectos_partido_asistido)==1

@pytest.mark.parametrize(["partido_id", "usuario"],
	[("20190622", "nacho98"), ("20190622", "nacho948"),("20190622", "nacho")]
)
def test_insertar_trayecto_partido_asistido_ida_vuelta(conexion_entorno, partido_id, usuario):

	conexion_entorno.insertarUsuario(usuario, "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido(partido_id, usuario, "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_I_0", partido_id, usuario, "I", 103, "Transporte", 103)

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_V_0", partido_id, usuario, "V", 103, "Transporte", 103)

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	trayectos_partido_asistido=conexion_entorno.c.fetchall()

	assert len(trayectos_partido_asistido)==2

def test_eliminar_trayectos_partido_asistido_no_existen_partidos(conexion):

	conexion.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion.c.fetchall()

	conexion.eliminarTrayectosPartidoAsistido("20190622", "nacho")

	conexion.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion.c.fetchall()

def test_eliminar_trayectos_partido_asistido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

	conexion_entorno.eliminarTrayectosPartidoAsistido("20190622", "otro")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

def test_eliminar_trayectos_partido_asistido_no_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

	conexion_entorno.eliminarTrayectosPartidoAsistido("20190622", "nacho")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

def test_eliminar_trayectos_partido_asistido_no_existen_trayectos(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

	conexion_entorno.eliminarTrayectosPartidoAsistido("20190622", "nacho")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

def test_eliminar_trayectos_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_I_0", "20190622", "nacho", "I", 103, "Transporte", 103)

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert conexion_entorno.c.fetchall()

	conexion_entorno.eliminarTrayectosPartidoAsistido("20190622", "nacho")

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	assert not conexion_entorno.c.fetchall()

def test_obtener_trayecto_partido_asistido_no_existen_partidos(conexion):

	assert not conexion.obtenerTrayectoPartidoAsistido("20190622", "nacho", "I")

def test_obtener_trayecto_partido_asistido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "otro", "I")

def test_obtener_trayecto_partido_asistido_no_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "I")

def test_obtener_trayecto_partido_asistido_no_existen_trayectos(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "I")

def test_obtener_trayecto_partido_asistido_no_existe_tipo_trayecto(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_I_0", "20190622", "nacho", "I", 103, "Transporte", 103)

	assert not conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "N")

def test_obtener_trayecto_partido_asistido_ida(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_I_0", "20190622", "nacho", "I", 103, "Transporte", 103)

	trayecto=conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "I")

	assert trayecto[0]=="I"
	assert trayecto[1]=="Transporte"
	assert trayecto[2]=="Madrid"
	assert trayecto[3]!=trayecto[6]
	assert trayecto[4]!=trayecto[7]
	assert trayecto[5]=="Metropolitano"
	assert trayecto[8]=="transporte"
	assert trayecto[9]=="23"

def test_obtener_trayecto_partido_asistido_vuelta(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_V_0", "20190622", "nacho", "V", 103, "Transporte Nacho", 103)

	trayecto=conexion_entorno.obtenerTrayectoPartidoAsistido("20190622", "nacho", "V")

	assert trayecto[0]=="V"
	assert trayecto[1]=="Transporte Nacho"
	assert trayecto[2]=="Metropolitano"
	assert trayecto[3]!=trayecto[6]
	assert trayecto[4]!=trayecto[7]
	assert trayecto[5]=="Madrid"
	assert trayecto[8]=="23"
	assert trayecto[9]=="transporte_nacho"

@pytest.mark.parametrize(["numero_trayectos"],
	[(1,), (5,), (2,), (13,), (22,), (0,)]
)
def test_insertar_trayectos_partido_asistido(conexion_entorno, numero_trayectos):

	conexion_entorno.insertarUsuario("golden", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "golden", "comentario")

	columnas=["Trayecto_Id", "Partido_Id", "Usuario_Id", "Tipo", "Codigo_Ciudad_Origen", "Transporte", "Codigo_Ciudad_Destino", "Correcto"]

	trayectos=[[f"trayecto_id_I_{numero+1}", "20190622", "golden", "I", 103, "Avion", 160, True] for numero in range(numero_trayectos)]

	df=pd.DataFrame(trayectos, columns=columnas)

	conexion_entorno.insertarTrayectosPartidoAsistido(df)

	conexion_entorno.c.execute("SELECT * FROM trayecto_partido_asistido")

	trayectos_partido_asistido=conexion_entorno.c.fetchall()

	assert len(trayectos_partido_asistido)==numero_trayectos










def test_obtener_trayectos_partido_asistido_no_existen_partidos(conexion):

	assert not conexion.obtenerTrayectosPartidoAsistido("20190622", "nacho", "I")

def test_obtener_trayectos_partido_asistido_no_existe_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerTrayectosPartidoAsistido("20190622", "otro", "I")

def test_obtener_trayectos_partido_asistido_no_existe_partido_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerTrayectosPartidoAsistido("20190622", "nacho", "I")

def test_obtener_trayectos_partido_asistido_no_existen_trayectos(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert not conexion_entorno.obtenerTrayectosPartidoAsistido("20190622", "nacho", "I")

def test_obtener_trayectos_partido_asistido_no_existe_tipo_trayecto(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_I_0", "20190622", "nacho", "I", 103, "Transporte", 103)

	assert not conexion_entorno.obtenerTrayectosPartidoAsistido("20190622", "nacho", "N")

def test_obtener_trayectos_partido_asistido_un_trayecto_ida(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_I_0", "20190622", "nacho", "I", 103, "Transporte", 103)

	trayectos=conexion_entorno.obtenerTrayectosPartidoAsistido("20190622", "nacho", "I")

	assert len(trayectos)==1

	trayecto=trayectos[0]

	assert trayecto[0]=="trayecto_id_I_0"
	assert trayecto[1]=="I"
	assert trayecto[2]=="Transporte"
	assert trayecto[3]=="Madrid"
	assert trayecto[4]=="España"
	assert trayecto[5]!=trayecto[9]
	assert trayecto[6]!=trayecto[10]
	assert trayecto[7]=="Metropolitano"
	assert trayecto[8]=="España"
	assert trayecto[11]=="transporte"
	assert trayecto[12]=="23"
	assert trayecto[13]=="origen"

def test_obtener_trayectos_partido_asistido_un_trayecto_vuelta(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("trayecto_id_V_0", "20190622", "nacho", "V", 103, "Transporte", 103)

	trayectos=conexion_entorno.obtenerTrayectosPartidoAsistido("20190622", "nacho", "V")

	assert len(trayectos)==1

	trayecto=trayectos[0]

	assert trayecto[0]=="trayecto_id_V_0"
	assert trayecto[1]=="V"
	assert trayecto[2]=="Transporte"
	assert trayecto[3]=="Metropolitano"
	assert trayecto[4]=="España"
	assert trayecto[5]!=trayecto[9]
	assert trayecto[6]!=trayecto[10]
	assert trayecto[7]=="Madrid"
	assert trayecto[8]=="España"
	assert trayecto[11]=="23"
	assert trayecto[12]=="transporte"
	assert trayecto[13]=="estadio_mapa"

def test_obtener_trayectos_partido_asistido_idas(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_I_1", "20190622", "nacho", "I", 160, "Avion", 3025)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_I_2", "20190622", "nacho", "I", 3025, "Cercanias", 2947)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_I_3", "20190622", "nacho", "I", 2947, "Metro", 103)

	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_1", "20190622", "nacho", "V", 103, "Avion", 34)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_2", "20190622", "nacho", "V", 34, "Cercanias", 211)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_3", "20190622", "nacho", "V", 211, "Metro", 35)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_4", "20190622", "nacho", "V", 35, "Tren", 1876)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_5", "20190622", "nacho", "V", 1876, "Pie", 160)

	trayectos=conexion_entorno.obtenerTrayectosPartidoAsistido("20190622", "nacho", "I")

	assert len(trayectos)==3

	for numero, trayecto in enumerate(trayectos):

		assert trayecto[0]==f"id_20190622_nacho_I_{numero+1}"
		assert trayecto[1]=="I"
		assert trayecto[5]!=trayecto[9]
		assert trayecto[6]!=trayecto[10]

	assert trayectos[0][11]=="avion"
	assert trayectos[0][12]=="avion"
	assert trayectos[0][13]=="origen"
	assert trayectos[-1][11]=="metro"
	assert trayectos[-1][12]=="23"
	assert trayectos[-1][13]=="estadio_mapa"

	for trayecto in trayectos[1:-1]:

		assert trayecto[13]=="destino"

def test_obtener_trayectos_partido_asistido_vueltas(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_I_1", "20190622", "nacho", "I", 160, "Avion", 3025)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_I_2", "20190622", "nacho", "I", 3025, "Cercanias", 2947)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_I_3", "20190622", "nacho", "I", 2947, "Metro", 103)

	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_1", "20190622", "nacho", "V", 103, "Avion", 34)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_2", "20190622", "nacho", "V", 34, "Cercanias", 211)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_3", "20190622", "nacho", "V", 211, "Metro", 35)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_4", "20190622", "nacho", "V", 35, "Tren", 1876)
	conexion_entorno.insertarTrayectoPartidoAsistido("id_20190622_nacho_V_5", "20190622", "nacho", "V", 1876, "Pie", 160)

	trayectos=conexion_entorno.obtenerTrayectosPartidoAsistido("20190622", "nacho", "V")

	assert len(trayectos)==5

	for numero, trayecto in enumerate(trayectos):

		assert trayecto[0]==f"id_20190622_nacho_V_{numero+1}"
		assert trayecto[1]=="V"
		assert trayecto[5]!=trayecto[9]
		assert trayecto[6]!=trayecto[10]

	assert trayectos[0][11]=="23"
	assert trayectos[0][12]=="avion"
	assert trayectos[0][13]=="estadio_mapa"
	assert trayectos[-1][11]=="pie"
	assert trayectos[-1][12]=="pie"
	assert trayectos[-1][13]=="origen"

	for trayecto in trayectos[1:-1]:

		assert trayecto[13]=="destino"