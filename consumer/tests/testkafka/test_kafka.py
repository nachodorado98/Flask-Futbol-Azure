import pytest
import time
import json
from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer, Producer
from src.kafka.kafka_utils import kafka_admin, crearTopic, kafka_consumer, subscribirseTOPIC, consumirMensajes
from src.kafka.configkafka import SERVIDOR

def test_kafka_admin_error():

	assert not kafka_admin("host_error:9092")

def test_kafka_admin():

	assert isinstance(kafka_admin(), AdminClient)

def borrar_todos_topics():

	admin=kafka_admin()

	topics=admin.list_topics().topics

	for topic in topics:

		time.sleep(1)

		admin.delete_topics(topics=[topic])

@pytest.mark.parametrize(["topic"],
	[("hola",), ("topic1",), ("topic_prueba",)]
)
def test_topic_no_existe(topic):

	borrar_todos_topics()

	admin=kafka_admin()

	assert topic not in admin.list_topics().topics

@pytest.mark.parametrize(["topic"],
	[("hola1",), ("topic2",), ("topic_prueba1",)]
)
def test_topic_existe(topic):

	admin=kafka_admin()

	assert topic not in admin.list_topics().topics

	crearTopic(topic)

	time.sleep(1)

	assert topic in admin.list_topics().topics

def test_kafka_consumer_error():

	assert not kafka_consumer(servidor_kafka="host_error:9092")

def test_kafka_comsumer():

	assert isinstance(kafka_consumer(), Consumer)

def test_subscribirse_topic_consumer_error():

	assert not subscribirseTOPIC("consumer", "topic")

def test_subscribirse_topic_topic_no_existe():

	consumer=kafka_consumer()

	assert not subscribirseTOPIC(consumer, "topic")

	consumer.close()

def test_subscribirse_topic():

	consumer=kafka_consumer()

	assert isinstance(subscribirseTOPIC(consumer, "hola1"), Consumer)

	consumer.close()

def test_consumir_mensajes_consume_error():

	assert not consumirMensajes("consumer")

def test_consumir_mensajes_no_mensajes():

	consumer=kafka_consumer()

	consumer=subscribirseTOPIC(consumer, "hola1")

	assert not consumirMensajes(consumer)

	consumer.close()

def test_consumir_mensajes_mensajes_otro_topic():

	producer=Producer({"bootstrap.servers": SERVIDOR})

	consumer=kafka_consumer()

	consumer=subscribirseTOPIC(consumer, "hola1")

	producer.produce("hola2", key="test", value="valor")

	producer.flush()

	time.sleep(2)

	assert not consumirMensajes(consumer)

	consumer.close()

def test_consumir_mensajes_error():

	producer=Producer({"bootstrap.servers": SERVIDOR})

	consumer=kafka_consumer(grupo_id="grupo1", inicio=True)

	consumer=subscribirseTOPIC(consumer, "hola1")

	producer.produce("hola1", value=b"\x80\x81\x82\x83")

	producer.flush()

	time.sleep(2)

	assert not consumirMensajes(consumer)

	consumer.close()

def test_consumir_mensajes():

	producer=Producer({"bootstrap.servers": SERVIDOR})

	consumer=kafka_consumer(grupo_id="grupo2", inicio=True)

	consumer=subscribirseTOPIC(consumer, "topic2")

	producer.produce("topic2", value="valor")

	producer.flush()

	time.sleep(2)

	mensaje=consumirMensajes(consumer)

	assert mensaje=="valor"

	consumer.close()