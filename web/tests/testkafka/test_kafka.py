import pytest
import time
from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer

from src.kafka.kafka_utils import kafka_admin, crearTopic, kafka_producer, enviarMensajeKafka

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

def test_kafka_producer_error():

	assert not kafka_producer("host_error:9092")

def test_kafka_producer():

	assert isinstance(kafka_producer(), Producer)

@pytest.mark.parametrize(["topic"],
	[("hola",), ("topic1",), ("topic_prueba",)]
)
def test_enviar_mensaje_no_existe_topic(topic):

	assert not enviarMensajeKafka(topic, {"mensaje":"hola"})

@pytest.mark.parametrize(["topic"],
	[("hola1",), ("topic2",), ("topic_prueba1",)]
)
def test_enviar_mensaje(topic):

	admin=kafka_admin()

	assert topic in admin.list_topics().topics

	assert enviarMensajeKafka(topic, {"mensaje":"hola"})

	admin.delete_topics(topics=[topic])