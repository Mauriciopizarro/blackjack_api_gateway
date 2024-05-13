import requests
from fastapi import APIRouter, HTTPException, Depends
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from requests.exceptions import HTTPError
from config import settings

router = APIRouter()


@router.post("/game/start/{game_id}")
def start_game(game_id: str, current_user: User = Depends(authenticate_with_token)):
    try:
        url = f"{settings.GAME_MANAGEMENT_API_URL}/game/start/{game_id}"
        response = requests.post(url=url, json={
            'user_id': current_user.id
        })
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
