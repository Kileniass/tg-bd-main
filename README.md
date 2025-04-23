# Car Dating App

Веб-приложение для знакомств автолюбителей с интеграцией Telegram.

## Требования

- Python 3.8+
- SQLite (для разработки)
- PostgreSQL (для продакшена)
- Telegram Bot Token

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd car-dating-app
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env и заполните его:
```bash
cp .env.example .env
# Отредактируйте .env файл, добавив свои значения
```

5. Инициализируйте базу данных:
```bash
python -m app.init_db
```

## Запуск

1. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

2. Откройте в браузере:
```
http://localhost:8000
```

## API Документация

После запуска сервера, документация API будет доступна по адресу:
```
http://localhost:8000/docs
```

## Деплой на Render

1. Создайте аккаунт на [Render](https://render.com)

2. Создайте новый Web Service:
   - Подключите ваш GitHub репозиторий
   - Выберите ветку для деплоя
   - Укажите следующие настройки:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. Создайте PostgreSQL базу данных:
   - В панели управления Render выберите "New +" -> "PostgreSQL"
   - После создания базы данных, скопируйте External Database URL
   - Добавьте его в переменные окружения вашего Web Service как `DATABASE_URL`

4. Добавьте остальные переменные окружения:
   - `SECRET_KEY`: сгенерируйте случайную строку
   - `TELEGRAM_BOT_TOKEN`: токен вашего Telegram бота

5. После деплоя, инициализируйте базу данных:
   ```bash
   python init_db_render.py
   ```

## Структура проекта

```
app/
├── core/           # Основные настройки и конфигурация
├── models/         # Модели базы данных
├── schemas/        # Pydantic схемы
├── routers/        # API роутеры
└── database.py     # Настройки базы данных
```

## Основные функции

- Регистрация и авторизация через Telegram
- Создание и редактирование профиля
- Загрузка фотографий
- Просмотр анкет других пользователей
- Система лайков и мэтчей
- Уведомления о новых лайках и мэтчах

## Разработка

1. Создайте новую ветку для ваших изменений:
```bash
git checkout -b feature/your-feature-name
```

2. Внесите изменения и закоммитьте их:
```bash
git add .
git commit -m "Описание ваших изменений"
```

3. Отправьте изменения в репозиторий:
```bash
git push origin feature/your-feature-name
```

## Лицензия

MIT 