from fastapi import APIRouter, Depends
from pydantic import BaseModel
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from config import settings
from infrastructure.proxy import proxy_request

router = APIRouter()


class PlaceBetRequestData(BaseModel):
    bet_amount: int


@router.post("/game/make_bet/{game_id}")
async def make_bet_controller(game_id: str, request: PlaceBetRequestData, current_user: User = Depends(authenticate_with_token)):
    return proxy_request(
        'POST', f'{settings.GAME_API_URL}/game/make_bet/{game_id}',
        json={'player_id': current_user.id, 'bet_amount': request.bet_amount},
    )

