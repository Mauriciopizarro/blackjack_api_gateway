from fastapi import APIRouter, HTTPException
from requests import HTTPError
import requests
from config import settings


router = APIRouter()


@router.get("/player/history/{user_id}")
async def get_history_controller(user_id: str):
    try:
        response = requests.get(f'{settings.GAME_API_URL}/player/history/{user_id}')
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
