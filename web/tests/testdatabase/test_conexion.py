def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_futbol_data"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "usuarios" in tablas 
	assert "paises" in tablas
	assert "ciudades" in tablas
	assert "equipos" in tablas
	assert "partidos" in tablas
	assert "estadios" in tablas
	assert "equipo_estadio" in tablas
	assert "competiciones" in tablas
	assert "competiciones_campeones" in tablas
	assert "partido_competicion" in tablas
	assert "partido_goleador" in tablas
	assert "jugadores" in tablas
	assert "entrenadores" in tablas
	assert "jugadores_equipo" in tablas
	assert "jugadores_seleccion" in tablas
	assert "partidos_asistidos" in tablas
	assert "partido_asistido_favorito" in tablas
	
def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

def test_vaciar_bbdd(conexion_entorno_usuario):

	conexion_entorno_usuario.insertarPartidoAsistido("20190622", "nacho98", "comentario")

	conexion_entorno_usuario.insertarPartidoAsistidoFavorito("20190622", "nacho98")

	tablas=["equipos", "partidos", "estadios", "equipo_estadio", "competiciones", "competiciones_campeones",
			"partido_competicion", "jugadores", "jugadores_equipo", "jugadores_seleccion", "entrenadores",
			"partido_goleador", "usuarios", "partidos_asistidos", "partido_asistido_favorito"]

	for tabla in tablas:

		conexion_entorno_usuario.c.execute(f"SELECT * FROM {tabla}")

		assert conexion_entorno_usuario.c.fetchall()

	conexion_entorno_usuario.vaciarBBDD()

	for tabla in tablas:

		conexion_entorno_usuario.c.execute(f"SELECT * FROM {tabla}")

		assert not conexion_entorno_usuario.c.fetchall()