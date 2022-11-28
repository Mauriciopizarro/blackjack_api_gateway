from fastapi import APIRouter, HTTPException
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

router = APIRouter()
dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


@router.post("/croupier_play/{game_id}")
async def croupier_controller(game_id: str):

    #try:
    logger.warning("Please add an HTTP call to game_service")
    #    croupier_service.croupier_play(game_id)
    #except NotCroupierTurnError:
    #    raise HTTPException(
    #        status_code=400, detail='Is not the croupier turn',
    #    )
    #except IncorrectGameID:
    #    raise HTTPException(
    #        status_code=404, detail='game_id not found',
    #    )
    #except GameFinishedError:
    #    raise HTTPException(
    #        status_code=400, detail='The game_id entered is finished',
    #    )
    #return {'message': "Croupier is playing"}
