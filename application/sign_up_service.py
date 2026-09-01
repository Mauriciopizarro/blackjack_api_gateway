from dependency_injector.wiring import Provide, inject
from domain.exceptions import EmailInUse
from domain.user import UserPlainPassword
from infrastructure.injector import Injector
from infrastructure.http_clients.money_service_http_client import MoneyServiceHttpClient
from domain.interfaces.user_repository import UserRepository
from application.token_service import TokenService
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class SignUpService:

    @inject
    def __init__(
            self,
            user_repository: UserRepository = Provide[Injector.user_repo],
            money_service_http_client: MoneyServiceHttpClient = Provide[Injector.money_service_http_client]
    ):
        self.user_repository = user_repository
        self.money_service_http_client = money_service_http_client

    def sign_up(self, username, plain_password, email):
        if self.user_repository.is_mail_in_use(email):
            raise EmailInUse()
        user = UserPlainPassword(username=username, plain_password=plain_password, email=email)
        user_response = self.user_repository.save_user(user)
        token = TokenService.generate_token(user_response)
        access_info = {
            "token": token,
            "username": user_response.username,
            "user_id": user_response.id,
            "email": user_response.email
        }
        send_email_user_created_message = {
            "username": user_response.username,
            "email": user_response.email,
            "subject": "User has been successfully created"
        }
        logger.info(f"User created email notification (no email service): {send_email_user_created_message}")
        self.money_service_http_client.create_wallet(user_id=user_response.id)
        return access_info
