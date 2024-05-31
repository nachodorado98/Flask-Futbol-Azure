from src.extraer_equipos_liga import extraerDataEquiposLiga

for liga in ["primera", "segunda", "bundesliga", "premier", "ligue_1", "portugal"]:

	data=extraerDataEquiposLiga(liga)

	print(data)