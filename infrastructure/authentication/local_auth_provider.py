from typing import Dict
from jose import jwt, JWTError
from domain.interfaces.auth_provider import AuthProvider
from infrastructure.authentication.exceptions import InvalidTokenError
from config import settings


class LocalAuthProvider(AuthProvider):

    def get_user_data(self, token: str) -> Dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise InvalidTokenError()
        except JWTError:
            raise InvalidTokenError()
        return {"username": username}
