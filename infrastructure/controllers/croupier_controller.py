from fastapi import APIRouter, HTTPException, Depends
from requests.exceptions import HTTPError
import requests


router = APIRouter()


@router.post("/game/croupier_play/{game_id}")
async def croupier_controller(game_id: str):
    try:
        response = requests.post(f'http://game_service:5002/game/croupier_play/{game_id}')
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
