from fastapi import APIRouter
from config import settings
from infrastructure.proxy import proxy_request

router = APIRouter()


@router.get("/player/history/{user_id}")
async def get_history_controller(user_id: str):
    return proxy_request('GET', f'{settings.GAME_API_URL}/player/history/{user_id}')

