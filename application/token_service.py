from dependency_injector.wiring import Provide, inject
from domain.interfaces.auth_provider import AuthProvider
from domain.user import User, UserInDB
from infrastructure.injector import Injector
from datetime import datetime, timedelta
from jose import jwt
from domain.interfaces.user_repository import UserRepository
from config import settings


class TokenService:

    @staticmethod
    def generate_token(user: User):
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta
        to_encode = {
            "exp": expire,
            "sub": user.username
        }
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    @inject
    def get_user_by_token(token: str,
                          user_repository: UserRepository = Provide[Injector.user_repo],
                          auth_provider: AuthProvider = Provide[Injector.auth_provider]
                          ) -> UserInDB:
        user_data = auth_provider.get_user_data(token)
        user = user_repository.get_by_username(user_data["username"])
        return user
