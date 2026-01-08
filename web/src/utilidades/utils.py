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
from geopy.distance import geodesic
import math
from collections import Counter

from src.database.conexion import Conexion

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

def ciudad_estadio_correcta(ciudad_ida_estadio:str, ciudad_vuelta_estadio:str, ciudad_estadio:str):

	return ciudad_ida_estadio==ciudad_vuelta_estadio==ciudad_estadio

def trayecto_correcto(codigo_ciudad_origen:int, codigo_ciudad_destino:int, transporte:str, entorno:str):

	if not codigo_ciudad_origen or not codigo_ciudad_destino or transporte not in TRANSPORTES:

		return False

	con=Conexion(entorno)

	coordenadas_origen=con.obtenerCoordenadasCiudad(codigo_ciudad_origen)

	coordenadas_destino=con.obtenerCoordenadasCiudad(codigo_ciudad_destino)

	con.cerrarConexion()

	distancia_coordenadas=distancia_maxima_coordenadas([coordenadas_origen, coordenadas_destino])

	if distancia_coordenadas<20:

		transportes_validos=["Autobus Urbano", "Autobus Interurbano", "Coche", "Metro", "Cercanias", "Pie"]

	elif distancia_coordenadas<150:

		transportes_validos=["Tren", "Autobus", "Autobus Interurbano", "Coche", "Cercanias"]

	elif distancia_coordenadas<300:

		transportes_validos=["Avion", "Tren", "Autobus", "Coche", "Cercanias"]

	elif distancia_coordenadas<1000:

		transportes_validos=["Avion", "Tren", "Autobus", "Coche"]

	elif distancia_coordenadas<1500:

		transportes_validos=["Avion", "Autobus"]

	else:
		transportes_validos=["Avion"]

	return transporte in transportes_validos

def obtenerCentroideCoordenadas(coordenadas:List[tuple])->tuple:

	latitudes=[latitud for latitud, longitud in coordenadas]

	longitudes = [longitud for latitud, longitud in coordenadas]

	try:

		return (sum(latitudes)/len(latitudes), sum(longitudes)/len(longitudes))

	except Exception:

		raise Exception("Error en obtener el centroide")

def obtenerAngulo(coordenadas:List[tuple])->float:

	if len(coordenadas)!=2:
		return 0

	(lat_origen, lon_origen), (lat_destino, lon_destino)=coordenadas

	lat1_rad=math.radians(lat_origen)
	lon1_rad=math.radians(lon_origen)
	lat2_rad=math.radians(lat_destino)
	lon2_rad=math.radians(lon_destino)
 
	y=math.sin(lon2_rad-lon1_rad)*math.cos(lat2_rad)
	x=math.cos(lat1_rad)*math.sin(lat2_rad)-math.sin(lat1_rad)*math.cos(lat2_rad)*math.cos(lon2_rad-lon1_rad)
 
	angulo_rad=math.atan2(y, x)
	angulo_deg=math.degrees(angulo_rad)
 
	return (angulo_deg-90)%360

