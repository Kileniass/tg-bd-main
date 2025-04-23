from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB
from app.core.security import create_access_token
from typing import Optional

router = APIRouter()

@router.post("/auth/telegram", response_model=UserInDB)
async def auth_telegram(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Проверяем, существует ли пользователь
    db_user = db.query(User).filter(User.telegram_id == user_data.telegram_id).first()
    
    if db_user:
        # Обновляем данные пользователя
        for key, value in user_data.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    else:
        # Создаем нового пользователя
        db_user = User(**user_data.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    # Создаем токен доступа
    access_token = create_access_token(data={"sub": str(db_user.id)})
    
    return {
        **db_user.__dict__,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/auth/me", response_model=UserInDB)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user 