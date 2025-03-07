import time
from typing import Optional
from confluent_kafka import Consumer

from src.kafka.kafka_utils import kafka_consumer, crearTopic, subscribirseTOPIC, consumirMensajes, escribirLogKafka
from src.kafka.configkafka import TOPIC

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

        time.sleep(1)

        if not mensaje:

            continue

        else:

            print(f"Mensaje: {mensaje}")
            escribirLogKafka(f"Mensaje recibido: {mensaje}")

if __name__ == "__main__":

    ejecutarConsumer()