def crearMapaTrayecto(ruta:str, datos_trayecto:tuple, nombre_mapa:str, ida_vuelta:bool=False, zoom:float=5)->None:

	tipo, transporte=datos_trayecto[0], datos_trayecto[1]
	ciudad_origen, latitud_origen, longitud_origen=datos_trayecto[2], datos_trayecto[3], datos_trayecto[4]
	ciudad_destino, latitud_destino, longitud_destino=datos_trayecto[5], datos_trayecto[6], datos_trayecto[7]
	imagen_origen, imagen_destino=datos_trayecto[8], datos_trayecto[9]

	centroide=obtenerCentroideCoordenadas([(latitud_origen, longitud_origen), (latitud_destino, longitud_destino)])

	constantes_tipo_trayecto={"I":["ffcccc", "red", "inicio", "estadio_mapa", "/static/imagenes/iconos/", URL_DATALAKE_ESTADIOS, "50", "200"],
								"V":["95ebf7", "blue", "estadio_mapa", "inicio", URL_DATALAKE_ESTADIOS, "/static/imagenes/iconos/", "200", "50"],
								"IV":["ffdd73", "orange", "inicio", "estadio_mapa", "/static/imagenes/iconos/", URL_DATALAKE_ESTADIOS, "50", "200"]}

	try:

		zoom=calcularZoomMapa([(latitud_origen, longitud_origen), (latitud_destino, longitud_destino)])

		tipo_trayecto=tipo if not ida_vuelta else "IV"

		constante_tipo_trayecto=constantes_tipo_trayecto[tipo_trayecto]

		mapa=folium.Map(location=[centroide[0], centroide[1]], zoom_start=zoom)

		popup_origen_html=f"""
							<div style="text-align: center;">
								<h4>{ciudad_origen}</h4>
								<img src="{constante_tipo_trayecto[4]}{imagen_origen}.png" alt="Estadio_Transporte_{tipo_trayecto}" style="width:{constante_tipo_trayecto[6]}px;">
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
								<h4>{ciudad_destino}</h4>
								<img src="{constante_tipo_trayecto[5]}{imagen_destino}.png" alt="Estadio_Transporte_{tipo_trayecto}" style="width:{constante_tipo_trayecto[7]}px;">
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

		angulo=obtenerAngulo([(latitud_origen, longitud_origen), (latitud_destino, longitud_destino)])

		folium.RegularPolygonMarker(location=(centroide[0], centroide[1]),
									fill_color=constante_tipo_trayecto[1],
									color=constante_tipo_trayecto[1],
									fill_opacity=1,
									number_of_sides=3,
									radius=10,
									rotation=angulo).add_to(mapa)
		
		mapa.save(os.path.join(ruta, nombre_mapa))

	except Exception as e:

		raise Exception("Error al crear el mapa")

def crearMapaTrayectos(ruta:str, datos_trayectos:List[tuple], nombre_mapa:str)->None:

	coordenadas_trayectos=[par for datos_trayecto in datos_trayectos for par in [(datos_trayecto[3], datos_trayecto[4]), (datos_trayecto[6], datos_trayecto[7])]]

	centroide=obtenerCentroideCoordenadas(coordenadas_trayectos)

	try:

		zoom=calcularZoomMapa(coordenadas_trayectos)

		mapa=folium.Map(location=[centroide[0], centroide[1]], zoom_start=zoom)

		constantes_tipo_trayecto={"I":["ffcccc", "red", "inicio", "estadio_mapa", "/static/imagenes/iconos/", URL_DATALAKE_ESTADIOS, "50", "200"],
									"V":["95ebf7", "blue", "estadio_mapa", "inicio", URL_DATALAKE_ESTADIOS, "/static/imagenes/iconos/", "200", "50"]}

		for datos_trayecto in datos_trayectos:

			tipo, transporte=datos_trayecto[0], datos_trayecto[1]
			ciudad_origen, latitud_origen, longitud_origen=datos_trayecto[2], datos_trayecto[3], datos_trayecto[4]
			ciudad_destino, latitud_destino, longitud_destino=datos_trayecto[5], datos_trayecto[6], datos_trayecto[7]
			imagen_origen, imagen_destino=datos_trayecto[8], datos_trayecto[9]

			constante_tipo_trayecto=constantes_tipo_trayecto[tipo]

			popup_origen_html=f"""
								<div style="text-align: center;">
									<h4>{ciudad_origen}</h4>
									<img src="{constante_tipo_trayecto[4]}{imagen_origen}.png" alt="Estadio_Transporte_{tipo}" style="width:{constante_tipo_trayecto[6]}px;">
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
									<h4>{ciudad_destino}</h4>
									<img src="{constante_tipo_trayecto[5]}{imagen_destino}.png" alt="Estadio_Transporte_{tipo}" style="width:{constante_tipo_trayecto[7]}px;">
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

			angulo=obtenerAngulo([(latitud_origen, longitud_origen), (latitud_destino, longitud_destino)])

			centroide_trayecto_simple=obtenerCentroideCoordenadas([(latitud_origen, longitud_origen), (latitud_destino, longitud_destino)])

			folium.RegularPolygonMarker(location=(centroide_trayecto_simple[0], centroide_trayecto_simple[1]),
										fill_color=constante_tipo_trayecto[1],
										color=constante_tipo_trayecto[1],
										fill_opacity=1,
										number_of_sides=3,
										radius=10,
										rotation=angulo).add_to(mapa)

		mapa.save(os.path.join(ruta, nombre_mapa))

	except Exception as e:

		raise Exception("Error al crear el mapa")

