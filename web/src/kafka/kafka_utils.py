from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
import json
from typing import Optional

from .configkafka import SERVIDOR

def kafka_admin(servidor_kafka:str=SERVIDOR)->Optional[AdminClient]:

	try:

		admin=AdminClient({"bootstrap.servers":servidor_kafka})

		admin.list_topics(timeout=5)

		return admin

	except Exception as e:

		print(f"Error conectando a Kafka: {e}")

		return None

def crearTopic(topic:str, servidor_kafka:str=SERVIDOR)->None:

	admin=kafka_admin(servidor_kafka)

	if topic not in admin.list_topics().topics:

		print(f"Creando topic {topic}...")

		objeto_topic=NewTopic(topic=topic, num_partitions=3, replication_factor=1)

		admin.create_topics([objeto_topic])

		crearTopic(topic)

	else:

		print(f"Topic {topic} creado")

def kafka_producer(servidor_kafka:str=SERVIDOR)->Optional[Producer]:

	try:

		producer=Producer({"bootstrap.servers":servidor_kafka})

		producer.list_topics(timeout=5)

		return producer

	except Exception as e:

		print(f"Error conectando a Kafka: {e}")

		return None

def enviarMensajeKafka(topic:str, mensaje:dict, servidor_kafka:str=SERVIDOR)->bool:

	admin=kafka_admin(servidor_kafka)

	if topic not in admin.list_topics().topics:

		return False

	try:

		producer=kafka_producer(servidor_kafka)

		producer.produce(topic, json.dumps(mensaje).encode("utf-8"))

		producer.flush()
		
		return True

	except Exception:

		return False