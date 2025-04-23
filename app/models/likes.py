from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    is_match = Column(Boolean, default=False)
    
    # Отношения
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_likes")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_likes") 