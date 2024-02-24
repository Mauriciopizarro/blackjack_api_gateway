import ssl
import smtplib
from config import settings
from email.message import EmailMessage
from domain.interfaces.notify_user import NotifyUser


class SendEmail(NotifyUser):

    def __init__(self):
        self.email_sender = settings.EMAIL_SENDER
        self.email_password = settings.EMAIL_PASSWORD

    def send_email(self, user_email, subject, body):
        mail = EmailMessage()
        mail["From"] = self.email_sender
        mail["To"] = user_email
        mail["Subject"] = subject
        mail.set_content(body, subtype='html')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, port=settings.EMAIL_PORT, context=context) as smtp:
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
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome {username}!</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    background: linear-gradient(135deg, #6c5ce7, #fd79a8);
                }}
                h1 {{
                    color: #ffffff;
                    text-align: center;
                }}
                p {{
                    color: #ffffff;
                    text-align: center;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    color: #ffffff;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome {username}!</h1>
                <p>Your account has been successfully created.</p>
                <div class="footer">
                    <p>Thank you,</p>
                    <p>BlackJack team</p>
                </div>
            </div>
        </body>
        </html>
        """
        return mail_body
