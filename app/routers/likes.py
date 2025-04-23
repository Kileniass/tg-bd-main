from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.likes import Like
from app.schemas.likes import LikeCreate, LikeInDB
from typing import List

router = APIRouter()

@router.post("/likes/", response_model=LikeInDB)
async def create_like(
    like: LikeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Проверяем, существует ли профиль, которому ставим лайк
    receiver = db.query(User).filter(User.id == like.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверяем, не поставили ли мы уже лайк этому пользователю
    existing_like = db.query(Like).filter(
        Like.sender_id == current_user.id,
        Like.receiver_id == like.receiver_id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Like already exists")
    
    # Создаем новый лайк
    db_like = Like(sender_id=current_user.id, **like.dict())
    db.add(db_like)
    
    # Проверяем, есть ли взаимный лайк
    mutual_like = db.query(Like).filter(
        Like.sender_id == like.receiver_id,
        Like.receiver_id == current_user.id
    ).first()
    
    if mutual_like:
        # Если есть взаимный лайк, отмечаем оба как мэтч
        db_like.is_match = True
        mutual_like.is_match = True
    
    db.commit()
    db.refresh(db_like)
    return db_like

@router.get("/likes/matches", response_model=List[LikeInDB])
async def read_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    matches = db.query(Like).filter(
        Like.sender_id == current_user.id,
        Like.is_match == True
    ).all()
    return matches

@router.get("/likes/received", response_model=List[LikeInDB])
async def read_received_likes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    received_likes = db.query(Like).filter(
        Like.receiver_id == current_user.id
    ).all()
    return received_likes 