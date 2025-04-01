import re
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import List, Dict, Optional
import os
import folium
import geopandas as gpd
import fiona
from shapely.geometry import Point
import pandas as pd

from src.config import URL_DATALAKE_PAISES, URL_DATALAKE_ESTADIOS

from .configutils import TRANSPORTES

def usuario_correcto(usuario:str)->bool:

	return bool(usuario and usuario.isalnum())

def nombre_correcto(nombre:str)->bool:

	return bool(nombre and nombre.isalpha())

def apellido_correcto(apellido:str)->bool:

	return nombre_correcto(apellido)

def contrasena_correcta(contrasena:str)->bool:

	if not contrasena:

		return None

	patron=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

	return bool(re.match(patron, contrasena))

def fecha_correcta(fecha:str, minimo:str="1900-01-01")->bool:

	hoy=datetime.today()

	ano_maximo=hoy.year-18

	fecha_maxima=f"{ano_maximo}-{hoy.month:02d}-{hoy.day:02d}"

	if hoy.month==2 and hoy.day==29:

		if not (ano_maximo%4==0 and (ano_maximo%100!=0 or ano_maximo%400==0)):

			fecha_maxima=f"{ano_maximo}-02-28"

	try:

		fecha_nacimiento=datetime.strptime(fecha, "%Y-%m-%d")

		return bool(datetime.strptime(minimo, "%Y-%m-%d")<=fecha_nacimiento<=datetime.strptime(fecha_maxima, "%Y-%m-%d"))

	except Exception:

		return False

def equipo_correcto(equipo:str)->bool:

	if not equipo:

		return False

	return bool(re.fullmatch(r"[a-zA-Z0-9-]+", equipo))

def correo_correcto(correo:str)->bool:

	if not correo:

		return False

	patron=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

	return bool(re.match(patron, correo))

def datos_correctos(usuario:str, nombre:str, apellido:str, contrasena:str, fecha_nacimiento:str, equipo:str, correo:str)->bool:

	return (usuario_correcto(usuario) and
			nombre_correcto(nombre) and
			apellido_correcto(apellido) and
			contrasena_correcta(contrasena) and
			fecha_correcta(fecha_nacimiento) and
			equipo_correcto(equipo) and
			correo_correcto(correo))

def generarHash(contrasena:str)->str:

	objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

	return objeto_hash.hash(contrasena)

def comprobarHash(contrasena:str, contrasena_hash:str)->bool:

	objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

	return objeto_hash.verify(contrasena, contrasena_hash)

def anadirPuntos(numero:str)->str:

	numero_con_puntos=""

	for indice, digito in enumerate(numero[::-1], 1):

		numero_con_puntos+=digito

		if indice%3==0 and indice!=len(numero[::-1]):

			numero_con_puntos+="."

	return numero_con_puntos[::-1]

def limpiarResultadosPartidos(partidos:List[tuple])->Dict:

	partidos_ganados=len(list(filter(lambda partido: partido[-3]==1, partidos)))

	partidos_perdidos=len(list(filter(lambda partido: partido[-2]==1, partidos)))

	partidos_empatados=len(list(filter(lambda partido: partido[-1]==1, partidos)))

	return {"ganados":partidos_ganados,
			"perdidos": partidos_perdidos,
			"empatados": partidos_empatados}

def obtenerNombrePaisSeleccionado(paises:List[tuple], codigo_pais:str)->Optional[str]:

	try:

		return list(filter(lambda pais: pais[0]==codigo_pais, paises))[0][1]

	except Exception:

		return None

def obtenerPaisesNoSeleccionados(paises:List[tuple], codigo_pais:str)->List[tuple]:

	paises_no_seleccionados=list(filter(lambda pais: pais[0]!=codigo_pais, paises))

	return [(pais[0], pais[1]) for pais in paises_no_seleccionados]

def crearCarpeta(ruta:str)->None:

	if not os.path.exists(ruta):

		os.mkdir(ruta)

		print(f"Carpeta creada: {ruta}")

def borrarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		os.rmdir(ruta)

		print(f"Carpeta borrada: {ruta}")

def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			try:

				if not os.path.isdir(os.path.join(ruta, archivo)):

					os.remove(os.path.join(ruta, archivo))

				else:

					os.rmdir(os.path.join(ruta, archivo))

			except Exception:
				
				pass

def vaciarCarpetaMapasUsuario(ruta:str, nombre_usuario:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			if nombre_usuario in archivo:

				try:

					os.remove(os.path.join(ruta, archivo))

				except Exception:
					
					pass

def obtenerCentroide(datos_estadios:List[tuple])->tuple:

	coordenadas=[(latitud, longitud) for nombre, latitud, longitud, escudo, pais in datos_estadios]

	return obtenerCentroideCoordenadas(coordenadas)

def crearMapaMisEstadios(ruta:str, datos_estadios:List[tuple], nombre_mapa:str, centro_mapa:List=[50.0909, 10.1228], zoom:float=2.4)->None:

	mapa=folium.Map(location=centro_mapa, zoom_start=zoom)

	for nombre, latitud, longitud, escudo, pais in datos_estadios:

		folium.Circle(location=[latitud, longitud],
						radius=2000,
						color="red",
						fill=True,
						fill_color="red",
						fill_opacity=1).add_to(mapa)

	mapa.save(os.path.join(ruta, nombre_mapa))

def crearMapaMisEstadiosDetalle(ruta:str, datos_estadios:List[tuple], nombre_mapa:str, centro_mapa:List=[50.0909, 10.1228], zoom:float=3.5)->None:

	mapa=folium.Map(location=centro_mapa, zoom_start=zoom, min_zoom=zoom)

	for nombre, latitud, longitud, estadio, pais in datos_estadios:

		popup_html=f"""
					<div style="text-align: center;">
						<h4>
							{nombre}
							<img src="{URL_DATALAKE_PAISES}{pais}.png" 
							 alt="Pais" style="width:35px;">
						</h4>
						<img src="{URL_DATALAKE_ESTADIOS}{estadio}.png" 
							 alt="Estadio" style="width:250px;">
					</div>
					"""

		icono_html=f"""
					<div style="background-color: #ffcccc ; width: 35px; height: 35px; border-radius: 50%; text-align: center; border: 1px solid red; border-width: 1px;"">
						<img src="/static/imagenes/iconos/estadio_mapa.png" style="width: 25px; height: 25px; margin-top: 4px;">
					</div>
					"""

		folium.Marker(location=[latitud, longitud],
						popup=folium.Popup(popup_html, max_width=400),
						icon=folium.DivIcon(html=icono_html)).add_to(mapa)

	mapa.save(os.path.join(ruta, nombre_mapa))

def leerGeoJSON(ruta:str)->Optional[gpd.geodataframe.GeoDataFrame]:

	archivo_geojson=os.path.join(ruta, "paises_geojson.geojson")

	try:

		with fiona.open(archivo_geojson, "r") as src:

			features=list(src)

			return gpd.GeoDataFrame.from_features(features, crs=src.crs)

	except Exception as e:

		raise Exception(f"Error al leer el geojson: {ruta}")

def obtenerGeometriaPais(ruta:str, latitud:float, longitud:float)->Optional[gpd.geodataframe.GeoDataFrame]:

	geodataframe=leerGeoJSON(ruta)

	punto=Point(longitud, latitud)

	registros=[row for _, row in geodataframe.iterrows() if row['geometry'].contains(punto)]

	if registros:

		return gpd.GeoDataFrame(registros, columns=geodataframe.columns, crs=geodataframe.crs).drop_duplicates()

	else:

		return gpd.GeoDataFrame(columns=geodataframe.columns, crs=geodataframe.crs)

def obtenerGeometriasPaises(ruta:str, lista_coordenadas:str)->Optional[gpd.geodataframe.GeoDataFrame]:

	geodataframes=[obtenerGeometriaPais(ruta, latitud, longitud) for latitud, longitud in lista_coordenadas]

	return gpd.GeoDataFrame(pd.concat(geodataframes, ignore_index=True)).drop_duplicates()

def crearMapaMisEstadiosDetallePaises(ruta:str, coordenadas:List[tuple], nombre_mapa:str, centro_mapa:List=[50.0909, 10.1228], zoom:float=3.5)->None:

	mapa=folium.Map(location=centro_mapa, zoom_start=zoom, min_zoom=zoom)

	geodataframe=obtenerGeometriasPaises("/app/src/static/geojson", coordenadas)

	folium.GeoJson(geodataframe, name="paises").add_to(mapa)

	mapa.save(os.path.join(ruta, nombre_mapa))

def crearMapaEstadio(ruta:str, estadio:tuple, nombre_mapa:str, zoom:float=15)->None:

	latitud, longitud=estadio[3], estadio[4]

	try:

		mapa=folium.Map(location=[latitud, longitud], zoom_start=zoom)

		icono_html=f"""
					<div style="background-color: #ffcccc ; width: 32px; height: 32px; border-radius: 50%; text-align: center; border: 1px solid red; border-width: 1px;"">
						<img src="/static/imagenes/iconos/estadio_mapa.png" style="width: 23px; height: 23px; margin-top: 4px;">
					</div>
					"""

		folium.Marker(location=[latitud, longitud],
						icon=folium.DivIcon(html=icono_html)).add_to(mapa)

		mapa.save(os.path.join(ruta, nombre_mapa))

	except Exception as e:

		raise Exception("Error al crear el mapa")

def obtenerCompeticionesPartidosUnicas(partidos:List[tuple])->List[str]:

	competiciones_ordenadas=sorted(list(set(list(map(lambda partido: partido[9], partidos)))))

	competiciones_ordenadas.append("Todo")

	return competiciones_ordenadas

def extraerExtension(archivo:str, extension_alternativa:str="jpg")->str:

	return archivo.rsplit(".", 1)[1].lower() if "." in archivo else extension_alternativa

def comprobarFechas(fecha_ida:str, fecha_vuelta:str, fecha_partido:str)->bool:

	try:

		datetime_partido=datetime.strptime(fecha_partido, "%Y-%m-%d")

		if datetime.strptime(fecha_ida, "%Y-%m-%d")<=datetime_partido and datetime.strptime(fecha_vuelta, "%Y-%m-%d")>=datetime_partido:

			return True

		else:

			return False

	except Exception:

		return False

def obtenerPrimerUltimoDiaAnoMes(ano_mes:str)->Optional[tuple]:

	try:

		ano_mes_datetime=datetime.strptime(ano_mes, "%Y-%m")

		mes=ano_mes_datetime.month

		ano=ano_mes_datetime.year

		primer_dia=datetime(ano, mes, 1)

		primer_dia_siguiente_mes=datetime(ano+1, 1, 1) if mes==12 else datetime(ano, mes+1, 1)

		ultimo_dia=primer_dia_siguiente_mes-timedelta(days=1)

		return primer_dia.strftime("%Y-%m-%d"), ultimo_dia.strftime("%Y-%m-%d")

	except Exception:

		return None

def mapearAnoMes(ano_mes:str)->Optional[str]:

	meses_espanol={"January":"Enero", "February":"Febrero", "March":"Marzo", "April":"Abril",
					"May":"Mayo", "June":"Junio", "July":"Julio", "August":"Agosto", "September":"Septiembre",
					"October":"Octubre", "November":"Noviembre", "December":"Diciembre"}

	try:

		fecha=datetime.strptime(ano_mes, "%Y-%m")

		mes_ingles=fecha.strftime("%B")
		   
		mes_espanol=meses_espanol[mes_ingles]
		
		return f"{mes_espanol} {fecha.year}"

	except Exception:

		return None

def obtenerAnoMesFechas(fecha_inicio:str, fecha_fin:str)->Optional[List[List[str]]]:

	try:

		inicio_datetime=datetime.strptime(fecha_inicio, "%Y-%m-%d").replace(day=1)

		fin_datetime=datetime.strptime(fecha_fin, "%Y-%m-%d").replace(day=1)

		anos_meses=[]

		while inicio_datetime<=fin_datetime:

			ano_mes=inicio_datetime.strftime("%Y-%m")

			anos_meses.append([ano_mes, mapearAnoMes(ano_mes)])

			if inicio_datetime.month==12:

				inicio_datetime=inicio_datetime.replace(year=inicio_datetime.year+1, month=1)

			else:

				inicio_datetime=inicio_datetime.replace(month=inicio_datetime.month+1)

		return sorted(anos_meses, reverse=True)

	except Exception:

		return None

def generarCalendario(fecha_inicio, fecha_fin)->List[Optional[List]]:

	try:

		fecha_inicio_datetime=datetime.strptime(fecha_inicio, "%Y-%m-%d")

		fecha_fin_datetime=datetime.strptime(fecha_fin, "%Y-%m-%d")
		
		fechas=[fecha_inicio_datetime+timedelta(days=dia) for dia in range((fecha_fin_datetime-fecha_inicio_datetime).days+1)]
		
		dia_inicio_semana=fecha_inicio_datetime.weekday()
		
		dias_vacios_inicio=[""]*dia_inicio_semana
		
		dia_fin_semana=fecha_fin_datetime.weekday()
		
		dias_vacios_fin=[""]*(6-dia_fin_semana)
		
		fechas_completas=dias_vacios_inicio+[fecha.strftime("%Y-%m-%d") for fecha in fechas]+dias_vacios_fin
		
		return [fechas_completas[dia:dia+7] for dia in range(0, len(fechas_completas), 7)]

	except Exception:

		return []

def cruzarPartidosCalendario(partidos:List[tuple], calendario:List[List])->List[List[tuple]]:

	try:

		partidos_dict={partido[3]:partido for partido in partidos}

		for fila in range(len(calendario)):

			for celda in range(len(calendario[fila])):

				fecha=calendario[fila][celda]

				if fecha:

					dia=datetime.strptime(fecha, "%Y-%m-%d").day

					calendario[fila][celda]=(fecha, dia, partidos_dict[fecha]) if fecha in partidos_dict else (fecha, dia, None)

		return calendario

	except Exception:

		return []

def ano_mes_anterior(ano_mes:str)->Optional[str]:

	try:

		ano_mes_dia=datetime.strptime(ano_mes, "%Y-%m").replace(day=15)

		ano_mes_dia_anterior=ano_mes_dia-timedelta(days=30)

		return ano_mes_dia_anterior.strftime("%Y-%m")

	except Exception:

		return None

def ano_mes_siguiente(ano_mes:str)->Optional[str]:

	try:

		ano_mes_dia=datetime.strptime(ano_mes, "%Y-%m").replace(day=15)

		ano_mes_dia_siguiente=ano_mes_dia+timedelta(days=30)

		return ano_mes_dia_siguiente.strftime("%Y-%m")

	except Exception:

		return None

def limpiarResultadosPartidosCalendario(partidos_calendario:List[tuple])->Dict:

	partidos_ganados=len(list(filter(lambda partido: partido[-4]==1, partidos_calendario)))

	partidos_perdidos=len(list(filter(lambda partido: partido[-3]==1, partidos_calendario)))

	partidos_empatados=len(list(filter(lambda partido: partido[-2]==1, partidos_calendario)))

	return {"ganados":partidos_ganados,
			"perdidos": partidos_perdidos,
			"empatados": partidos_empatados}

def datos_trayectos_correctos(codigo_ciudad_ida:bool, codigo_ciudad_vuelta:bool, ciudad_ida_estadio:str,
								ciudad_vuelta_estadio:str, ciudad_estadio_partido:str, transporte_ida:str, transporte_vuelta:str)->bool:

	ciudad_correcta=ciudad_ida_estadio==ciudad_vuelta_estadio==ciudad_estadio_partido

	transportes_correctos=transporte_ida in TRANSPORTES and transporte_vuelta in TRANSPORTES

	return True if codigo_ciudad_ida and codigo_ciudad_vuelta and ciudad_correcta and transportes_correctos else False

def obtenerCentroideCoordenadas(coordenadas:List[tuple])->tuple:

	latitudes=[latitud for latitud, longitud in coordenadas]

	longitudes = [longitud for latitud, longitud in coordenadas]

	try:

		return (sum(latitudes)/len(latitudes), sum(longitudes)/len(longitudes))

	except Exception:

		raise Exception("Error en obtener el centroide")

def crearMapaTrayecto(ruta:str, datos_trayecto:tuple, nombre_mapa:str, ida_vuelta:bool=False, zoom:float=5)->None:

	tipo, transporte=datos_trayecto[0], datos_trayecto[1]
	ciudad_origen, latitud_origen, longitud_origen=datos_trayecto[2], datos_trayecto[3], datos_trayecto[4]
	ciudad_destino, latitud_destino, longitud_destino=datos_trayecto[5], datos_trayecto[6], datos_trayecto[7]

	centroide=obtenerCentroideCoordenadas([(latitud_origen, longitud_origen), (latitud_destino, longitud_destino)])

	constantes_tipo_trayecto={"I":["ffcccc", "red", "inicio", "estadio_mapa"], "V":["95ebf7", "blue", "estadio_mapa", "inicio"], "IV":["ffdd73", "orange", "inicio", "estadio_mapa"]}

	try:

		tipo_trayecto=tipo if not ida_vuelta else "IV"

		constante_tipo_trayecto=constantes_tipo_trayecto[tipo_trayecto]

		mapa=folium.Map(location=[centroide[0], centroide[1]], zoom_start=zoom)

		popup_origen_html=f"""
					<div style="text-align: center;">
						<h4>
							{ciudad_origen}
						</h4>
					</div>
					"""

		icono_origen_html=f"""
						<div style="background-color: #{constante_tipo_trayecto[0]} ; width: 32px; height: 32px; border-radius: 50%; text-align: center; border: 1px solid {constante_tipo_trayecto[1]}; border-width: 1px;"">
							<img src="/static/imagenes/iconos/{constante_tipo_trayecto[2]}.png" style="width: 23px; height: 23px; margin-top: 4px;">
						</div>
						"""

		folium.Marker(location=[latitud_origen, longitud_origen],
						popup=folium.Popup(popup_origen_html, max_width=400),
						icon=folium.DivIcon(html=icono_origen_html)).add_to(mapa)

		popup_destino_html=f"""
					<div style="text-align: center;">
						<h4>
							{ciudad_destino}
						</h4>
					</div>
					"""

		icono_destino_html=f"""
						<div style="background-color: #{constante_tipo_trayecto[0]} ; width: 32px; height: 32px; border-radius: 50%; text-align: center; border: 1px solid {constante_tipo_trayecto[1]}; border-width: 1px;"">
							<img src="/static/imagenes/iconos/{constante_tipo_trayecto[3]}.png" style="width: 23px; height: 23px; margin-top: 4px;">
						</div>
						"""

		folium.Marker(location=[latitud_destino, longitud_destino],
						popup=folium.Popup(popup_destino_html, max_width=400),
						icon=folium.DivIcon(html=icono_destino_html)).add_to(mapa)

		folium.PolyLine(locations=[[latitud_origen, longitud_origen], [latitud_destino, longitud_destino]], color=constante_tipo_trayecto[1], weight=2.5, opacity=1).add_to(mapa)

		mapa.save(os.path.join(ruta, nombre_mapa))

	except Exception as e:

		raise Exception("Error al crear el mapa")

def crearMapaTrayectos(ruta:str, datos_trayectos:List[tuple], nombre_mapa:str, zoom:float=5)->None:

	coordenadas_trayectos=[par for datos_trayecto in datos_trayectos for par in [(datos_trayecto[3], datos_trayecto[4]), (datos_trayecto[6], datos_trayecto[7])]]

	centroide=obtenerCentroideCoordenadas(coordenadas_trayectos)

	try:

		mapa=folium.Map(location=[centroide[0], centroide[1]], zoom_start=zoom)

		constantes_tipo_trayecto={"I":["ffcccc", "red", "inicio", "estadio_mapa"], "V":["95ebf7", "blue", "estadio_mapa", "inicio"]}

		for datos_trayecto in datos_trayectos:

			tipo, transporte=datos_trayecto[0], datos_trayecto[1]
			ciudad_origen, latitud_origen, longitud_origen=datos_trayecto[2], datos_trayecto[3], datos_trayecto[4]
			ciudad_destino, latitud_destino, longitud_destino=datos_trayecto[5], datos_trayecto[6], datos_trayecto[7]

			constante_tipo_trayecto=constantes_tipo_trayecto[tipo]

			popup_origen_html=f"""
				<div style="text-align: center;">
					<h4>
						{ciudad_origen}
					</h4>
				</div>
				"""

			icono_origen_html=f"""
							<div style="background-color: #{constante_tipo_trayecto[0]} ; width: 32px; height: 32px; border-radius: 50%; text-align: center; border: 1px solid {constante_tipo_trayecto[1]}; border-width: 1px;"">
								<img src="/static/imagenes/iconos/{constante_tipo_trayecto[2]}.png" style="width: 23px; height: 23px; margin-top: 4px;">
							</div>
							"""

			folium.Marker(location=[latitud_origen, longitud_origen],
							popup=folium.Popup(popup_origen_html, max_width=400),
							icon=folium.DivIcon(html=icono_origen_html)).add_to(mapa)

			popup_destino_html=f"""
						<div style="text-align: center;">
							<h4>
								{ciudad_destino}
							</h4>
						</div>
						"""

			icono_destino_html=f"""
							<div style="background-color: #{constante_tipo_trayecto[0]} ; width: 32px; height: 32px; border-radius: 50%; text-align: center; border: 1px solid {constante_tipo_trayecto[1]}; border-width: 1px;"">
								<img src="/static/imagenes/iconos/{constante_tipo_trayecto[3]}.png" style="width: 23px; height: 23px; margin-top: 4px;">
							</div>
							"""

			folium.Marker(location=[latitud_destino, longitud_destino],
							popup=folium.Popup(popup_destino_html, max_width=400),
							icon=folium.DivIcon(html=icono_destino_html)).add_to(mapa)

			folium.PolyLine(locations=[[latitud_origen, longitud_origen], [latitud_destino, longitud_destino]], color=constante_tipo_trayecto[1], weight=2.5, opacity=1).add_to(mapa)

		mapa.save(os.path.join(ruta, nombre_mapa))

	except Exception as e:

		raise Exception("Error al crear el mapa")

def crearMapaTrayectosIdaVuelta(ruta:str, datos_trayectos:List[tuple], nombre_mapa:str, zoom:float=5)->None:

	coordenadas_trayectos=[par for datos_trayecto in datos_trayectos for par in [(datos_trayecto[3], datos_trayecto[4]), (datos_trayecto[6], datos_trayecto[7])]]

	ida_vuelta_igual=True if len(set(coordenadas_trayectos))<len(coordenadas_trayectos)-1 else False

	if ida_vuelta_igual:

		crearMapaTrayecto(ruta, datos_trayectos[0], nombre_mapa, True)

	else:

		crearMapaTrayectos(ruta, datos_trayectos, nombre_mapa)