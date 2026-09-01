from fastapi import APIRouter, Depends
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from config import settings
from infrastructure.proxy import proxy_request

router = APIRouter()


@router.post("/game/create")
async def create_game(current_user: User = Depends(authenticate_with_token)):
    return proxy_request(
        'POST', f'{settings.GAME_MANAGEMENT_API_URL}/game/create',
        json={'username': current_user.username, 'user_id': current_user.id},
    )

