from app.database import Base, engine
from app.models.user import User
from app.models.profile import Profile
from app.models.likes import Like

def init_db():
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    print("База данных успешно инициализирована")

if __name__ == "__main__":
    init_db() 