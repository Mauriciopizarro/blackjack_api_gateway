from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig
from fastapi import APIRouter, Depends
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token

router = APIRouter()
dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


@router.post("/create_game")
async def create_game(current_user: User = Depends(authenticate_with_token)):

    logger.warning("Please add an HTTP call to game_management_service")
    #game = create_game_service.create_game(username=current_user.username, user_id=current_user.id)
    #return {
    #    "message": "Game created",
    #    "id": game.id,
    #    "admin": {
    #        "name": current_user.username,
    #        "id": current_user.id
    #    }
    #}
