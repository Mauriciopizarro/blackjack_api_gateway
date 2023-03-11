from abc import ABC, abstractmethod
from domain.user import UserInDB, UserPlainPassword


class UserRepository(ABC):

    @abstractmethod
    def is_mail_in_use(self, email: str) -> bool:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> UserInDB:
        pass

    @abstractmethod
    def save_user(self, user: UserPlainPassword) -> UserPlainPassword:
        pass

    @abstractmethod
    def update_password(self, user: UserInDB):
        pass
