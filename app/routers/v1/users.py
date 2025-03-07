from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.service.user import create_user, get_users
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def register_user(user_data: UserCreate):
    user = create_user(user_data.name, user_data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return UserResponse(id=str(user.id), name=user.name, email=user.email)


@router.get("/", response_model=List[UserResponse])
def list_users():
    return [
        UserResponse(id=str(user.id), name=user.name, email=user.email)
        for user in get_users()
    ]
