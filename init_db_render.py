import os
from app.database import engine, Base
from app.models.user import User
from app.models.profile import Profile
from app.models.likes import Like
from alembic.config import Config
from alembic import command

def init_db():
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    
    # Инициализируем Alembic
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
    
    # Создаем и применяем миграции
    command.stamp(alembic_cfg, "head")

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!") 