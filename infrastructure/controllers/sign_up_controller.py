from pydantic import BaseModel, ValidationError
from fastapi import HTTPException, APIRouter
from domain.exceptions import UserExistent
from domain.user import EmptyPasswordError
from application.sign_up_service import SignUpService

router = APIRouter()
sign_up_service = SignUpService()


class SignUpRequestData(BaseModel):
    email: str
    username: str
    password: str


class SignUpResponseData(BaseModel):
    token: str
    username: str
    user_id: str
    email: str


@router.post("/sign_up", response_model=SignUpResponseData)
async def sign_up_controller(request: SignUpRequestData):
    try:
        return sign_up_service.sign_up(request.username, request.password, request.email)
    except EmptyPasswordError:
        raise HTTPException(
            status_code=400,
            detail="Empty password, please complete the password field",
        )
    except UserExistent:
        raise HTTPException(
            status_code=400,
            detail="Username already in use, try another",
        )
    except ValidationError:
        raise HTTPException(
            status_code=400,
            detail="Field 'email' contains a not valid email address",
        )
