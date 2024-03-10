from dependency_injector.wiring import Provide, inject
from domain.exceptions import EmailInUse
from domain.user import UserPlainPassword
from infrastructure.injector import Injector
from domain.interfaces.publisher import Publisher
from domain.interfaces.user_repository import UserRepository
from application.token_service import TokenService


class SignUpService:

    @inject
    def __init__(
            self, user_repository: UserRepository = Provide[Injector.user_repo],
            publisher: Publisher = Provide[Injector.publisher]
    ):
        self.user_repository = user_repository
        self.publisher = publisher

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
        create_wallet_message = {
            "user_id": user_response.id
        }
        self.publisher.send_message(message=send_email_user_created_message, topic="user_created_send_email")
        self.publisher.send_message(message=create_wallet_message, topic="create_new_wallet")
        return access_info
