from logging.config import dictConfig
import logging

import requests

from infrastructure.logging import LogConfig
from fastapi import APIRouter, Depends
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token

router = APIRouter()
dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


@router.post("/create_game")
async def create_game(current_user: User = Depends(authenticate_with_token)):
    url = "http://game_management_service:5001/create_game"
    response = requests.post(url=url, json={
        'username': current_user.username,
        'user_id': current_user.id
    })

    return response.json()
