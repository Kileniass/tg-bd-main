from pydantic import BaseModel

class AboutUpdate(BaseModel):
    user_id: int
    about: str 