def crearMapaTrayectosIdaVuelta(ruta:str, datos_trayectos:List[tuple], nombre_mapa:str)->None:

	coordenadas_trayectos=[par for datos_trayecto in datos_trayectos for par in [(datos_trayecto[3], datos_trayecto[4]), (datos_trayecto[6], datos_trayecto[7])]]

	ida_vuelta_igual=True if len(set(coordenadas_trayectos))<len(coordenadas_trayectos)-1 else False

	if ida_vuelta_igual:

		crearMapaTrayecto(ruta, datos_trayectos[0], nombre_mapa, True)

	else:

		crearMapaTrayectos(ruta, datos_trayectos, nombre_mapa)

def distancia_maxima_coordenadas(coordenadas:List[tuple])->int:
	
	if len(coordenadas)<2:
		return 0 

	max_distancia=0

	for numero in range(len(coordenadas)):

		for numero_siguiente in range(numero+1, len(coordenadas)):

			distancia=geodesic(coordenadas[numero], coordenadas[numero_siguiente]).kilometers

			max_distancia=max(max_distancia, distancia)

	return max_distancia

def calcularZoomMapa(coordenadas:List[tuple], C:int=15)->int:

	if len(coordenadas)<2:
		return 15

	max_distancia=distancia_maxima_coordenadas(coordenadas)

	zoom=C-math.log2(max_distancia+1)

	return round(max(1, min(zoom, 18)))

def obtenerNombreDivisionSeleccionado(divisiones:List[tuple], codigo_division:str)->Optional[str]:
 
	try:
 
		return list(filter(lambda division: division[1]==codigo_division, divisiones))[0][0]
 
	except Exception:
 
		return None

def obtenerDivisionesNoSeleccionados(divisiones:List[tuple], codigo_division:str)->List[tuple]:
 
	divisiones_no_seleccionados=list(filter(lambda division: division[1]!=codigo_division, divisiones))
 
	return [(division[0], division[1], division[3]) for division in divisiones_no_seleccionados]

def existen_paradas(transportes:List[Optional[str]], paises:List[Optional[str]], ciudades:List[Optional[str]])->bool:

	return True if transportes or paises or ciudades else False

def obtenerParadas(transportes:List[Optional[str]], paises:List[Optional[str]], ciudades:List[Optional[str]])->List[Optional[tuple]]:

	if not (len(transportes)==len(paises)==len(ciudades)):
		return []

	return [(t.strip(), p.strip(), c.strip()) for t, p, c in zip(transportes, paises, ciudades) if t and p and c and t.strip() and p.strip() and c.strip()]

def obtenerCombinacionesParadas(paradas:List[tuple])->List[tuple]:

	return [(ciudad1, pais1, ciudad2, pais2, transporte2) for (transporte1, pais1, ciudad1), (transporte2, pais2, ciudad2) in zip(paradas, paradas[1:])]

def obtenerDataframeTrayecto(df:pd.DataFrame, partido_id:str, usuario_id:str, tipo:str, entorno:str, numero:bool=False)->pd.DataFrame:

	df_base=df.copy()

	con=Conexion(entorno)

	tupla_columnas=[["Ciudad_Origen", "Pais_Origen", "Codigo_Ciudad_Origen"], ["Ciudad_Destino", "Pais_Destino", "Codigo_Ciudad_Destino"]]

	for columna in tupla_columnas:

		df_base[columna[2]]=df[[columna[0], columna[1]]].apply(lambda fila: con.obtenerCodigoCiudadPais(fila[columna[0]], fila[columna[1]]), axis=1)

	con.cerrarConexion()

	df_base=df_base[["Ciudad_Origen", "Pais_Origen", "Codigo_Ciudad_Origen", "Ciudad_Destino", "Pais_Destino", "Codigo_Ciudad_Destino", "Transporte"]]

	df_base["Correcto"]=df_base[["Codigo_Ciudad_Origen", "Codigo_Ciudad_Destino", "Transporte"]].apply(lambda fila: trayecto_correcto(fila["Codigo_Ciudad_Origen"], fila["Codigo_Ciudad_Destino"], fila["Transporte"], entorno), axis=1)

	df_base["Partido_Id"]=partido_id

	df_base["Usuario_Id"]=usuario_id

	df_base["Tipo"]=tipo

	if numero:

		df_base["Trayecto_Id"]="id_"+df_base["Partido_Id"].astype(str)+"_"+df_base["Usuario_Id"].astype(str)+"_"+df_base["Tipo"]+"_"+(df_base.index+1).astype(str)

	else:

		df_base["Trayecto_Id"]="id_"+df_base["Partido_Id"].astype(str)+"_"+df_base["Usuario_Id"].astype(str)+"_"+df_base["Tipo"]+"_0"

	return df_base[["Trayecto_Id", "Partido_Id", "Usuario_Id", "Tipo", "Codigo_Ciudad_Origen", "Transporte", "Codigo_Ciudad_Destino", "Correcto"]]

