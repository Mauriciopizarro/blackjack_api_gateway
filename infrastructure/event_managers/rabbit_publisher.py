import json
import pika
import uuid
from domain.interfaces.publisher import Publisher
from infrastructure.event_managers.rabbit_conection import RabbitConnection
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class RabbitPublisher(Publisher):

    def send_message(self, message: dict, topic: str):
        """Method to publish message to RabbitMQ"""
        publish_queue_name = topic
        channel = RabbitConnection.get_channel()
        channel.basic_publish(
            exchange='',
            routing_key=publish_queue_name,
            properties=pika.BasicProperties(
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )
        logger.info(f'Message published in topic {topic}')
