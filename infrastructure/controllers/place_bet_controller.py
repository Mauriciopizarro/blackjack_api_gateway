import requests
from pydantic import BaseModel
from requests import HTTPError
from domain.user import User
from fastapi import APIRouter, HTTPException, Depends
from infrastructure.authentication.fast_api_authentication import authenticate_with_token

router = APIRouter()

class PlaceBetRequestData(BaseModel):
    bet_amount: int


@router.post("/game/make_bet/{game_id}")
async def stand_controller(game_id: str, request: PlaceBetRequestData, current_user: User = Depends(authenticate_with_token)):
    try:
        url = f'http://game_service:5002/game/make_bet/{game_id}'
        response = requests.post(url, json={
            'player_id': current_user.id,
            'bet_amount': request.bet_amount
        })
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
