import requests
from fastapi import APIRouter, HTTPException, Depends
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from requests.exceptions import HTTPError

router = APIRouter()


@router.post("/start_game/{game_id}")
def start_game(game_id: str, current_user: User = Depends(authenticate_with_token)):
    try:
        url = f'http://game_management_service:5001/start_game/{game_id}'
        response = requests.post(url=url, json={
            'user_id': current_user.id
        })
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
