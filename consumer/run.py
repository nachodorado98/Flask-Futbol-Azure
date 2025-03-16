import time
from typing import Optional
from confluent_kafka import Consumer

from src.kafka.kafka_utils import kafka_consumer, crearTopic, subscribirseTOPIC, consumirMensajes, escribirLogKafka
from src.kafka.configkafka import TOPIC

from src.datalake.conexion_data_lake import ConexionDataLake

from src.utilidades.utils import obtenerClave, obtenerCorreoUsuarioNombre, correo_enviado, crearCarpetaDataLakeUsuario, crearCarpetaDataLakeUsuarios

def conectarKafka(max_intentos:int=5)->Optional[Consumer]:

    intento=1

    escribirLogKafka("Intentando conectar con Kafka...")

    while intento<max_intentos+1:

        escribirLogKafka(f"Intento numero {intento}")

        consumer=kafka_consumer()

        if not consumer:

            intento+=1

            time.sleep(5)

            continue

        escribirLogKafka("Consumer conectado a Kafka")

        return consumer

    raise Exception("Error, imposible conectar")

def realizarFuncionalidadCorreo(mensaje:str)->None:

    datos_correo=obtenerCorreoUsuarioNombre(mensaje)

    if datos_correo:

        correo_correcto=correo_enviado(datos_correo[0], datos_correo[2])

        if correo_correcto:

            escribirLogKafka(f"Correo del usuario {datos_correo[1]} enviado a la direccion: {datos_correo[0]}")

        else:

            escribirLogKafka(f"Correo del usuario {datos_correo[1]} NO enviado a la direccion: {datos_correo[0]}")

    else:

            escribirLogKafka("Correo NO enviado")

def realizarFuncionalidadDataLakeUsuario(mensaje:str)->None:

    usuario=obtenerClave(mensaje, "usuario")

    if usuario:

        if crearCarpetaDataLakeUsuario():

            escribirLogKafka("Carpeta usuarios creada")

            if crearCarpetaDataLakeUsuarios(usuario):

                escribirLogKafka(f"Carpeta del usuario {usuario} creada correctamente en el DataLake")

            else:

                escribirLogKafka(f"Carpeta del usuario {usuario} NO creada correctamente en el DataLake")

        else:

            escribirLogKafka("Carpeta usuarios NO creada")

def ejecutarConsumer()->None:

    consumer=conectarKafka()

    crearTopic(TOPIC)

    escribirLogKafka(f"Topic {TOPIC} creado")

    consumer=subscribirseTOPIC(consumer, TOPIC)

    escribirLogKafka(f"Suscrito al topic {TOPIC}")

    print(f"Escuchando del topic {TOPIC}...")

    escribirLogKafka(f"Escuchando del topic {TOPIC}...")

    while True:

        mensaje=consumirMensajes(consumer)

        if mensaje:

            categoria=obtenerClave(mensaje, "categoria")

            if categoria=="correo":

                realizarFuncionalidadCorreo(mensaje)                

            elif categoria=="datalake_usuario":

                realizarFuncionalidadDataLakeUsuario(mensaje)

            else:

                escribirLogKafka(f"Mensaje erroneo: {mensaje}")

if __name__ == "__main__":

    ejecutarConsumer()