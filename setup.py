from setuptools import setup, find_packages

setup(
    name="car_dating_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "sqlalchemy==2.0.23",
        "pydantic==2.5.2",
        "python-multipart==0.0.6",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-dotenv==1.0.0",
        "python-telegram-bot==20.7",
        "aiofiles==23.2.1",
        "pydantic-settings==2.1.0",
        "python-magic==0.4.27",
        "psycopg2-binary==2.9.9",
        "alembic==1.13.1"
    ],
) 