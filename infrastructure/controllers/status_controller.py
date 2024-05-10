from fastapi import APIRouter, HTTPException
from requests import HTTPError
import requests


router = APIRouter()


@router.get("/game/status/{game_id}")
async def get_status_controller(game_id: str):
    try:
        response = requests.get(f'http://game_service:5002/game/status/{game_id}')
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
