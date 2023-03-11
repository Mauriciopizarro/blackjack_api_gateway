from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from requests import HTTPError
from typing import List
import requests


router = APIRouter()


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


@router.get("/game/status/{game_id}", response_model=StatusResponse)
async def get_status_controller(game_id: str):
    try:
        response = requests.get(f'http://game_service:5002/game/status/{game_id}')
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
