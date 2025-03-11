from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.account import Account
from app.dependencies.auth import get_current_user

from app.schemas.auth import RegisterRequest
from app.service.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/account", tags=["account"])


@router.post("/register")
async def register(data: RegisterRequest):
    if Account.objects(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(data.password)
    account = Account(
        display_name=data.display_name,
        email=data.email,
        password=hashed_password,
    )
    account.save()

    return {"message": "Account created successfully"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    account = Account.objects(email=form_data.username).first()
    if not account or not verify_password(form_data.password, account.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": account.email, "role": account.role})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    return {"email": user["email"], "role": user["role"]}
