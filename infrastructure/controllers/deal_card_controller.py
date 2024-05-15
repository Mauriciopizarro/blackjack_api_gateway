from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from fastapi import APIRouter, HTTPException, Depends
from requests.exceptions import HTTPError
from domain.user import User
import requests
from config import settings


router = APIRouter()


@router.post("/game/deal_card/{game_id}")
async def deal_card_controller(game_id: str, current_user: User = Depends(authenticate_with_token)):

    try:
        url = f'{settings.GAME_API_URL}/game/deal_card/{game_id}'
        response = requests.post(url, json={
            'user_id': current_user.id
        })
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
