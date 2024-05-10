from fastapi import APIRouter, HTTPException, Depends
from requests.exceptions import HTTPError
import requests
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token


router = APIRouter()


@router.post("/game/croupier_play/{game_id}")
async def croupier_controller(game_id: str, current_user: User = Depends(authenticate_with_token)):
    try:
        response = requests.post(f'http://game_service:5002/game/croupier_play/{game_id}')
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
