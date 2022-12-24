from dependency_injector.wiring import Provide, inject
from domain.exceptions import EmptyNewPassword
from domain.user import UserInDB, UserPlainPassword
from infrastructure.injector import Injector
from domain.interfaces.publisher import Publisher
from domain.interfaces.user_repository import UserRepository

import logging
from logging.config import dictConfig
from infrastructure.logging import LogConfig


dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class ResetPasswordService:

    @inject
    def __init__(
            self,
            user_repository: UserRepository = Provide[Injector.user_repo],
            publisher: Publisher = Provide[Injector.publisher]
    ):

        self.user_repository = user_repository
        self.publisher = publisher

    def reset_password(self, user_name: str, new_password: str):
        # in a future is posible add old_password and if the old_password is correct, new_password is updated
        if not new_password:
            raise EmptyNewPassword()
        user_db = self.user_repository.get_by_username(user_name)
        user = UserPlainPassword(username=user_db.username, id=user_db.id, plain_password=new_password, email=user_db.email)
        hash_password = user.get_hashed_password()
        updated_user = UserInDB(username=user_db.username, id=user_db.id, hashed_password=hash_password, email=user_db.email)
        self.user_repository.update_password(updated_user)
        message = {
            "email": user_db.email,
            "subject": "Your password has been updated"
        }
        self.publisher.send_message(message=message, topic="password_updated_send_email")
        logger.info("message sended to password_updated topic")
