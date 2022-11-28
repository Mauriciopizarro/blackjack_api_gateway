from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig


router = APIRouter()
dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class EnrollPlayerResponse(BaseModel):
    message: str
    name: str
    player_id: str


@router.post("/enroll_player/{game_id}", response_model=EnrollPlayerResponse)
async def enroll_player(game_id: str, current_user: User = Depends(authenticate_with_token)):

    logger.warning("Please add an HTTP call to game_management_service")

    """ 
    try:
        player_id = enroll_player_service.enroll_player(current_user.username, current_user.id, game_id)
        return EnrollPlayerResponse(
            message="Player enrolled successfully",
            name=str(current_user.username),
            player_id=str(player_id)
        )
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
    except CantEnrollPlayersStartedGame:
        raise HTTPException(
            status_code=400, detail='Can not enroll players in game started'
        )
    except AlreadyEnrolledPlayer:
        raise HTTPException(
            status_code=400, detail='Player already enrolled'
        )
        """