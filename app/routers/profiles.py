from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileInDB
from typing import List
import shutil
import os

router = APIRouter()

@router.post("/profiles/", response_model=ProfileInDB)
async def create_profile(
    profile: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_profile = Profile(**profile.dict(), user_id=current_user.id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/profiles/", response_model=List[ProfileInDB])
async def read_profiles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    profiles = db.query(Profile).offset(skip).limit(limit).all()
    return profiles

@router.get("/profiles/{profile_id}", response_model=ProfileInDB)
async def read_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.put("/profiles/{profile_id}", response_model=ProfileInDB)
async def update_profile(
    profile_id: int,
    profile: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    if db_profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    for key, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.post("/profiles/{profile_id}/photo")
async def upload_profile_photo(
    profile_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    if db_profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Создаем директорию для фото, если её нет
    os.makedirs("uploads", exist_ok=True)
    
    # Сохраняем файл
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Обновляем путь к фото в базе данных
    db_profile.photo = file_path
    db.commit()
    db.refresh(db_profile)
    
    return {"filename": file.filename} 