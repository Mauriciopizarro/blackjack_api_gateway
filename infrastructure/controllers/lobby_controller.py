import time
from typing import Dict, Tuple

import requests
from fastapi import APIRouter
from config import settings
from infrastructure.proxy import proxy_request, _parse_json


router = APIRouter()

# Una partida en pending_bet con más de 30 minutos se considera fantasma
# (abandonada antes de que todos apostaran).
GHOST_GAME_SECONDS = 30 * 60

# El front dispara /game/lobby/list por varias vías a la vez (eventos socket
# `newGame`/`gameUpdated` globales + focus/visibility en N pestañas). Cada
# request = 1 llamada a game_management + N a game_service (enriquecimiento
# de estado). Sin collapsar, la ráfaga multiplica las llamadas downstream y
# el hosting free responde 429. Cache corto por user_id: 1 sola llamada real
# cada 2 segundos.
_LOBBY_LIST_TTL_SECONDS = 2
_lobby_list_cache: Dict[str, Tuple[float, dict]] = {}


@router.get("/game/lobby/list/{user_id}")
async def get_lobby_list_controller(user_id: str):
    now = time.time()
    cached = _lobby_list_cache.get(user_id)
    if cached is not None and (now - cached[0]) < _LOBBY_LIST_TTL_SECONDS:
        return cached[1]

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
                # Parseo defensivo: el game_service puede devolver basura no-JSON
                # (Render 502/503, servicio dormido). Igual que el resto de los
                # controllers, usamos _parse_json en vez de response.json().
                game_status_data = _parse_json(game_status_response)
                if isinstance(game_status_data, dict):
                    status = game_status_data.get('status_game', status)
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

    result = {"user_id": data.get('user_id'), "games": enriched_games}
    _lobby_list_cache[user_id] = (now, result)
    return result


@router.get("/game/lobby/{game_id}")
async def get_lobby_controller(game_id: str):
    return proxy_request('GET', f'{settings.GAME_MANAGEMENT_API_URL}/game/lobby/{game_id}')
