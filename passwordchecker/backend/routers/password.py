from fastapi import APIRouter

from schemas.password import PasswordCheckRequest, PasswordCheckResponse
from services.password_service import PasswordService

router = APIRouter(prefix="/password", tags=["password"])


@router.post("/check", response_model=PasswordCheckResponse)
def check_password(payload: PasswordCheckRequest):
    return PasswordService().check(payload.password)
