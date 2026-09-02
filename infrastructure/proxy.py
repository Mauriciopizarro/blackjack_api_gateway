"""Proxy HTTP hacia los microservicios downstream.

Todos los controllers del gateway usan este helper para que una
respuesta vacía, no-JSON (por ejemplo una página HTML de error que
devuelve el proxy de Render cuando el servicio está caído o
reiniciando) o un timeout no reviente el gateway con un
JSONDecodeError sin manejar.
"""
from typing import Any, Optional
from urllib.parse import urlparse

import requests
from fastapi import HTTPException
from requests.exceptions import RequestException

# Amplio a propósito: los free tier de Render se duermen y el primer
# request puede tardar en despertar el servicio downstream.
DEFAULT_TIMEOUT = 30


def _parse_json(response: requests.Response) -> Optional[Any]:
    try:
        return response.json()
    except ValueError:
        return None


def proxy_request(method: str, url: str, timeout: int = DEFAULT_TIMEOUT, **kwargs) -> Any:
    """Ejecuta una llamada HTTP a un microservicio y devuelve su JSON.

    - Servicio caído / inalcanzable / timeout -> 502.
    - Respuesta OK pero con cuerpo vacío o no-JSON -> 502.
    - Respuesta de error -> propaga el status y el `detail` del
      downstream si el cuerpo es JSON parseable.
    """
    try:
        response = requests.request(method, url, timeout=timeout, **kwargs)
    except RequestException:
        raise HTTPException(
            status_code=502,
            detail='Downstream service is unavailable',
        )

    data = _parse_json(response)

    if response.ok:
        if data is None:
            raise HTTPException(
                status_code=502,
                detail='Downstream service returned an invalid response',
            )
        return data

    detail = data.get('detail') if isinstance(data, dict) else None
    # Identificamos el servicio downstream en el mensaje: sin esto un
    # 429/503 es indistinguible entre game/money/game_management.
    downstream = urlparse(response.url).netloc
    raise HTTPException(
        status_code=response.status_code,
        detail=detail or f'Downstream service {downstream} returned status {response.status_code}',
    )
