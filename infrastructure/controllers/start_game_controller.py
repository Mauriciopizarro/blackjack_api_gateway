from fastapi import APIRouter, HTTPException, Depends
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig


router = APIRouter()
dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


@router.post("/start_game/{game_id}")
def start_game(game_id: str, current_user: User = Depends(authenticate_with_token)):
    logger.warning("Please add an HTTP call to game_management_service")
    """ 
    try:
        star_game_service.start_game(game_id, current_user.id)
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
    except GameAlreadyStarted:
        raise HTTPException(
            status_code=400, detail='Game already started'
        )
    except IncorrectAdminId:
        raise HTTPException(
            status_code=400, detail='User not enabled for this action'
        )
    return {'message': "Game started"}
    """