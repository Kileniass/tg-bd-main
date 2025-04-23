from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    age = Column(Integer)
    car_model = Column(String)
    car_description = Column(String)
    region = Column(String)
    profile_photo = Column(String)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Отношения
    profiles = relationship("Profile", back_populates="user")
    sent_likes = relationship("Like", foreign_keys="Like.sender_id", back_populates="sender")
    received_likes = relationship("Like", foreign_keys="Like.receiver_id", back_populates="receiver") 