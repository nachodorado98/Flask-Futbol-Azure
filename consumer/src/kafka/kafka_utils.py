from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer, KafkaError
from typing import Optional, Dict
import time

from .configkafka import SERVIDOR

def escribirLogKafka(mensaje: str)->None:

    with open("consumer_log_kafka.txt", "a") as f:

        f.write(f"{time.ctime()} - {mensaje}\n")

def kafka_admin(servidor_kafka:str=SERVIDOR)->Optional[AdminClient]:

    try:

        admin=AdminClient({"bootstrap.servers":servidor_kafka})

        admin.list_topics(timeout=5)

        return admin

    except Exception as e:

        print(f"Error conectando a Kafka: {e}")

        return

def crearTopic(topic:str, servidor_kafka:str=SERVIDOR)->None:

    admin=kafka_admin(servidor_kafka)

    if topic not in admin.list_topics().topics:

        print(f"Creando topic {topic}...")

        objeto_topic=NewTopic(topic=topic, num_partitions=3, replication_factor=1)

        admin.create_topics([objeto_topic])

        crearTopic(topic)

    else:

        print(f"Topic {topic} creado")

def kafka_consumer(grupo_id:str="grupo-consumidores", inicio:bool=False, servidor_kafka:str=SERVIDOR)->Optional[Consumer]:

    try:

        config={"bootstrap.servers":servidor_kafka, "group.id": grupo_id}

        if inicio:

            config["auto.offset.reset"]="earliest"

        consumer=Consumer(config)

        consumer.list_topics(timeout=5)

        return consumer

    except Exception as e:

        print(f"Error conectando a Kafka: {e}")

        return

def subscribirseTOPIC(consumer:Consumer, topic:str, servidor_kafka:str=SERVIDOR)->Optional[Consumer]:

    try:

        admin=AdminClient({"bootstrap.servers":servidor_kafka})

        if topic not in admin.list_topics().topics:

            return

        consumer.subscribe([topic])

        return consumer

    except Exception:

        return

def consumirMensajes(consumer:Consumer)->Optional[Dict]:

    try:

        # Comando terminal para el Consumer
        # kafka-console-consumer --bootstrap-server localhost:9092 --topic TOPIC

        mensaje=consumer.poll(1.0)
                
        if not mensaje:

            return
        
        if mensaje.error():

            if mensaje.error().code()==KafkaError._PARTITION_EOF:

                return

            else:

                print("Error en Kafka")
                return

        consumer.commit()
        
        return mensaje.value().decode("utf-8")

    except Exception:

        return