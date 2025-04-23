from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    telegram_id: int
    username: str
    full_name: str
    age: int
    car_model: str
    car_description: str
    region: str
    description: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    car_model: Optional[str] = None
    car_description: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True 