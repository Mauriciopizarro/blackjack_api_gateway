import requests
from typing import Union
from config import settings
from domain.user import User
from requests import HTTPError
from pydantic import BaseModel, confloat
from fastapi import APIRouter, HTTPException, Depends
from infrastructure.authentication.fast_api_authentication import authenticate_with_token

router = APIRouter()


class StatusResponse(BaseModel):
    amount: confloat(gt=-1)
    user_id: Union[int, str]


@router.get("/wallet/get/{user_id}", response_model=StatusResponse)
async def get_status_controller(current_user: User = Depends(authenticate_with_token)):
    try:
        response = requests.get(f'{settings.WALLET_API_URL}/wallet/get/{current_user.id}')
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        raise HTTPException(
            status_code=response.status_code, detail=response.json().get('detail'),
        )
