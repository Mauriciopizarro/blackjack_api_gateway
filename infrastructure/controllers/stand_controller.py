import requests
from requests import HTTPError
from domain.user import User
from fastapi import APIRouter, HTTPException, Depends
from infrastructure.authentication.fast_api_authentication import authenticate_with_token

router = APIRouter()


@router.post("/game/stand/{game_id}")
async def stand_controller(game_id: str, current_user: User = Depends(authenticate_with_token)):
    try:
        url = f'http://game_service:5002/game/stand/{game_id}'
        response = requests.post(url, json={
            'user_id': current_user.id
        })
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
