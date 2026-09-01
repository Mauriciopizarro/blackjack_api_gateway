import logging
import requests
from requests.exceptions import RequestException

from config import settings
from logging.config import dictConfig
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class MoneyServiceHttpClient:

    create_wallet_path = "/wallet/create_wallet/{user_id}"

    def create_wallet(self, user_id: str):
        """Creates the user wallet in the money_service via HTTP.

        Best-effort: si el money_service no responde, el registro del
        usuario ya se completó, así que no fallamos el sign_up (igual
        que pasaba cuando la wallet se creaba por RabbitMQ); solo
        dejamos registrado el error.
        """
        url = f"{settings.WALLET_API_URL}{self.create_wallet_path.format(user_id=user_id)}"
        try:
            requests.post(url=url, timeout=30)
        except RequestException:
            logger.warning(f"Could not create wallet in money_service for user {user_id}", exc_info=True)
            return
        logger.info(f"Wallet created in money_service via HTTP for user {user_id}")
