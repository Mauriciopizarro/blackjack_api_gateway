import time
from typing import Dict, Tuple

from fastapi import APIRouter
from config import settings
from infrastructure.proxy import proxy_request


router = APIRouter()

# Una partida en pending_bet con más de 30 minutos se considera fantasma
# (abandonada antes de que todos apostaran).
GHOST_GAME_SECONDS = 30 * 60

# El front dispara /game/lobby/list por varias vías a la vez (eventos socket
# `newGame`/`gameUpdated` globales + focus/visibility en N pestañas). Sin
# collapsar, la ráfaga multiplica las llamadas downstream y el hosting free
# responde 429. Cache corto por user_id: 1 sola llamada real cada 2 segundos.
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

    # Descarta partidas fantasma: pending_bet con más de 30 minutos son
    # abandonadas (el flujo normal de apuestas tarda segundos) y nunca pasan
    # a finished.
    def is_ghost(game_id: str, status: str) -> bool:
        if status != 'pending_bet':
            return False
        try:
            created_ts = int(game_id[:8], 16)  # timestamp embebido en el ObjectId
            return (time.time() - created_ts) > GHOST_GAME_SECONDS
        except (ValueError, TypeError):
            return False

    # Estado real de TODAS las partidas en UNA sola llamada batch (en vez de
    # N llamadas a /game/status/{id}, que multiplicaban la carga downstream).
    game_ids = [g['game_id'] for g in games if g.get('game_id')]
    statuses: Dict[str, str] = {}
    try:
        batch = proxy_request(
            'POST', f'{settings.GAME_API_URL}/game/status/batch',
            json={'game_ids': game_ids},
        )
        for item in batch.get('games', []):
            statuses[item['game_id']] = item['status_game']
    except Exception:
        # Si el game_service no responde (duerme/levanta), conservamos el
        # estado del game_management y seguimos.
        pass

    for game in games:
        game_id = game.get('game_id')
        if not game_id:
            continue
        if is_ghost(game_id, game.get('status')):
            continue

        status = statuses.get(game_id, game.get('status'))
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
