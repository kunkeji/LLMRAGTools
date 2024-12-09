from typing import List
from pydantic_settings import BaseSettings
import json
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Your API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: str = "[]"

    @property
    def BACKEND_CORS_ORIGINS_LIST(self) -> List[str]:
        try:
            return json.loads(self.BACKEND_CORS_ORIGINS)
        except json.JSONDecodeError:
            return []

    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Runtime configuration
    RUN_MODE: str = "dev"
    PORT: int = 8111

    # SMTP 配置
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = ""
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = ""
    
    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 