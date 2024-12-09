from typing import List, Optional
from pydantic_settings import BaseSettings
import json
from functools import lru_cache

class Settings(BaseSettings):
    # 基本配置
    PROJECT_NAME: str = "Agent Tools API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    DEBUG: bool = False
    
    # CORS配置
    BACKEND_CORS_ORIGINS: str = "[]"

    @property
    def BACKEND_CORS_ORIGINS_LIST(self) -> List[str]:
        try:
            return json.loads(self.BACKEND_CORS_ORIGINS)
        except json.JSONDecodeError:
            return []

    # 数据库配置
    DATABASE_URL: str

    # JWT配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 运行时配置
    RUN_MODE: str = "dev"
    PORT: int = 8111

    # SMTP配置
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> request_id={extra[request_id]} <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    LOG_PATH: str = "logs/api.log"
    LOG_ROTATION: str = "20 days"
    LOG_RETENTION: str = "1 months"

    # 安全配置
    ALLOWED_HOSTS: str = '["*"]'
    MAX_REQUESTS_PER_MINUTE: int = 60
    SSL_KEYFILE: Optional[str] = None
    SSL_CERTFILE: Optional[str] = None

    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # 其他配置
    TIMEZONE: str = "Asia/Shanghai"
    DEFAULT_LANGUAGE: str = "zh-cn"

    @property
    def ALLOWED_HOSTS_LIST(self) -> List[str]:
        try:
            return json.loads(self.ALLOWED_HOSTS)
        except json.JSONDecodeError:
            return ["*"]

    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 