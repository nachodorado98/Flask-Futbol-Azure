from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
import json

from .configkafka import SERVIDOR

def crearTopic(topic:str)->None:

	admin=AdminClient({"bootstrap.servers":SERVIDOR})

	if topic not in admin.list_topics().topics:

		print(f"Creando topic {topic}...")

		objeto_topic=NewTopic(topic=topic, num_partitions=3, replication_factor=1)

		admin.create_topics([objeto_topic])

		crearTopic(topic)

	else:

		print(f"Topic {topic} creado")

def enviarMensajeKafka(topic:str, mensaje:dict, servidor_kafka:str=SERVIDOR)->bool:

	admin=AdminClient({"bootstrap.servers":servidor_kafka})

	if topic not in admin.list_topics().topics:

		return False

	try:

		producer=Producer({"bootstrap.servers":servidor_kafka})

		producer.produce(topic, json.dumps(mensaje).encode("utf-8"))

		producer.flush()
		
		return True

	except Exception:

		return False