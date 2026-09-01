from fastapi import APIRouter, Depends
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from config import settings
from infrastructure.proxy import proxy_request

router = APIRouter()


@router.post("/game/croupier_play/{game_id}")
async def croupier_controller(game_id: str, current_user: User = Depends(authenticate_with_token)):
    return proxy_request(
        'POST', f'{settings.GAME_API_URL}/game/croupier_play/{game_id}',
    )

