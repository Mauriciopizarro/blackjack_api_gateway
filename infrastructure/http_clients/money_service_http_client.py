import requests
from config import settings
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class MoneyServiceHttpClient:

    create_wallet_path = "/wallet/create_wallet/{user_id}"

    def create_wallet(self, user_id: str):
        """Creates the user wallet in the money_service via HTTP."""
        url = f"{settings.WALLET_API_URL}{self.create_wallet_path.format(user_id=user_id)}"
        response = requests.post(url=url)
        response.raise_for_status()
        logger.info(f"Wallet created in money_service via HTTP for user {user_id}")