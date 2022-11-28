from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig
from domain.user import User
from fastapi import APIRouter, HTTPException, Depends
from infrastructure.authentication.fast_api_authentication import authenticate_with_token

router = APIRouter()
dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


@router.post("/stand/{game_id}")
async def stand_controller(game_id: str, current_user: User = Depends(authenticate_with_token)):
    logger.warning("Please add an HTTP call to game_service")

    """ 
    try:
        stand_service.stand(current_user.id, game_id)
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
    except GameFinishedError:
        raise HTTPException(
            status_code=400, detail='The game_id entered is finished',
        )
    except IncorrectPlayerTurn:
        raise HTTPException(
            status_code=400, detail='Is not a turn to player entered',
        )
    return {'message': "Player stand"}
    """