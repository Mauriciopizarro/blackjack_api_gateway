from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig


router = APIRouter()
dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class Player(BaseModel):
    cards: List[str]
    id: str
    is_stand: bool
    name: str
    status: str
    total_points: List[int]


class Croupier(BaseModel):
    cards: List[str]
    is_stand: bool
    name: str
    status: str
    total_points: List[int]


class StatusResponse(BaseModel):
    croupier: Croupier
    players: List[Player]
    players_quantity: int
    status_game: str


@router.get("/player_status/{game_id}", response_model=StatusResponse)
async def get_status_controller(game_id: str):
    logger.warning("Please add an HTTP call to game_service")
    """ 
    try:
        player_status_json = status_service.players_status(game_id)
        return player_status_json
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
        """