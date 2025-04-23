from app.routers.auth import router as auth_router
from app.routers.profiles import router as profiles_router
from app.routers.likes import router as likes_router

__all__ = ['auth_router', 'profiles_router', 'likes_router'] 