from app.database import engine, Base
from app.models.user import User
from app.models.profile import Profile
from app.models.likes import Like

def init_db():
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!") 