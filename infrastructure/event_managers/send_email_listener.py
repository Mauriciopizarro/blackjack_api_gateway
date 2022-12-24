import ssl
import json
import logging
import smtplib
from logging.config import dictConfig
from email.message import EmailMessage
from infrastructure.logging import LogConfig
from infrastructure.event_managers.rabbit_consumer import RabbitConsumer


dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class SendEmailListener(RabbitConsumer):

    topic = "password_updated_send_email"

    def process_message(self, channel, method, properties, body):
        logger.info('Received message')
        event = json.loads(body)
        self.send_email_pass_reset(user_email=event["email"], subject=event["subject"])
        logger.info('Message consumed')

    @staticmethod
    def send_email_pass_reset(user_email, subject):
        email_sender = "noreplyblackjackmauri@gmail.com"
        email_password = "sdmswaviqhajommx"

        body = """ 
        Your password has been updated, you can sign_up with your new credentials, thank you.
        """

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = user_email
        em["Subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, user_email, em.as_string())

