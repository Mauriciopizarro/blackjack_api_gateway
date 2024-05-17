from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from application.login_service import LoginService
from application.token_service import TokenService
from domain.exceptions import NotExistentUser
from domain.user import IncorrectPasswordError


router = APIRouter()
login_service = LoginService()


class ResponseDataModel(BaseModel):
    access_token: str
    token_type: str
    user_id: str


class LoginRequestData(BaseModel):
    username_or_email: str
    password: str


@router.post("/login", response_model=ResponseDataModel)
async def login_for_access_token(json_data: LoginRequestData):
    try:
        user = login_service.authenticate_user(json_data.username_or_email, json_data.password)
    except NotExistentUser:
        raise HTTPException(
            status_code=404,
            detail="User does not exist",
        )
    except IncorrectPasswordError:
        raise HTTPException(
            status_code=400,
            detail="Incorrect password",
        )
    access_token = TokenService.generate_token(user)
    return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id
    }
