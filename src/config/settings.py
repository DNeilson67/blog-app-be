from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # CORS
    FRONTEND_URL: str = "https://dn-blog-wheat.vercel.app"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
