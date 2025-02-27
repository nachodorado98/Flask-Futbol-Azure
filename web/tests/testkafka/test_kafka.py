import pytest
import time

from src.kafka.kafka_utils import crearTopic, enviarMensajeKafka

@pytest.mark.parametrize(["topic"],
	[("hola",), ("topic1",), ("topic_prueba",)]
)
def test_topic_no_existe(admin, topic):

	assert topic not in admin.list_topics().topics

@pytest.mark.parametrize(["topic"],
	[("hola1",), ("topic2",), ("topic_prueba1",)]
)
def test_topic_existe(admin, topic):

	assert topic not in admin.list_topics().topics

	crearTopic(topic)

	time.sleep(1)

	assert topic in admin.list_topics().topics

@pytest.mark.parametrize(["topic"],
	[("hola",), ("topic1",), ("topic_prueba",)]
)
def test_enviar_mensaje_no_existe_topic(topic):

	assert not enviarMensajeKafka(topic, {"mensaje":"hola"})

@pytest.mark.parametrize(["topic"],
	[("hola1",), ("topic2",), ("topic_prueba1",)]
)
def test_enviar_mensaje(admin, topic):

	assert topic in admin.list_topics().topics

	assert enviarMensajeKafka(topic, {"mensaje":"hola"})

	admin.delete_topics(topics=[topic])