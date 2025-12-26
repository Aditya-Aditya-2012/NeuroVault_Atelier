#backend/src/schemas.py
from pydantic import BaseModel, EmailStr
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserShow(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True