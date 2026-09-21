from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth.users import authenticate_user
from auth.jwt_handler import create_access_token

router = APIRouter(prefix="/api/v1", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": user["username"]})
    return TokenResponse(access_token=token)