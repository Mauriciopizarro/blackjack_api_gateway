import requests
from fastapi import APIRouter, Depends, HTTPException
from requests import HTTPError
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token

router = APIRouter()


@router.post("/game/create")
async def create_game(current_user: User = Depends(authenticate_with_token)):
    try:
        url = "http://game_management_service:5001/game/create"
        response = requests.post(url=url, json={
            'username': current_user.username,
            'user_id': current_user.id
        })
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
