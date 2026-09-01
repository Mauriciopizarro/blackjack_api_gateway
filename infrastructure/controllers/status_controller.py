from fastapi import APIRouter
from config import settings
from infrastructure.proxy import proxy_request

router = APIRouter()


@router.get("/game/status/{game_id}")
async def get_status_controller(game_id: str):
    return proxy_request('GET', f'{settings.GAME_API_URL}/game/status/{game_id}')

