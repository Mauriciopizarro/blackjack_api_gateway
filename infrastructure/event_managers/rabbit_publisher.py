import json
import pika
import uuid
from logging.config import dictConfig
import logging
from domain.interfaces.publisher import Publisher
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class RabbitConnection:

    instance = None

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq", heartbeat=600, blocked_connection_timeout=300)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="password_updated_send_email")
        logger.warning('Rabbit connection initialized')

    @classmethod
    def get_channel(cls):
        instance = cls.init_connection()
        return instance.channel

    @classmethod
    def get_connection(cls):
        instance = cls.init_connection()
        return instance.connection

    @classmethod
    def init_connection(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance


class RabbitPublisher(Publisher):

    def send_message(self, message: dict, topic: str):
        """Method to publish message to RabbitMQ"""
        publish_queue_name = topic
        channel = RabbitConnection.get_channel()
        connection = RabbitConnection.get_connection()
        channel.basic_publish(
            exchange='',
            routing_key=publish_queue_name,
            properties=pika.BasicProperties(
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )
        logger.info('Message published')
