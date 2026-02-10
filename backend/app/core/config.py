import os
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS"))

@dataclass(frozen=True)
class Settings:
    serve_backend: str = os.getenv("SERVE_BACKEND", "redis").lower()
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_db: int = int(os.getenv("REDIS_DB", 0))

settings = Settings()


