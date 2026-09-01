import time

import requests
from fastapi import APIRouter
from config import settings
from infrastructure.proxy import proxy_request


router = APIRouter()

# Una partida en pending_bet con más de 30 minutos se considera fantasma
# (abandonada antes de que todos apostaran).
GHOST_GAME_SECONDS = 30 * 60


@router.get("/game/lobby/list/{user_id}")
async def get_lobby_list_controller(user_id: str):
    data = proxy_request('GET', f'{settings.GAME_MANAGEMENT_API_URL}/game/lobby/list/{user_id}')
    games = data.get('games', [])
    enriched_games = []

    # El game_management solo guarda "created"/"started". El estado real
    # (pending_bet/started/finished) lo tiene el game_service. Enriquecimos
    # cada partida con su estado real para que el front pueda filtrar las
    # terminadas.
    for game in games:
        status = game.get('status')
        game_id = game.get('game_id')
        if not game_id:
            continue

        # Partidas fantasma: pending_bet con más de 30 minutos son abandonadas
        # (el flujo normal de apuestas tarda segundos) y nunca pasan a finished.
        # Se ocultan del listado.
        try:
            created_ts = int(game_id[:8], 16)  # timestamp embebido en el ObjectId
            if status == 'pending_bet' and (time.time() - created_ts) > GHOST_GAME_SECONDS:
                continue
        except (ValueError, TypeError):
            pass

        try:
            game_status_response = requests.get(
                f'{settings.GAME_API_URL}/game/status/{game_id}', timeout=2
            )
            if game_status_response.ok:
                status = game_status_response.json().get('status_game', status)
        except Exception:
            # Si el game_service aún no tiene la partida (aún no se dio
            # "start"), conservamos el estado del game_management.
            pass
        game['status'] = status
        # Las partidas terminadas no corresponden al listado de "juegos
        # activos": se descartan una vez conocido su estado real.
        if status == 'finished':
            continue
        enriched_games.append(game)

    return {"user_id": data.get('user_id'), "games": enriched_games}


@router.get("/game/lobby/{game_id}")
async def get_lobby_controller(game_id: str):
    return proxy_request('GET', f'{settings.GAME_MANAGEMENT_API_URL}/game/lobby/{game_id}')
