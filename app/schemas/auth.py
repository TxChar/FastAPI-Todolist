from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    display_name: str
    email: EmailStr
    password: str
