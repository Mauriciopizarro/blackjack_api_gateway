from typing import Union

from pydantic import BaseModel, confloat
from fastapi import APIRouter, Depends
from config import settings
from domain.user import User
from infrastructure.authentication.fast_api_authentication import authenticate_with_token
from infrastructure.proxy import proxy_request

router = APIRouter()


class StatusResponse(BaseModel):
    amount: confloat(gt=-1)
    user_id: Union[int, str]


@router.get("/wallet/get/{user_id}", response_model=StatusResponse)
async def get_status_controller(current_user: User = Depends(authenticate_with_token)):
    return proxy_request(
        'GET', f'{settings.WALLET_API_URL}/wallet/get/{current_user.id}'
    )