def obtenerDataframeConParadas(df:pd.DataFrame, paradas:List[tuple], ciudad_final:str, pais_final:str, transporte_final:str)->pd.DataFrame:

	try:

		df_sin_paradas=df.copy()

		df_sin_paradas[["Ciudad_Destino", "Pais_Destino", "Transporte"]]=[paradas[0][2], paradas[0][1], paradas[0][0]]

		combinaciones_paradas=obtenerCombinacionesParadas(paradas)

		for parada in combinaciones_paradas:

			df_sin_paradas.loc[len(df_sin_paradas)]=parada

		df_sin_paradas.loc[len(df_sin_paradas)]=[paradas[-1][2], paradas[-1][1], ciudad_final, pais_final, transporte_final]

		return df_sin_paradas

	except IndexError:

		raise Exception("Error, no hay paradas")

def obtenerDataframeDireccion(ciudad_origen:str, pais_origen:str, ciudad_destino:str, pais_destino:str, transporte:str, partido_id:str, usuario_id:str, tipo:str, entorno:str)->pd.DataFrame:

	if tipo not in ["I", "V"]:

		raise Exception("El tipo no es valido")

	columnas=("Ciudad_Origen", "Pais_Origen", "Ciudad_Destino", "Pais_Destino", "Transporte")

	df=pd.DataFrame([(ciudad_origen, pais_origen, ciudad_destino, pais_destino, transporte)], columns=columnas)

	df_final=obtenerDataframeTrayecto(df, partido_id, usuario_id, tipo, entorno)

	return df_final

def obtenerDataframeDireccionParadas(ciudad_origen:str, pais_origen:str, ciudad_destino:str, pais_destino:str, transporte:str, paradas:List[tuple], partido_id:str, usuario_id:str, tipo:str, entorno:str)->pd.DataFrame:

	if tipo not in ["I", "V"]:

		raise Exception("El tipo no es valido")

	df=pd.DataFrame([(ciudad_origen, pais_origen)], columns=["Ciudad_Origen", "Pais_Origen"])

	df_paradas=obtenerDataframeConParadas(df, paradas, ciudad_destino, pais_destino, transporte)

	df_final=obtenerDataframeTrayecto(df_paradas, partido_id, usuario_id, tipo, entorno, True)

	return df_final

def validarDataFramesTrayectosCorrectos(df_ida:pd.DataFrame, df_vuelta:pd.DataFrame)->bool:

	df_ida_copia=df_ida.copy()
	df_vuelta_copia=df_vuelta.copy()

	if df_ida_copia.empty or df_vuelta_copia.empty:
		return False

	if (~df_ida_copia["Correcto"]).any() or (~df_vuelta_copia["Correcto"]).any():
		return False

	return True

def validarDataFrameDuplicados(df:pd.DataFrame)->bool:

	df_copia=df.copy()

	if df_copia.empty:
		return False

	if df["Codigo_Ciudad_Origen"].duplicated().any() or df["Codigo_Ciudad_Destino"].duplicated().any():
		return False

	return True

def obtenerTrayectosConDistancia(trayectos:List)->List:

	trayectos_distancias=list(map(lambda trayecto: round(distancia_maxima_coordenadas([trayecto[5:7], trayecto[9:11]]), 2), trayectos))

	return [list(trayecto)+[distancia] for trayecto, distancia in zip(trayectos, trayectos_distancias)]

def obtenerDistanciaTotalTrayecto(trayectos:List)->int:

	return round(sum([trayecto[-1] for trayecto in trayectos]))

