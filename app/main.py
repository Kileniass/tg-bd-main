from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, crud, database, utils, schemas
from app.database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import AboutUpdate
from app.core.config import settings
from app.routers import auth_router, profiles_router, likes_router

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Middleware для CORS - разрешаем запросы с любых доменов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы: GET, POST и т.д.
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Подключение роутеров
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(profiles_router, prefix=settings.API_V1_STR)
app.include_router(likes_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Car Dating App API"}

@app.get("/api/init/{telegram_id}")
def init_user(telegram_id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id)
    if not user:
        new_user = schemas.UserCreate(telegram_id=telegram_id)
        user = crud.create_user(db, new_user)
    return user

@app.put("/api/users/{telegram_id}")
def update_user_profile(telegram_id: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, telegram_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.get("/api/users/{telegram_id}")
def get_user_profile(telegram_id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/profiles/{user_id}/like")
def like_profile(user_id: int, current_user_id: int, db: Session = Depends(get_db)):
    like, match = crud.like_user(db, current_user_id, user_id)
    return {"like": like.id if like else None, "match": match.id if match else None}

@app.post("/profiles/{user_id}/dislike")
def dislike_profile(user_id: int, current_user_id: int, db: Session = Depends(get_db)):
    crud.dislike_user(db, current_user_id, user_id)
    return {"message": "Profile disliked"}

@app.get("/profiles/next")
def next_profile(current_user_id: int, db: Session = Depends(get_db)):
    profile = crud.get_next_profile(db, current_user_id)
    if profile:
        return {
            "profile": {
                "id": profile.id,
                "name": profile.name,
                "age": profile.age,
                "photo_url": profile.photo_url,
                "car": profile.car,
                "region": profile.region,
                "about": profile.about
            }
        }
    else:
        return {"message": "No more profiles"}

@app.get("/matches/{user_id}")
def matches(user_id: int, db: Session = Depends(get_db)):
    matched_users = crud.get_matches(db, user_id)
    return {
        "matches": [
            {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "photo_url": user.photo_url,
                "car": user.car,
                "region": user.region,
                "about": user.about
            }
            for user in matched_users
        ]
    }

@app.get("/generate-password")
def generate_password():
    password = utils.generate_password()
    return {"password": password}

@app.put("/profiles/about")
def update_about(data: AboutUpdate, db: Session = Depends(get_db)):
    user = crud.update_about(db, user_id=data.user_id, about_text=data.about)
    if user:
        return {"message": "About section updated", "about": user.about}
    else:
        return {"message": "User not found"}
