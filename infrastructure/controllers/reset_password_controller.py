from domain.user import User
from pydantic import BaseModel
from fastapi import HTTPException, APIRouter, Depends
from domain.exceptions import NotExistentUser, EmptyNewPassword
from application.reset_password_service import ResetPasswordService
from infrastructure.authentication.fast_api_authentication import authenticate_with_token

router = APIRouter()
reset_password_service = ResetPasswordService()


class ResetPasswordRequestData(BaseModel):
    new_password: str
    repeat_new_password: str


@router.post("/user/reset_password")
async def reset_password_controller(request: ResetPasswordRequestData,  current_user: User = Depends(authenticate_with_token)):
    try:
        if request.new_password == request.repeat_new_password:
            reset_password_service.reset_password(user_name=current_user.username, new_password=request.new_password)
        else:
            raise HTTPException(
                status_code=400,
                detail="Password are not matching, try again",
            )
    except NotExistentUser:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    except EmptyNewPassword:
        raise HTTPException(
            status_code=400,
            detail="'new_password' field is empty",
        )
    return {"message": "Password has been updated successfully"}