def es_numero(valor):

	try:

		float(valor)
		return True

	except (ValueError, TypeError):
		
		return False

def obtenerNumeroDias(fecha_inicio:str, fecha_fin:str)->int:

	try:

		fecha_inicio_datetime=datetime.strptime(fecha_inicio, "%d-%m-%Y")

		fecha_fin_datetime=datetime.strptime(fecha_fin, "%d-%m-%Y")

		return 0 if fecha_inicio_datetime>fecha_fin_datetime else (fecha_fin_datetime-fecha_inicio_datetime).days+1

	except:

		raise Exception("Error en la obtencion de los dias")

def anadirDiaActualCalendario(calendario:List[List[tuple]], dia:str)->List[List[tuple]]:

	semanas_actualizadas=[[d+(True,) if isinstance(d, tuple) and len(d)>=3 and d[0]==dia
							else d+(False,) if isinstance(d, tuple) and len(d)>=3
							else d
							for d in semana]
						for semana in calendario]

	return semanas_actualizadas

def validarNumeroGoles(goles:int)->bool:

	try:

		return 0<=goles<=9

	except Exception:

		return False

def validarGoleadores(goleadores:List[str], entorno:str)->bool:

	con=Conexion(entorno)

	for goleador in goleadores:

		if not con.existe_jugador(goleador):

			con.cerrarConexion()

			return False

	con.cerrarConexion()

	return True

def validarGolesGoleadores(goles_local:int, goles_visitante:int, goleadores_local:List[str], goleadores_visitante:List[str], entorno:str)->bool:

	if not all(map(validarNumeroGoles, [goles_local, goles_visitante])):

		return False

	if len(goleadores_local)!=goles_local or len(goleadores_visitante)!=goles_visitante:

		return False

	if not all(map(lambda goleadores: validarGoleadores(goleadores, entorno), [goleadores_local, goleadores_visitante])):

		return False

	return True

def goleadoresLimpios(goleadores:List[str], local:bool)->List[tuple]:

	goleadores_contados=Counter(goleadores)

	return [(goleador, goleadores_contados[goleador], local) for goleador in dict.fromkeys(goleadores)]

def estadiosVisitadosWrappedLimpio(partidos_asistidos:List[Optional[tuple]])->List[Optional[tuple]]:

	return sorted(list(set([(partido[12], partido[13], partido[14], partido[15]) for partido in partidos_asistidos])))

def equiposVistosWrappedLimpio(partidos_asistidos:List[Optional[tuple]], equipo:str)->List[Optional[tuple]]:

	equipos_vistos=[(partido[8], partido[4], partido[6], partido[11]) if partido[8]!=equipo else (partido[9], partido[5], partido[7], partido[12]) for partido in partidos_asistidos]

	equipos_vistos_contados=Counter(equipos_vistos)

	return sorted([(equipo_visto[0], equipo_visto[1], equipo_visto[2], equipo_visto[3], veces) for equipo_visto, veces in equipos_vistos_contados.items()], key=lambda x: (-x[4], x[2]))

def obtenerGolesResultado(resultado:str)->tuple:

	goles=resultado.split("-")

	goles_local=goles[0].split("(")[0].strip()

	try:

		goles_visitante=goles[1].split(")")[1].strip()

	except Exception:

		goles_visitante=goles[1].strip()

	return int(goles_local), int(goles_visitante)

def partidoMasGolesWrapped(partidos_asistidos:List[Optional[tuple]])->Optional[tuple]:

	resultados=[(partido[0], obtenerGolesResultado(partido[1])) for partido in partidos_asistidos]

	if not resultados:

		return None

	mas_goles=max(resultados, key=lambda goles: sum(goles[1]))

	return list(filter(lambda partido: mas_goles[0]==partido[0], partidos_asistidos))[0]

def partidosMesWrapped(partidos_asistidos:List[Optional[tuple]])->List[Optional[tuple]]:

	meses=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
			"Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

	conteo=[0]*12

	partidos_mes={mes:[] for mes in meses}

	for partido in partidos_asistidos:

	    _,mes,_=partido[2].split('/')

	    conteo[int(mes)-1]+=1

	    partidos_mes[meses[int(mes)-1]].append(partido)

	return {"meses":meses, "num_partidos":conteo, "partidos":partidos_mes}