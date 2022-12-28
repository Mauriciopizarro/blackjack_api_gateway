import ssl
import smtplib
from email.message import EmailMessage
from domain.interfaces.notify_user import NotifyUser


class SendEmail(NotifyUser):

    def __init__(self):
        self.email_sender = "noreplyblackjackmauri@gmail.com"
        self.email_password = "sdmswaviqhajommx"

    def send_email(self, user_email, subject, body):
        mail = EmailMessage()
        mail["From"] = self.email_sender
        mail["To"] = user_email
        mail["Subject"] = subject
        mail.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as smtp:
            smtp.login(self.email_sender, self.email_password)
            smtp.sendmail(self.email_sender, user_email, mail.as_string())

    @staticmethod
    def get_password_updated_mail(username):
        mail_body = f"""
            ¡Hi {username}! 
            Your password has been updated.
            You can sign_up with your new credentials.


            Thank you.
            BlackJack team.
        """
        return mail_body

    @staticmethod
    def get_user_created_mail(username):
        mail_body = f"""
            ¡Hi {username}! 
            User created successfully.


            Thank you.
            BlackJack team.
        """
        return mail_body
