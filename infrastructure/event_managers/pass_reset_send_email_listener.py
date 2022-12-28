import json
import logging
from logging.config import dictConfig
from infrastructure.notify_managers.send_email import SendEmail
from infrastructure.logging import LogConfig
from infrastructure.event_managers.rabbit_consumer import RabbitConsumer

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class PassResetSendEmailListener(RabbitConsumer):
    topic = "password_updated_send_email"

    def process_message(self, channel, method, properties, body):
        logger.info('Received message')
        event = json.loads(body)
        mail = SendEmail()
        mail.send_email(user_email=event["email"], subject=event["subject"], body=mail.get_password_updated_mail(event["username"]))
        logger.info('Message consumed')
