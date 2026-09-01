from pydantic import BaseModel
from fastapi import APIRouter, Depends
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from config import settings
from infrastructure.proxy import proxy_request

router = APIRouter()


class EnrollPlayerResponse(BaseModel):
    message: str
    name: str
    player_id: str


@router.post("/game/enroll_player/{game_id}", response_model=EnrollPlayerResponse)
async def enroll_player(game_id: str, current_user: User = Depends(authenticate_with_token)):
    return proxy_request(
        'POST', f'{settings.GAME_MANAGEMENT_API_URL}/game/enroll_player/{game_id}',
        json={'username': current_user.username, 'user_id': current_user.id},
    )

