from pydantic import BaseModel
from typing import Optional

class ProfileBase(BaseModel):
    description: Optional[str] = None
    car_description: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileInDB(ProfileBase):
    id: int
    user_id: int
    photo: Optional[str] = None
    car_photo: Optional[str] = None

    class Config:
        from_attributes = True 