from pydantic import BaseModel

class LikeBase(BaseModel):
    receiver_id: int

class LikeCreate(LikeBase):
    pass

class LikeInDB(LikeBase):
    id: int
    sender_id: int
    is_match: bool

    class Config:
        from_attributes = True 