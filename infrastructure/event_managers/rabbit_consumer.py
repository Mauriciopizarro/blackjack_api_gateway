from abc import abstractmethod
import pika
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class RabbitConsumer:

    topic = None

    def __init__(self):
        """Setup message listener with the current running loop"""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq", heartbeat=600, blocked_connection_timeout=300)
        )
        self.channel = self.connection.channel()
        self.channel.basic_consume(queue=self.topic, on_message_callback=self.process_message, auto_ack=True)
        logger.info('Established async listener')

    @abstractmethod
    def process_message(self, channel, method, properties, body):
        pass

    def start_consuming(self):
        self.channel.start_consuming()
