from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    photo = Column(String)
    description = Column(String)
    car_photo = Column(String)
    car_description = Column(String)
    
    # Отношения
    user = relationship("User", back_populates="profiles") 